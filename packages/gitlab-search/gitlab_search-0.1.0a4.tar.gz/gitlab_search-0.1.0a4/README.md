# gitlab-search

Command line tool for searching for text terms across several GitLab(TM) projects

[![release](https://img.shields.io/pypi/v/gitlab-search?label=release)](https://pypi.org/project/gitlab-search/)
[![python](https://img.shields.io/pypi/pyversions/gitlab-search)](https://pypi.org/project/gitlab-search/)
[![pipeline status](https://gitlab.com/ErikKalkoken/gitlab-search/badges/main/pipeline.svg)](https://gitlab.com/ErikKalkoken/gitlab-search/-/commits/main)
[![license](https://img.shields.io/badge/license-MIT-green)](https://gitlab.com/ErikKalkoken/gitlab-search/-/blob/master/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![chat](https://img.shields.io/discord/790364535294132234)](https://discord.gg/zmh52wnfvM)

## Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Description

This tool let's you perform a full text search across your personal projects, your group projects and/or public projects of any user on GitLab (TM).

GITLAB is a trademark of GitLab Inc. in the United States and other countries and regions

>**Note**: This is not an official tool from GitLab and the author has no affiliation with GitLab Inc.

## Features

- Search for occurrences of a text term across all files of all projects known to a user
- Matches are given with exact location and link to file on GitLab
- Search personal projects and group projects
- Search public projects of other users
- Limit search to personal projects or groups
- Exclude specific projects from search
- Limit search to files with specific extensions
- Search for several terms in the same run
- Works with custom gitlab domain

## Installation

You can install this tool from PyPI with the following command:

```bash
pip install gitlab-search
```

## Usage

To use this tool you need a private API token, which you can create on the GitHub profile page.

To run a search over all your projects for the term `kalkoken` you can enter:

```bash
github-search kalkoken
```

> **Note**: The tool will search all personal projects and known group projects by default. You can change the scope of what projects are searches through command line arguments.

When you start the command for the first time it will run setup, e.g. to configure your token. The configuration will be saved and re-used the next time you use the command. If you want to update your configuration your can setup again any time list this:

```bash
github-search --setup
```

> **Hint**: gitlab-search will store the configuration in the home directory of the current user in the file `.gitlabsearch`.

You can get a full overview of the command syntax with:

```bash
github-search -h
```
