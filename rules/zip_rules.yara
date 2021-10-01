rule zip_symlink : Zip
{
    meta:
        name = "Symlink Zip"
        created = "09/01/21"
        description = "This zip file contains a symlink."
        version = "1"

    strings:
        $is_symlink = { 50 4B 01 02 [37] A?}

    condition:
        $is_symlink
}

rule zip_bad_bits : Zip
{
    meta:
        name = "Zip with bad bits"
        created = "09/01/21"
        description = "This zip file contains a sticky, setuid, or setgit bit."
        version = "1"

    strings:
        $bad_bits = { 50 4B 01 02 [37] (82|83|84|85|86|87|88|89|8A|8B|8C|8D|8E|8F)}

    condition:
        $bad_bits
}
/*
rule zip_setuid : Zip
{
    meta:
        name = "Setuid Zip"
        created = "09/01/21"
        description = "This zip file contains a setuid bit."
        version = "1"

    strings:
        $is_uid = { 50 4B 01 02 [37] (88 | 89) }

    condition:
        $is_uid
}
rule zip_setgid : Zip
{
    meta:
        name = "Setgid Zip"
        created = "09/01/21"
        description = "This zip file contains a setgid bit."
        version = "1"

    strings:
        $is_uid = { 50 4B 01 02 [37] (85 | 84) }

    condition:
        $is_uid
}
*/
rule zip_slip : Zip
{
    meta:
        name = "Zip Slip"
        created = "09/01/21"
        description = "This zip file contains a zip slip."
        version = "1"

    strings:
        $is_slip = { 50 4B 01 02 [42] 2E 2E 2F}

    condition:
        $is_slip
}
rule nested_zip_bomb : Zip
{
    meta:
        name = "Nested Zip Bomb"
        created = "09/01/21"
        description = "This zip file contains a nested zip bomb."
        version = "1"

    strings:
        $is_bomb = ".zip"
        $magic = { 50 4B 03 04 }
    condition:
        $is_bomb and $magic
}
