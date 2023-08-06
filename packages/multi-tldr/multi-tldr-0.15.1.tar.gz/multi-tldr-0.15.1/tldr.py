#!/usr/bin/env python3
# encoding: utf-8

"""
Yet another python client for tldr-pages/tldr. View tldr pages in multi repo, multi platform, any language at the same time.
This tldr client is designed based on the tldr-pages client specification 1.4, but not 100% implemented.
https://github.com/Phuker/multi-tldr
"""

import os
import sys
import argparse
import logging
import re
import json
import subprocess
import functools

# buggy: https://github.com/pallets/click/issues/665
# import readline

import click


__title__ = 'multi-tldr'
__version__ = '0.15.1'
__author__ = 'Phuker'
__homepage__ = 'https://github.com/Phuker/multi-tldr'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 Phuker, Copyright (c) 2015 lord63'
__specification__ = 'This tldr client is designed based on the tldr-pages client specification 1.4, but not 100% implemented.'

VERSION_STR_SHORT = f'{__title__} {__version__}'
VERSION_STR_LONG = f'{__title__} {__version__}\n{__doc__.strip()}'
ALL_PLATFORM_LIST = ('common', 'linux', 'osx', 'sunos', 'windows', 'android')
SUPPORTED_COLORS = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'bright_black', 'bright_red', 'bright_green', 'bright_yellow', 'bright_blue', 'bright_magenta', 'bright_cyan', 'bright_white')

logger = logging.getLogger(__name__)
config = {
    'repo_directory_list': [],
    'color_output': 'auto',
    'colors': {
        'description': 'bright_yellow',
        'usage': 'green',
        'command': 'white',
        'param': 'cyan',
    },
    'command_indent_size': 4,
    'platform_list': [
        'common',
        'linux',
    ],
    'compact_output': False,
}


def _assert(expr, msg=''):
    if not expr:
        raise AssertionError(msg)


def _init_logging():
    logging_stream = sys.stderr
    logging_format = '%(asctime)s [%(levelname)s]:%(message)s'
    logging_level = logging.INFO

    if logging_stream.isatty():
        logging_date_format = '%H:%M:%S'
    else:
        logging_date_format = '%Y-%m-%d %H:%M:%S %z'

    logging.basicConfig(
        level=logging_level,
        format=logging_format,
        datefmt=logging_date_format,
        stream=logging_stream,
    )


def _logging_set_color_output():
    handler = logging.root.handlers[0]
    handler.setFormatter(logging.Formatter('\x1b[1m%(asctime)s [%(levelname)s]:\x1b[0m%(message)s', handler.formatter.datefmt))

    logging.addLevelName(logging.CRITICAL, '\x1b[31m{}\x1b[39m'.format(logging.getLevelName(logging.CRITICAL)))
    logging.addLevelName(logging.ERROR, '\x1b[31m{}\x1b[39m'.format(logging.getLevelName(logging.ERROR)))
    logging.addLevelName(logging.WARNING, '\x1b[33m{}\x1b[39m'.format(logging.getLevelName(logging.WARNING)))
    logging.addLevelName(logging.INFO, '\x1b[36m{}\x1b[39m'.format(logging.getLevelName(logging.INFO)))
    logging.addLevelName(logging.DEBUG, '\x1b[36m{}\x1b[39m'.format(logging.getLevelName(logging.DEBUG)))


