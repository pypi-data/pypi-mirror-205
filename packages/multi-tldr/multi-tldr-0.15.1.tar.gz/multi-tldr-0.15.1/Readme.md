# multi-tldr

Yet another python client for [tldr-pages/tldr](https://github.com/tldr-pages/tldr). View tldr pages in multi repo, multi platform, any language at the same time.

Forked from [lord63/tldr.py](https://github.com/lord63/tldr.py), whose original idea is very good. Modified a large proportion of code.

## Intro

Instead of the long man pages, tldr will give you several simple yet powerful examples:

![multi-tldr tar command](screenshots/screenshot1.png)

The command examples are not good? The tldr pages are just [simplified markdown files](https://github.com/tldr-pages/tldr/blob/master/contributing-guides/style-guide.md). You can easily contribute to [tldr-pages/tldr](https://github.com/tldr-pages/tldr), or create your own repo and keep your pages private.

One more thing, `tldr` is just a simple version for the man page, it's **NOT** an alternative. Sometimes, you should read the man pages patiently.

## Features

- No internet requests when lookup a tldr page, it is always fast.
- tldr pages are managed by `git`, and updated manually by `tldr --update`.
- Support display tldr pages in multi repo, multi platform, any language at the same time. You can create your own private tldr pages repo, add all dirs you want to the config file, whose path specified to the language level, e.g. `/path/to/pages/` or `/path/to/pages.xx/`.
- Support custom output style, including color, compact output (not output empty lines).

![multi-tldr custom output style](screenshots/screenshot2.png)

### Other differences with `lord63/tldr.py`

- No need to use `tldr find some_command` or create an alias of `tldr find`, just type `tldr some_command` ([related issue](https://github.com/lord63/tldr.py/issues/47))
- No need to rebuild `index.json` index file.
- Advanced parser: render nested `` ` `` inline code, `{{` and `}}` arguments ([related issue](https://github.com/lord63/tldr.py/issues/25)).
- Config file format `YAML` --> `JSON`, because I hate `YAML`.
- Drop support for Python 2.
- Simplify (just delete) tests code

## Requirements

- Python >= `3.6`, with `pip` installed

### Recommend

- Git: if you do not have `git`, you can still download `.zip` file from [tldr-pages/tldr](https://github.com/tldr-pages/tldr), extract it, and add it when run `tldr --init`, most things still work, but `tldr --update` will NOT work.

### For Windows users

A better terminal is recommended, which must support [ANSI escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code), and make sure `git` command is available. You may try and/or combine these: [Cmder](https://cmder.net/), [Cygwin](https://www.cygwin.com/), [Windows Terminal](https://github.com/microsoft/terminal), [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10), [Git for Windows](https://gitforwindows.org/), [scoop](https://github.com/lukesampson/scoop), [Chocolatey](https://chocolatey.org/), etc.

Test your environment with Python 3:

```python
#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import shutil

print(f'sys.stdout.isatty() -> {sys.stdout.isatty()}')
print(f'env TERM = {os.environ.get("TERM")!r}')
print('Test ANSI escape sequences: \x1b[31mred \x1b[1mbold\x1b[0m')
print(f'git command is: {shutil.which("git")!r}')
```

If you are using Windows 10, you can import this to the Windows Registry to enable [ANSI escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code) of `cmd` and `PowerShell` to enable colord output ([related discussions](https://superuser.com/questions/413073/windows-console-with-ansi-colors-handling)):

```registry
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Console]
"VirtualTerminalLevel"=dword:00000001
```

If output is not colored, try set `color_output` in the config file to `always`.

## Install

First, uninstall any other existing tldr client.

Then, use `pip` to install:

```bash
python3 -m pip install -U multi-tldr
```

## Initialize manually

This program won't work out of the box, first you need to initialize it manually.

### Clone [tldr-pages/tldr](https://github.com/tldr-pages/tldr)

`cd` to some directory (e.g. `~/code/tldr`) and clone the [tldr-pages/tldr](https://github.com/tldr-pages/tldr) repo. We will use it when we look up a command usage.

```bash
git clone --depth=1 https://github.com/tldr-pages/tldr.git
```

### Create config file

Then, run this command to interactively generate configuration file:

```bash
tldr --init
```

The default location for the config file is `~/.config/multi-tldr/tldr.config.json`. You can use `TLDR_CONFIG_DIR` and `XDG_CONFIG_HOME` environment variable to point it to another path. If `TLDR_CONFIG_DIR` is `/a/b/c`, config file is `/a/b/c/tldr.config.json`. If `XDG_CONFIG_HOME` is `/a/b/c`, config file is `/a/b/c/multi-tldr/tldr.config.json`.

Your configuration file should look like this:

```json
{
    "repo_directory_list": [
        "/home/user/code/tldr/pages/",
        "/home/user/code/tldr-private/pages.zh"
    ],
    "color_output": "auto",
    "colors": {
        "description": "bright_yellow",
        "usage": "green",
        "command": "white",
        "param": "cyan"
    },
    "command_indent_size": 4,
    "platform_list": [
        "common",
        "osx",
        "linux"
    ],
    "compact_output": false
}
```

The `colors` option is for the output when you look for a command, you can custom it by yourself. (Note that the color should be in `'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'bright_black', 'bright_red', 'bright_green', 'bright_yellow', 'bright_blue', 'bright_magenta', 'bright_cyan', 'bright_white'`)

## Usage

This tldr client is designed based on the [tldr-pages client specification 1.4](https://github.com/tldr-pages/tldr/blob/master/CLIENT-SPECIFICATION.md), so it is very similar to other clients. But the specification is not 100% implemented, there is some differences.

### Show help message

```console
$ tldr --help
usage: tldr [-h] [-i | -l | -u] [-p platform] [-V] [-v] [command ...]

multi-tldr 0.15.1
Yet another python client for tldr-pages/tldr. View tldr pages in multi repo, multi platform, any language at the same time.
This tldr client is designed based on the tldr-pages client specification 1.4, but not 100% implemented.
https://github.com/Phuker/multi-tldr

positional arguments:
  command               Command to query

options:
  -h, --help            show this help message and exit
  -i, --init            Interactively gererate config file
  -l, --list            Print all tldr page files path (of a command if specified) in all repo on all/specified platform
  -u, --update          Pull all git repo
  -p platform, --platform platform
                        Specify platform, choices: common, linux, osx, sunos, windows, android, all, default
  -V, --version         Show version and exit
  -v, --verbose         Increase verbosity level (use -vv or more for greater effect)
```

### Show version info

```console
$ tldr --version
multi-tldr 0.15.1
Yet another python client for tldr-pages/tldr. View tldr pages in multi repo, multi platform, any language at the same time.
This tldr client is designed based on the tldr-pages client specification 1.4, but not 100% implemented.
https://github.com/Phuker/multi-tldr
```

### Look up a command usage

```console
$ tldr tar
tar - /home/user/code/tldr/pages/common/tar.md

Archiving utility.
Often combined with a compression method, such as gzip or bzip2.
More information: <https://www.gnu.org/software/tar>.

[c]reate an archive and write it to a [f]ile:

    tar cf path/to/target.tar path/to/file1 path/to/file2 ...

[c]reate a g[z]ipped archive and write it to a [f]ile:

    tar czf path/to/target.tar.gz path/to/file1 path/to/file2 ...

[c]reate a g[z]ipped archive from a directory using relative paths:

    tar czf path/to/target.tar.gz --directory=path/to/directory .

E[x]tract a (compressed) archive [f]ile into the current directory [v]erbosely:

    tar xvf path/to/source.tar[.gz|.bz2|.xz]

E[x]tract a (compressed) archive [f]ile into the target directory:

    tar xf path/to/source.tar[.gz|.bz2|.xz] --directory=path/to/directory

[c]reate a compressed archive and write it to a [f]ile, using [a]rchive suffix to determine the compression program:

    tar caf path/to/target.tar.xz path/to/file1 path/to/file2 ...

Lis[t] the contents of a tar [f]ile [v]erbosely:

    tar tvf path/to/source.tar

E[x]tract files matching a pattern from an archive [f]ile:

    tar xf path/to/source.tar --wildcards "*.html"

```

`tldr git pull` is same as `tldr git-pull`:

```console
$ tldr git pull
git-pull - /home/user/code/tldr/pages/common/git-pull.md

Fetch branch from a remote repository and merge it to local repository.
More information: <https://git-scm.com/docs/git-pull>.

Download changes from default remote repository and merge it:

    git pull

Download changes from default remote repository and use fast-forward:

    git pull --rebase

Download changes from given remote repository and branch, then merge them into HEAD:

    git pull remote_name branch

```

By default, only pages on default platforms in `platform_list` are output. You can specify platform using `-p` argument.

Only macOS `osx` platform:

```console
$ tldr -p osx airport
airport - /home/user/code/tldr/pages/osx/airport.md

Wireless network configuration utility.
More information: <https://ss64.com/osx/airport.html>.

Show current wireless status information:

    airport --getinfo

Sniff wireless traffic on channel 1:

    airport sniff 1

Scan for available wireless networks:

    airport --scan

Disassociate from current airport network:

    sudo airport --disassociate

```

All platforms:

```console
$ tldr -p all snoop
snoop - /home/user/code/tldr/pages/sunos/snoop.md

Network packet sniffer.
SunOS equivalent of tcpdump.
More information: <https://www.unix.com/man-page/sunos/1m/snoop>.

Capture packets on a specific network interface:

    snoop -d e1000g0

Save captured packets in a file instead of displaying them:

    snoop -o path/to/file

Display verbose protocol layer summary of packets from a file:

    snoop -V -i path/to/file

Capture network packets that come from a hostname and go to a given port:

    snoop to port port from host hostname

Capture and show a hex-dump of network packets exchanged between two IP addresses:

    snoop -x0 -p4 ip1 ip2

```

### List tldr page files path

List all pages on all platforms:

```console
$ tldr --list | head -n 3
/home/user/code/tldr/pages/linux/xbacklight.md
/home/user/code/tldr/pages/linux/pacman-query.md
/home/user/code/tldr/pages/linux/nmcli-agent.md
```

All platforms, only `tar` command:

```console
$ tldr --list tar
/home/user/code/tldr/pages/common/tar.md
```

Only `linux` platform:

```console
$ tldr --list -p linux | head -n 3
/home/user/code/tldr/pages/linux/xbacklight.md
/home/user/code/tldr/pages/linux/pacman-query.md
/home/user/code/tldr/pages/linux/nmcli-agent.md
```

Only `common` platform, only `du` command:

```console
$ tldr --list -p common du
/home/user/code/tldr/pages/common/du.md
```

Only default platforms in config:

```console
$ tldr --list -p default | head -n 3
/home/user/code/tldr/pages/linux/xbacklight.md
/home/user/code/tldr/pages/linux/pacman-query.md
/home/user/code/tldr/pages/linux/nmcli-agent.md
```

Only default platforms in config, only `tree` command:

```console
$ tldr --list -p default tree
/home/user/code/tldr/pages/common/tree.md
```

Fuzzy find a command:

```console
$ tldr -l | grep git | grep show
/home/user/code/tldr/pages/common/git-show-unmerged-branches.md
/home/user/code/tldr/pages/common/git-show-index.md
/home/user/code/tldr/pages/common/git-show-merged-branches.md
/home/user/code/tldr/pages/common/git-show-ref.md
/home/user/code/tldr/pages/common/git-show.md
/home/user/code/tldr/pages/common/git-show-branch.md
/home/user/code/tldr/pages/common/git-show-tree.md
```

### Check for updates

`git pull` will be run in all dir paths of `repo_directory_list`, so that we can get the latest tldr pages.

```console
$ tldr --update
08:00:00 [INFO]:Check for updates in all repo directories
08:00:00 [INFO]:(1/2) Check for updates in '/home/user/code/tldr/pages' ...
Already up to date.
08:00:00 [INFO]:Command 'git pull --stat' return code 0
08:00:00 [INFO]:(2/2) Check for updates in '/home/user/code/tldr-private/pages' ...
Already up to date.
08:00:00 [INFO]:Command 'git pull --stat' return code 0
08:00:00 [INFO]:Check for updates finished
```

## FAQ

**Q: I want to add some custom command usages to a command, how to do it?**

**Q: I want to create some private command pages, how?**

A: You can contribute to [tldr-pages/tldr](https://github.com/tldr-pages/tldr), or create your own Git repo, or just create a private directory, and add it to `repo_directory_list`.

**Q: I don't like the default color theme, how to change it?**

A: Edit the configuration file, modify the color until you're happy with it.

**Q: I faided to update the tldr pages, why?**

A: Actually, This program just tries to pull the latest tldr pages for you, no magic behinds it. So the reason why you faided to update is that this program failed to pull the latest upstream, check the failing output and you may know the reason, e.g. you make some changes and haven't commit them yet. You can pull the pages by hand so you can have a better control on it.

**Q: Why use `git`, instead of download assets packaged by the official?**

A: In fact, you can use the offical assets if you want, download the assets and extract it somewhere, but this program don't support update it using `tldr --update`.

By using `git`, we can:

- make this program simple but powerful, and easy to understand and control.
- do the version control, yeah, use `git`.
- easily maintain private repos.

**Q: How to auto update tldr pages?**

A: This program will neither update tldr pages when loop up a command, nor create a daemon or service to update tldr pages periodically. Updating is totally up to you. You can run `tldr --update` manually at any time you want, or use `crontab`, Windows `Task Scheduler` or any tool else to automatically update.

## Contributing

It sucks? Want a new feature? Find a bug?

Please open an issue, and let me know the bad things and your opinion. After our discussion, a pull request is welcomed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for the full license text.
