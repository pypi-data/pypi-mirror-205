# Kireji

[![](https://img.shields.io/github/actions/workflow/status/wirehaiku/kireji/pytest.yml?style=flat-square)][test]
[![](https://img.shields.io/github/issues/wirehaiku/kireji?style=flat-square)][bugs]
[![](https://img.shields.io/pypi/pyversions/kireji?style=flat-square)][p310]
[![](https://img.shields.io/pypi/v/kireji?style=flat-square)][pypi]
[![](https://img.shields.io/github/license/wirehaiku/kireji?style=flat-square)][lcns]

Kireji is a command-line note manager written in [Python 3.10][p310] by [Stephen Malone][smal]. 
If you have a directory of plaintext note files you need to handle, Kireji can help you organise and manipulate them with ease.

- See [`changes.md`][chng] for a complete changelog.
- See [`license.md`][lcns] for licensing information (BSD-3).
- See the [issue tracker][bugs] for bugs and feature requests.

## Installation

You can install Kireji from [PyPi][pypi]...

```
pip install kireji
```

...or download the [latest release][rels] for your platform.

## Configuration

To use Kireji, you need to set two environment variables: `KIREJI_DIR` and `KIREJI_EXT`.

```bash
# The path to the directory your notes are in.
export KIREJI_DIR = "~/path/to/notes"

# The file extension your notes use.
export KIREJI_EXT = ".txt"
```

That's it! That's all the configuration you need.

## Commands

### Syntax

Notes are always referenced with lowercase hyphenated names. 
Asking Kireji to make a note called `My Note` will result in `my-note` being created.

All commands share these universal arguments:

- `-d` `--debug`: Print details about the current configuration and exit.
- `-h` `--help`:  Print help about one or all of Kireji's commands.
- `-f` `--force`: Force all `[Y/n]` safety prompts to yes.

### List all notes

Use `kireji list` to print the names of all existing notes, or only names matching a [glob pattern][glob].

```bash
$ kireji list
2023-roadmap
groceries
projects
  
$ kireji list "2023*"
2023-roadmap
```

To change the output format, use the `--mode` flag.
Choose between `comma`, `json`, `space` or `line` (the default).

```bash
$ kireji --mode=json
["2023-roadmap", "groceries", "projects"]
```

</details>

## Contributing

Please submit all feature requests and bug reports to the [issue tracker][bugs], thank you.

[bugs]: https://github.com/wirehaiku/kireji/issues
[chng]: https://github.com/wirehaiku/kireji/blob/main/changes.md
[glob]: https://en.wikipedia.org/wiki/Glob_(programming)
[lcns]: https://github.com/wirehaiku/kireji/blob/main/license.md
[p310]: https://python.org/downloads/release/python-3100/
[pypi]: https://pypi.org/project/kireji/
[rels]: https://github.com/wirehaiku/kireji/releases/latest
[smal]: https://wirehaiku.org/
[test]: https://github.com/wirehaiku/kireji/actions/workflows/pytest.yml
