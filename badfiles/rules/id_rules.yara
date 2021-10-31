rule is_zip
{
    meta:
        name = "Is zip file"
        description = "A rule stating a file contians the magic bytes 50 4B 03 04"
        created = "09/01/21"
        version = "1"
    strings:
        $magic = { 50 4B 03 04 }
    condition:
        #magic==1
}

rule is_tar
{
    meta:
        name = "Is tarfile"
        description = "A rule stating a file contians the magic bytes 75 73 74 61 72 20 20 00"
        created = "09/01/21"
        version = "1"
    strings:
        $magic = { ?? [255] 75 73 74 61 72 20 20 00 }
    condition:
        $magic
}
