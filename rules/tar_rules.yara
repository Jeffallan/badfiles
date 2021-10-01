rule tar_owner : Tar
{
    meta:
        name = "Tar Owner is Root"
        created = "09/22/21"
        description = "This tar file was created by a user with the uid 1000 (root)."
        version = "1"

    strings:
        //$is_symlink = { 50 4B 01 02 [37] A?}

    condition:
        //$is_symlink
}

rule tar_group : Tar
{
    meta:
        name = "Tar Group is Root"
        created = "09/22/21"
        description = "This tar file was created by a user with the gid 1000 (root)."
        version = "1"

    strings:
        //$is_symlink = { 50 4B 01 02 [37] A?}

    condition:
        //$is_symlink

rule tar_path_naming : Tar
{
    meta:
        name = "Tar with absolute path"  // ./ not . or /
        created = "09/22/21"
        description = "This tar file is named with an absolute file path."
        version = "1"

    strings:
        //$is_symlink = { 50 4B 01 02 [37] A?}

    condition:
        //$is_symlink

rule tar_permissions : Tar
{
    meta:
        name = "Tar with executable files"  //file permissions of 7 and not dir
        created = "09/22/21"
        description = "This tar file contains executable files."
        version = "1"

    strings:
        //$is_symlink = { 50 4B 01 02 [37] A?}

    condition:
        //$is_symlink

rule tar_device : Tar
{
    meta:
        name = "Tar with socket"  //tared device socket no named pipe for now (fifo)
        created = "09/22/21"
        description = "This tar file contains a socket."
        version = "1"

    strings:
        //$is_symlink = { 50 4B 01 02 [37] A?}

    condition:
        //$is_symlink
