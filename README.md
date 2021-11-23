# badfiles


<p align="center">
<a href="https://pypi.python.org/pypi/badfiles">
    <img src="https://img.shields.io/pypi/v/badfiles.svg"
        alt = "Release Status">
</a>

<a href="https://github.com/jeffallan/badfiles/actions">
    <img src="https://github.com/jeffallan/badfiles/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">
</a>

<!--
<a href="https://jeffallan.github.io/badfiles/">
    <img src="https://jeffallan.github.io/badfiles/badge/?version=latest" alt="Documentation Status">
</a>
-->
<!--
<a href="https://pyup.io/repos/github/jeffallan/badfiles/">
<img src="https://pyup.io/repos/github/jeffallan/badfiles/shield.svg" alt="Updates">
</a>
-->
</p>


A malicious file detection engine written with Python and Yara.


* Free software: Apache-2.0
* Documentation: <https://jeffallan.github.io/badfiles/>

## Introduction

At some point most applications need to accept files from a third party. Since we do not have absolute control over these files they can present a serious threat vector.

The aim of this project is to provide a flexible and expandable solution to triage these files so they can be handled accordingly.

## Features

Currently, this project focuses on detecting the following:

### Generally Suspicious Files:

:heavy_check_mark: Mime type confusion.

:black_square_button: Files with a root UID or GID (*NIX only).

:black_square_button: Sticky, setuid, or setgit bit (*NIX only).

### CSV Files
:heavy_check_mark: CSV Injection.

:black_square_button: Files with a root UID or GID (*NIX only).

:black_square_button: Sticky, setuid, or setgit bit (*NIX only).

### Office Documents
:heavy_check_mark: DDE injection.

:heavy_check_mark: Files with a root UID or GID (*NIX only).

:heavy_check_mark: Sticky, setuid, or setgit bit (*NIX only).

### Zip Files
:heavy_check_mark: Symlink attacks.

:heavy_check_mark: Zip slips.

:heavy_check_mark: Nested zip bombs.

:heavy_check_mark: Flat zip bombs.

:heavy_check_mark: Sticky, setuid, or setgit bit (*NIX only).

:heavy_check_mark: Files with a root UID or GID (*NIX only).

### Tar Files
:heavy_check_mark: Files with a root UID or GID (*NIX only).

:heavy_check_mark: Sticky, setuid, or setgit bit (*NIX only).

:black_square_button: Files with absolute paths (*Nix only).



### Additional Features
Please file an issue or a pull request especially if you have found or created malicious files that bypass these detection mechanisms. Please see the [contributing guidelines](https://jeffallan.github.io/badfiles/contributing/) for more details.

## [Getting Started](https://jeffallan.github.io/badfiles/installation/)

## [Usage](https://jeffallan.github.io/badfiles/usage/)

## Credits

This package was created with [This Cookiecutter template.](https://github.com/zillionare/cookiecutter-pypackage)

This project uses [zip-bomb](https://github.com/damianrusinek/zip-bomb) to create the nested and flat zip bombs for unit testing and detection rules.

This project uses a custom Yara rule from [Reversing Labs](https://blog.reversinglabs.com/blog/cvs-dde-exploits-and-obfuscation) to detect obfuscated CSV injection payloads.

### Contributors

<a href = "https://github.com/jeffallan/badfiles/graphs/contributors">
<img src = "https://contrib.rocks/image?repo=jeffallan/badfiles"/>
