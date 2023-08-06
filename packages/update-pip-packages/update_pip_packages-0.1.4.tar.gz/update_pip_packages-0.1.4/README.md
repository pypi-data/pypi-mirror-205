# Update Pip and App Packages

## v0.1.4

![Python application](https://github.com/OleksandrMakarov/update-pip-project/actions/workflows/python-app.yml/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/af2bad1ec28de4bea881/maintainability)](https://codeclimate.com/github/OleksandrMakarov/update-pip-project/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/af2bad1ec28de4bea881/test_coverage)](https://codeclimate.com/github/OleksandrMakarov/update-pip-project/test_coverage)

This Python script provides an efficient way to update Pip and app packages on various Linux distributions. The script supports Ubuntu, Debian, Fedora, CentOS, Red Hat, Arch, Manjaro, OpenSUSE, and SUSE distributions. It updates packages using the appropriate package manager for each distribution.

**I know this script may seem useless. Moreover, updating all pip packages can lead to challenges in some projects.
This script is only a part of my self-education journey.**

## Features

- Update Pip and its packages to the latest versions.
- Update app packages for supported Linux distributions using the corresponding package manager.
- Command-line interface with options for updating Pip packages, app packages, or both.

## Usage

To use the script, run the following command with the desired options:

```bash
update-pip-packages [--pip] [--app]
```
- -h, --help: Show this help message and exit
- --pip: Update Pip packages.
- --app: Update app packages.
- -v, --version: Display the version of the package
- If no options are provided, the script will display help information.

## Tests
The tests cover various aspects of the script, including the following:

- Getting the Linux distribution.
- Updating Pip packages.
- Updating app packages for each supported Linux distribution.
- Handling unsupported Linux distributions.



## Dependencies
- [Python](https://www.python.org/) 3.6 or later
- [Poetry](https://python-poetry.org/)
- [pytest](https://pytest.org/)
- [distro](https://pypi.org/project/distro/)
- [toml](https://pypi.org/project/toml/)

## Installation
From [PyPi.org](https://pypi.org/project/update-pip-packages/)

In Linux:
```
pip install update-pip-packages
```
or
```
python3 -m pip install update-pip-packages
```

## GitHub Repository
For more information, source code, and installation instructions, please visit the GitHub repository: [GitHub: update-pip-packages](https://github.com/OleksandrMakarov/update-pip-project)

## Remarks
There is also a [bash script](https://github.com/OleksandrMakarov/update-pip-project/blob/main/update_packages.sh). I started with it and developed it into this Python project. 
It does not support Linux distribution detection, but you can use it for the same purposes as the main(python) application in a Debian or Ubuntu environment.
