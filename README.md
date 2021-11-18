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

At some point in time every developer needs to accept files from a third party. Since we do not have absolute control over these files they present a serious threat vector.

The aim of this project is to provide a flexible and expandable solution to triage these files so a developer can handle them accordingly.

## Features

Currently, this project focuses on detecting the following:

### Generally Suspicious Files:

:heavy_check_mark: Mime Type confusion.

### CSV Files
:heavy_check_mark: CSV Injection

### Office Documents
:heavy_check_mark: DDE injection

### Zip Files
:heavy_check_mark: Symlink attacks

:heavy_check_mark: Sticky, setuid, or setgit bit

:heavy_check_mark: Zip slips

:heavy_check_mark: Nested zip bombs

:heavy_check_mark: Flat zip bombs

:heavy_check_mark: Files with a root UID or GID (*NIX only)

### Tar Files
:heavy_check_mark: Files with a root UID or GID (*NIX only)

:heavy_check_mark: Sticky, setuid, or setgit bit

:black_square_button: Files with absolute paths (*Nix only)

### Additional Features
Please file an issue or a pull request especially if you have found or created malicious files that bypass these detection mechanisms.

## Getting Started

### Installation

This package can be installed with `pip install badfiles`. The package also provides a convenance script called `badfiles` that runs a cli version of the detection engine. The `badfiles` command has an an additional dependency,[Gooey](https://github.com/chriskiehl/Gooey). If you wish to use the `badfiles` script please install the additional dependency via `pip install badfiles[gui]`.

This project also requires Yara. Installation instructions can be found [here](https://yara.readthedocs.io/en/stable/gettingstarted.html). This project also relies on [python-magic](https://github.com/ahupp/python-magic) which may require additional installation steps depending on your operating system.

### Quickstart

The Badfile class provides one public method called `is_badfile` which analyzes a file.

There is also a convenance method called `isolate_or_clear` to help the developer handle the file in question.

Their usage is demonstated below:

```python

from badfiles.badfiles import Badfiles, isolate_or_clear

b = Badfile()

bad = b.is_badfile(f=file)

"""
returns a named tuple with a classification: (safe, unsafe, unknown, or not implemented)
                            message: A message explaining the classification
                            file: The name of the file in the is_badfile function
"""

isolate_or_clear(f=file, msg=bad, iso_dir=iso_dir, safe_dir=safe_dir, safe=["safe",])
"""
The `safe` parameter is a list of badfile classifications (returned from is_badfile()) that are deemed safe (defaults to ["safe",]). If the classification in the parameter `bad` is in the safe list the file is moved to `safe_dir` otherwise it is moved to `iso_dir`.
"""

```
### Custom Yara Rules

A user may provide custom Yara detection rules upon class instantiation like so:

```python

from badfiles.badfiles import Badfiles, isolate_or_clear

b = Badfile(zip_rules="/path/to/rules", tar_rules="/path/to/rules", csv_rules="/path/to/rules")

bad = b.is_badfile(f=file)
```

### Project Integration

The aim of this library is to use it in larger projects and especially web applications. Here are a few ideas for how you can integrate `badfiles` into your current projects.

#### Fast API


```python
import pathlib
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from badfiles.badfiles import Badfile
import pathlib

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the badfiles demo"}

@app.post("/")
async def post_file(f: UploadFile = File(...)):
    upload = pathlib.Path(__file__).parent / "uploads" / f.filename
    with open(upload, "wb+") as fo:
        fo.write(f.file.read())
    b = Badfile()
    bf = b.is_badfile(upload)
    pathlib.Path.unlink(upload) # in real life you will not want to delete the file at this point
    if bf.classification == "safe":
        # handle safe files here
        return JSONResponse(status_code=200,
            content={"message": f"File accepted: {bf.message}"})
    # handle unsafe files here
    return JSONResponse(status_code=403,
        content={"message": f"File rejected: {bf.message}"})
```

#### Django

//TODO

## Credits

This package was created with [This Cookiecutter template.](https://github.com/zillionare/cookiecutter-pypackage)

This project uses [zip-bomb](https://github.com/damianrusinek/zip-bomb) to create the nested and flat zip bombs for unit testing and detection.

### Contributors

<a href = "https://github.com/jeffallan/badfiles/graphs/contributors">
<img src = "https://contrib.rocks/image?repo=jeffallan/badfiles"/>
