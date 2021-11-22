## Generally Suspicious Files

### Mime Type Confusion

Also known as mime type mismatch. This occurs when a file extension suggests one file type when it is actually another. An example of an attack using this principal can be found [here](https://capec.mitre.org/data/definitions/209.html).

This can be detected by comparing the expected mime type derived from the file extension and the actual file type by inspecting the [magic bytes](https://en.wikipedia.org/wiki/List_of_file_signatures) of the file using the [`_mime_type_confusion`](https://github.com/Jeffallan/badfiles/blob/a17263a5e6fd0312a01c17b33f364f86510105f0/badfiles/badfiles.py#L109) function.


### Files With a Root UID or GID or Sticky, Setuid, or Setgid Bit (*NIX only)

Generally speaking, files that belong to the root user or root group are something we do not want to receive from a user especially if this file is also executable. This is also true for files with a setuid or set gid bit. Lastly, files with a sticky bit are flagged because this bit restricts file deletion to just the owner of the file.

Detection strategies for the above vary by file type. Mostly, this is accomplished with a custom [Yara rule](https://github.com/Jeffallan/badfiles/tree/main/badfiles/rules)

## CSV Files

### CSV Injection
[CSV injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/CSV%20Injection) occurs when a user chooses to open a CSV file in a program like Excel. While this attack vector is mitigated by the default settings in excel-like programs, these default settings vary from program to program. Additionally, an unsuspecting user can alter these settings; creating an unsafe environment. Furthermore, CSV injection payloads can be [obfuscated](https://blog.reversinglabs.com/blog/cvs-dde-exploits-and-obfuscation) to evade detection.

[Yara rules](https://github.com/Jeffallan/badfiles/blob/main/badfiles/rules/csv_rules.yara) seem to be the best solution for detecting these types of files

## Zip Files

### Symlink Attacks


### Zip Slip


### Nested Zip Bombs


### Flat Zip Bombs


## Office Documents

Office Documents (docx, xlsx, etc) use the zip file specification as the underlying file structure. Therefore all zip file rules are applied to office documents before ay further processing.

### DDE Injection

DDE (Dynamic Data Exchange) injection behaves almost identically to CSV injection. Their detection strategies, however, differ.

After the file passes the zip file detection rules, it is safe to unzip. When the file is unzipped we look for a folder called `ExternalLinks`. If that folder exists the file uses the DDE protocol should be considered unsafe. This detection measure is implemented in the [`find_dde` method](https://github.com/Jeffallan/badfiles/blob/a17263a5e6fd0312a01c17b33f364f86510105f0/badfiles/utils.py#L52)

## Tar Files

### Files With Absolute Paths
