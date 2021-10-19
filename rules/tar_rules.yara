rule tar_owner : Tar
{
    meta:
        name = "Tar Owner is Root"
        created = "09/22/21"
        description = "This tar file was created by a user with the uid 0 (root)."
        version = "1"

    strings:
        $file = { ?? [110] 30 30 30 30 }
        $tar = { 00 75 73 74 61 72 20 20 00 72 6F 6F 74 00 }
    condition:
        $file and $tar
}

rule tar_group : Tar
{
    meta:
        name = "Tar Group is Root"
        created = "09/22/21"
        description = "This tar file was created by a user with the gid 0 (root)."
        version = "1"

    strings:
        $file = { ?? [118] 30 30 30 30 }
        $tar = { 00 75 73 74 61 72 20 20 00 [31] 72 6F 6F 74 00 }
    condition:
        $file and $tar
}
rule tar_bad_bits : Tar
{
    meta:
        name = "Tar with bad bits"
        created = "09/22/21"
        description = "This tar file contains a sticky, setuid, or setgit bit."
        version = "1"

    strings:
        $val = { ?? [101] (31|32|33|34|35|36|37)}

    condition:
        $val
}
rule tar_permissions : Tar
{
    meta:
        name = "Tar with executable files"  //file are odd and not dir
        created = "09/22/21"
        description = "This tar file contains executable files."
        version = "1"

    strings:
        $owner_perms = { ?? [102] (31|33|35|37)}
        $group_perms = { ?? [104] (31|33|35|37)}
        $global_perms = { ?? [102] (31|33|35|37)}
        $dir = { ?? [154] 35}
    condition:
        $owner_perms or $group_perms or $global_perms and not $dir
}
rule tar_device : Tar
{
    meta:
        name = "Tar with socket"  //tared device socket
        created = "09/22/21"
        description = "This tar file contains a socket."
        version = "1"

    strings:
        $val = { ?? [154] (31|34)}

    condition:
        $val
}
/*
https://docstore.mik.ua/orelly/unix3/upt/ch38_11.htm
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
*/