def _parse_args(args=sys.argv[1:]):
    choices_platform = ALL_PLATFORM_LIST + ('all', 'default')

    parser = argparse.ArgumentParser(
        description=VERSION_STR_LONG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-i', '--init', action='store_true', help='Interactively gererate config file')
    group.add_argument('-l', '--list', action='store_true', help='Print all tldr page files path (of a command if specified) in all repo on all/specified platform')
    group.add_argument('-u', '--update', action='store_true', help='Pull all git repo')
    
    parser.add_argument('command', help='Command to query', nargs='*')
    parser.add_argument('-p', '--platform', metavar='platform', help="Specify platform, choices: %(choices)s", choices=choices_platform)

    parser.add_argument('-V', '--version', action='version', version=VERSION_STR_LONG, help='Show version and exit')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase verbosity level (use -vv or more for greater effect)')

    result = parser.parse_args(args)

    if result.verbose >= 1:
        logging.root.setLevel(logging.DEBUG)
    
    if result.command:
        result.command = '-'.join(result.command)
    else:
        result.command = None
    
    ctrl_group_set = result.init or result.list or result.update
    ok_conditions = [
        result.init and result.command is None and result.platform is None,
        result.list,
        result.update and result.command is None and result.platform is None,
        not ctrl_group_set and result.command is not None,
    ]

    if not any(ok_conditions):
        logger.error('Bad command line arguments')
        parser.print_help()
        sys.exit(1)

    logger.debug('Command line arguments: %r', result)

    return result


def get_config_dir_path():
    sub_dir_name = 'multi-tldr'

    if 'TLDR_CONFIG_DIR' in os.environ:
        config_dir_path = os.environ.get('TLDR_CONFIG_DIR')
    elif 'XDG_CONFIG_HOME' in os.environ:
        config_dir_path = os.path.join(os.environ.get('XDG_CONFIG_HOME'), sub_dir_name)
    else:
        config_dir_path = os.path.join('~', '.config', sub_dir_name)
    
    config_dir_path = os.path.abspath(os.path.expanduser(config_dir_path))

    return config_dir_path


def get_config_file_path():
    return os.path.join(get_config_dir_path(), 'tldr.config.json')


def check_config(json_data):
    _assert(isinstance(json_data, dict), 'Invalid config')

    if 'repo_directory_list' in json_data:
        _assert(isinstance(json_data['repo_directory_list'], list), 'Invalid config: repo_directory_list')
        for _repo_dir in json_data['repo_directory_list']:
            _assert(isinstance(_repo_dir, str), 'Invalid config: repo_directory_list')
            _assert(os.path.isdir(os.path.abspath(os.path.expanduser(_repo_dir))), f'Invalid config: repo_directory_list, repo directory not exist: {_repo_dir!r}')

    if 'color_output' in json_data:
        _assert(isinstance(json_data['color_output'], str), 'Invalid config: color_output')
        _assert(json_data['color_output'] in ('always', 'auto', 'never'), 'Invalid config: color_output')
    
    if 'colors' in json_data:
        _assert(isinstance(json_data['colors'], dict), 'Invalid config: colors')
        _assert(json_data['colors'].keys() == config['colors'].keys(), 'Invalid config: colors')
        if not set(json_data['colors'].values()).issubset(set(SUPPORTED_COLORS)):
            bad_colors = set(json_data['colors'].values()) - set(SUPPORTED_COLORS)
            bad_colors_str = ', '.join([repr(_) for _ in bad_colors])
            raise ValueError(f'Invalid config: colors, unsupported colors: {bad_colors_str}')
    
    if 'command_indent_size' in json_data:
        _assert(isinstance(json_data['command_indent_size'], int), 'Invalid config: command_indent_size')
        _assert(json_data['command_indent_size'] >= 0, 'Invalid config: command_indent_size')

    if 'platform_list' in json_data:
        _assert(isinstance(json_data['platform_list'], list), 'Invalid config: platform_list')
        for platform in json_data['platform_list']:
            _assert(isinstance(platform, str), 'Invalid config: platform_list')
    
    if 'compact_output' in json_data:
        _assert(isinstance(json_data['compact_output'], bool), 'Invalid config: compact_output')


def load_json(file_path):
    _assert(isinstance(file_path, str))

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error('Error when load json file %r: %r %r', file_path, type(e), e)
        sys.exit(1)


def load_config():
    """Load config file and overwrite default config object"""

    config_file_path = get_config_file_path()
    if not os.path.isfile(config_file_path):
        logger.error("Can't find config file at: %r", config_file_path)
        logger.error('You may use `tldr --init` to init the config file')
        return

    logger.debug('Reading config file: %r', config_file_path)
    json_data = load_json(config_file_path)

    logger.debug('Check config')
    try:
        check_config(json_data)
    except Exception as e:
        logger.error('Check config failed: %r', e)
        logger.error('You may use `tldr --init` to init the config file')
        return
    
    logger.debug('Overwrite default config object')
    for k in config:
        if k in json_data:
            config[k] = json_data[k]

    config['repo_directory_list'] = [os.path.abspath(os.path.expanduser(_)) for _ in config['repo_directory_list']]
    logger.debug('Final config:\n%s', json.dumps(config, ensure_ascii=False, indent=4))


def do_color_output():
    color_output = config['color_output']

    return color_output == 'always' or (color_output == 'auto' and sys.stdout.isatty() and 'TERM' in os.environ)


def style(text, *args, **kwargs):
    """Wrapper of click.style()"""

    if do_color_output():
        return click.style(text, *args, **kwargs)
    else:
        return text


@functools.lru_cache
def get_escape_str(*args, **kwargs):
    """Wrapper of style(), get escape string without reset string at the end"""

    if 'reset' not in kwargs:
        kwargs['reset'] = False
    
    return style('', *args, **kwargs)


@functools.lru_cache
def get_escape_str_by_type(_type):
    """Get escape string by type"""

    _assert(_type is None or isinstance(_type, str))

    colors = config['colors']

    if _type is None:
        return ''
    elif _type in ('description', 'usage', 'command'):
        return get_escape_str(fg=colors[_type], underline=False)
    elif _type == 'param':
        return get_escape_str(fg=colors[_type], underline=True)
    else:
        raise ValueError(f'Unexpected type: {_type!r}')


def parse_inline_md(line, line_type):
    """Parse inline markdown syntax"""

    line_list = re.split(r'(`|\{\{|\}\})', line)
    line_list = [_ for _ in line_list if len(_) > 0]
    code_started = False
    result = ''
    
    result += get_escape_str_by_type(line_type)
    type_stack = [None] * 8 # fail safe, for invalid line like '- abc {def}} ghi'
    type_stack.append(line_type)
    for item in line_list:
        if item == '`':
            if not code_started:
                result += get_escape_str_by_type('command')
                type_stack.append('command')
            else:
                type_stack.pop()
                result += get_escape_str_by_type(type_stack[-1])
            
            code_started = not code_started
        elif item == '{{':
            result += get_escape_str_by_type('param')
            type_stack.append('param')
        elif item == '}}':
            type_stack.pop()
            result += get_escape_str_by_type(type_stack[-1])
        else:
            result += item
    
    result += get_escape_str(reset=True)
    return result


def parse_page(page_file_path):
    """Parse the command man page."""

    compact_output = config['compact_output']
    command_indent_size = config['command_indent_size']

    logger.debug('Reading file: %r', page_file_path)
    with open(page_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines() # with '\n' end
    
    output_lines = []
    for line in lines:
        line = line.strip('\n')
        if line.startswith('# '): # h1
            continue
        elif line.startswith('> '): # description
            line = parse_inline_md(line[2:], 'description')
            output_lines.append(line)
        elif line.startswith('- '): # usage
            line = parse_inline_md(line[2:], 'usage')
            output_lines.append(line)
        elif line.startswith('`'): # code example
            line = line.strip('`')
            line = parse_inline_md(line, 'command')
            line = (' ' * command_indent_size) + line
            output_lines.append(line)
        elif line == '':
            if not compact_output:
                # default: reset = True, add reset string at the end
                output_lines.append(style(line))
            else:
                pass
        else:
            line = parse_inline_md(line, 'usage')
            output_lines.append(line)
    
    output_lines.append(style('')) # gap new line + fail safe reset
    return output_lines


@functools.lru_cache
def get_index(repo_directory):
    """Generate index in the pages directory.
    Return: [(platform, command), ]
    """

    _assert(isinstance(repo_directory, str))

    index = []

    logger.debug('os.walk() in %r', repo_directory)
    tree_generator = os.walk(repo_directory)
    platforms = next(tree_generator)[1]
    
    for platform in platforms:
        pages = next(tree_generator)[2]
        index += [(platform, page[:-3]) for page in pages if page.endswith('.md')] # there is no .MD uppercase
    
    return index


def get_page_path_list(command=None, platform='default'):
    """Get page_path_list in all repo"""

    _assert(command is None or isinstance(command, str))
    _assert(isinstance(platform, str))

    repo_directory_list = config['repo_directory_list']
    default_platform_set = set(config['platform_list'])

    page_path_list = []
    for repo_directory in repo_directory_list:
        index = get_index(repo_directory)

        if command is not None:
            filter_func = lambda entry: entry[1] == command
            index = filter(filter_func, index)
        
        if platform == 'all':
            pass
        elif platform == 'default':
            index = filter(lambda entry: entry[0] in default_platform_set, index)
        else:
            index = filter(lambda entry: entry[0] == platform, index)

        page_path_list += [os.path.join(repo_directory, entry[0], entry[1] + '.md') for entry in index]
    
    return page_path_list


def action_init():
    """Interactively gererate config file"""

    config_file_path = get_config_file_path()
    if os.path.exists(config_file_path):
        logger.warning('A config file already exists: %r', config_file_path)
        if click.prompt('Are you sure want to overwrite it? (yes/no)', default='no') != 'yes':
            return
    
    repo_path_list = []
    logger.info('Please input repo path line by line, to "pages/" level, empty line to end.')
    while True:
        repo_path = click.prompt('Input 1 tldr repo path', default='')
        if len(repo_path) == 0:
            break
        repo_path = os.path.abspath(os.path.expanduser(repo_path))
        if not os.path.exists(repo_path):
            logger.error('Repo path not exist, clone it first.')
        elif repo_path not in repo_path_list:
            repo_path_list.append(repo_path)

    platform_list = []
    platform_choice = click.Choice(ALL_PLATFORM_LIST + ('', ))
    logger.info('Please input default platforms line by line, empty line to end.')
    while True:
        platform = click.prompt('Input 1 platform', type=platform_choice, default='')
        if len(platform) == 0:
            break
        elif platform not in platform_list:
            platform_list.append(platform)

    logger.info('Please input colors, empty to use default.')
    colors_choice = click.Choice(SUPPORTED_COLORS)
    colors = {
        'description': click.prompt('Input color for description', type=colors_choice, default='bright_yellow'),
        'usage': click.prompt('Input color for usage', type=colors_choice, default='green'),
        'command': click.prompt('Input color for command', type=colors_choice, default='white'),
        'param': click.prompt('Input color for param', type=colors_choice, default='cyan'),
    }

    color_output_choice = click.Choice(('always', 'auto', 'never'))
    color_output = click.prompt('When output with color?', type=color_output_choice, default='auto')

    command_indent_size = click.prompt('Command indent size?', type=int, default=4)
    if command_indent_size < 0:
        command_indent_size = 0

    compact_output = click.prompt('Enable compact output (not output empty lines)? (yes/no)', default='no') == 'yes'

    config = {
        'repo_directory_list': repo_path_list,
        'color_output': color_output,
        'colors': colors,
        'command_indent_size': command_indent_size,
        'platform_list': platform_list,
        'compact_output': compact_output,
    }

    config_dir_path = get_config_dir_path()
    if not os.path.exists(config_dir_path):
        logger.info('Make dir: %r', config_dir_path)
        os.makedirs(config_dir_path)

    logger.info('Write to config file %r', config_file_path)
    with open(config_file_path, 'w') as f:
        f.write(json.dumps(config, ensure_ascii=False, indent=4))


def action_update():
    """Update all tldr pages repo."""

    repo_directory_list = config['repo_directory_list']
    command = ['git', 'pull', '--stat']
    command_str = ' '.join(command)

    exist_error = False
    logger.info('Check for updates in all repo directories')
    for i, repo_directory in enumerate(repo_directory_list):
        os.chdir(repo_directory)
        logger.info('(%d/%d) Check for updates in %r ...', i + 1, len(repo_directory_list), repo_directory)
        try:
            return_code = subprocess.call(command)
            if return_code == 0:
                return_code_color = 'green'
            else:
                return_code_color = 'bright_red'
                exist_error = True
            
            return_code_str = style(str(return_code), fg=return_code_color)
            logger.info('Command %r return code %s', command_str, return_code_str)
        except Exception as e:
            logger.error('Error when run %r in %r: %r %r', command_str, repo_directory, type(e), e)
            exist_error = True
    
    if exist_error:
        logger.info('Check for updates finished with error')
        sys.exit(1)
    else:
        logger.info('Check for updates finished')


def action_find(command, platform):
    """Find and display the tldr pages of a command."""

    _assert(isinstance(command, str))
    _assert(platform is None or isinstance(platform, str))

    if platform:
        page_path_list = get_page_path_list(command, platform)
    else:
        page_path_list = get_page_path_list(command, 'default')
    
    if len(page_path_list) == 0:
        logger.error('Command not found: %r', command)
        logger.error('You can try to find a page on all platforms by run %r.', f'tldr -p all {command}')
        logger.error('If still nothing, you can create a new issue against the tldr-pages/tldr GitHub repository: %r,', f'https://github.com/tldr-pages/tldr/issues/new?title=page%20request:%20{command}')
        logger.error('or create a Pull Request on GitHub.')
        sys.exit(1)
    else:
        for page_path in page_path_list:
            print(style(command, underline=True, bold=True) + ' - ' + style(page_path, underline=True, bold=True))
            output_lines = parse_page(page_path)
            for line in output_lines:
                print(line)


def action_list_command(command, platform):
    """Locate all tldr page files path of the command."""
    
    _assert(command is None or isinstance(command, str))
    _assert(platform is None or isinstance(platform, str))

    if platform:
        page_path_list = get_page_path_list(command, platform)
    else:
        page_path_list = get_page_path_list(command, 'all')
    
    for page_path in page_path_list:
        print(page_path)


def broken_pipe_error_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # https://docs.python.org/3/library/signal.html#note-on-sigpipe
        try:
            return func(*args, **kwargs)
        except BrokenPipeError:
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
            sys.exit(1)

    return wrapper


@broken_pipe_error_wrapper
def main():
    global config

    _init_logging()
    shell_args = _parse_args()

    if shell_args.init:
        action_init()
    else:
        load_config()
        if do_color_output():
            _logging_set_color_output()

        if shell_args.list:
            action_list_command(shell_args.command, shell_args.platform)
        elif shell_args.update:
            action_update()
        else:
            action_find(shell_args.command, shell_args.platform)
    
    sys.stdout.flush()


if __name__ == '__main__':
    main()
