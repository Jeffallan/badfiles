## Generally Suspicious Files

### Mime Type Confusion

Also known as mime type mismatch. This occurs when a file extension suggests one file type when it is actually another. An example of an attack using this principal can be found [here](https://capec.mitre.org/data/definitions/209.html).

Mime type confusion is detected by comparing the expected mime type derived from the file extension and the actual file type by inspecting the [magic bytes](https://en.wikipedia.org/wiki/List_of_file_signatures) of the file using the [`_mime_type_confusion`](https://github.com/Jeffallan/badfiles/blob/a17263a5e6fd0312a01c17b33f364f86510105f0/badfiles/badfiles.py#L109) function.


### Files With a Root UID or GID or Sticky, Setuid, or Setgid Bit (*NIX only)

Generally speaking, files that belong to the root user or root group are something we do not want to receive from a user especially if this file is also executable. This is also true for files with a setuid or set gid bit because they can be used to escalade privilege. Lastly, files with a sticky bit are flagged because this bit restricts file deletion to just the owner of the file.

Detection strategies for the above vary by file type. Mostly, this is accomplished with a custom [Yara rule](https://github.com/Jeffallan/badfiles/tree/main/badfiles/rules)

## CSV Files

### CSV Injection
[CSV injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/CSV%20Injection) occurs when a user chooses to open a CSV file in a program like Excel. While this attack vector is mitigated by the default settings in excel-like programs, these default settings vary from program to program. Additionally, an unsuspecting user can alter these settings; creating an unsafe environment. Furthermore, CSV injection payloads can be [obfuscated](https://blog.reversinglabs.com/blog/cvs-dde-exploits-and-obfuscation) to evade conventional detection methods.

This [Yara rule](https://github.com/Jeffallan/badfiles/blob/main/badfiles/rules/csv_rules.yara) is used for detecting these types of files

## Zip Files

### Symlink Attacks

A [symlink attack](https://security.stackexchange.com/questions/73718/how-zip-symlink-works) works by creating a symlink to a target file like `/etc/passwd` and masking it with an arbitrary filename like `safe_upload.jpg` if this file is unzipped, any user that has the correct permissions for the target file can access it through the symlink.

Symlinks attacks are detected with a Yara [rule](https://github.com/Jeffallan/badfiles/blob/a17263a5e6fd0312a01c17b33f364f86510105f0/badfiles/rules/zip_rules.yara#L1) that checks for a symlink bit in the central file header (`0x504B0102`)

### Zip Slip

A [zip slip](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/ba2c02cc3ef3f63df6351aa55509bdac137fb3b8/Upload%20Insecure%20Files/Zip%20Slip/README.md) occurs when a zip file contains a name with a [directory traversal](https://portswigger.net/web-security/file-path-traversal) build in (../../malicious_file.zip) which can lead to content being uploaded to unintended locations.

Zip slips are [detected](https://github.com/Jeffallan/badfiles/blob/a17263a5e6fd0312a01c17b33f364f86510105f0/badfiles/rules/zip_rules.yara#L60) by navigating to the central file header in the zip archive (`0x504B0102`) and searching for `../` at the beginning of the file name.

### Zip Bombs

Zip Bombs come in two varieties nested and flat. In each case when this malicious file is unzipped it creates an extremely large file potentially causing a denial of service due to a lack of disk space on the server.

#### Nested Zip Bombs

A nested zip bomb is a zip file that contains other zip files.

This type of zip bomb is [detected](https://github.com/Jeffallan/badfiles/blob/a17263a5e6fd0312a01c17b33f364f86510105f0/badfiles/rules/zip_rules.yara#L74) by navigating to every local file header (`0x504B0304`) and searching for the string `.zip`

#### Flat Zip Bombs

Flat zip bombs are zip archives that are constructed in such a way that their compression rates are much higher than a normal zip files whose compression rates range from about 60%-70% (**citation needed**).

To detect flat zip bombs one must investigate the compression rate of the zip archive. This is implemented in the [`_high_compression` method](https://github.com/Jeffallan/badfiles/blob/a17263a5e6fd0312a01c17b33f364f86510105f0/badfiles/badfiles.py#L148)

## Office Documents

Office Documents (docx, xlsx, etc) use the zip file specification as the underlying file structure. Therefore, all zip file rules are applied to office documents before any further processing.

### DDE Injection

DDE (Dynamic Data Exchange) injection behaves almost identically to CSV injection. The detection strategy is, however, different.

After the file passes the zip file detection rules, it is safe to [unzip](https://github.com/Jeffallan/badfiles/blob/a17263a5e6fd0312a01c17b33f364f86510105f0/badfiles/utils.py#L70). When the file is unzipped we look for a folder called `externalLinks`. If that folder exists the file uses the DDE protocol should be considered unsafe. This detection measure is implemented in the [`find_dde` method](https://github.com/Jeffallan/badfiles/blob/a17263a5e6fd0312a01c17b33f364f86510105f0/badfiles/utils.py#L52)

## Tar Files

### Files With Absolute Paths

If a tar file contains a file with an absolute path, it will overwrite the file at that location if user who untars the file has the correct permissions.

There are numerous targets a threat actor would be interested in including:

* /etc/passwd
* .bashrc
* .bash_aliases

This detection mechanism has yet to be implemented.
