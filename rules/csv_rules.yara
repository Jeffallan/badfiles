rule obfuscated_dde : CSV
{
    meta:
        name = "Obfuscated CSV Injection"
        created = "10/27/21"
        description = "This file contains a dde payload"
        version = "1"

    strings:

        $dde_command = /[=+-]+[ 0-9A-Za-z_\"\&\^\-\=\/\+\(\x00]*(((c|C)[\x00]*(m|M)[\x00]*(d|D)[\x00]*\|)|((m|M)[\x00]*(s|S)[\x00]*(i|I|e|E)[\x00]*(e|E|x|X)[\x00]*(x|X|c|C)[\x00]*(e|E)[\x00]*(c|C|l|L)[\x00]*\|)|((r|R)[\x00]*(u|U|e|E)[\x00]*(n|N|g|G)[\x00]*(d|D|s|S)[\x00]*(l|L|v|V)[\x00]*(l|L|r|R)[\x00]*3[\x00]*2[0-9A-Za-z\x00]*\|)|((c|C)[\x00]*(e|E)[\x00]*(r|R)[\x00]*(t|T)[\x00]*(u|U)[\x00]*(t|T)[\x00]*(i|I)[\x00]*(l|L)[0-9A-Za-z\x00]*\|))[\x00]*\'/

    condition:
        $dde_command
}
