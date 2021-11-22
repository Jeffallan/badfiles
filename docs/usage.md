### Quickstart

The Badfile class provides one public method called `is_badfile` which analyzes a file.

There is also a convenance method called `isolate_or_clear` to help the developer handle the file in question.

Their usage is demonstrated below:

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
The safe parameter is a list of badfile classifications, returned from is_badfile(), that are deemed safe (defaults to ["safe",]). If the classification in the msg parameter is in the safe list the file is moved to safe_dir otherwise it is moved to iso_dir.
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
