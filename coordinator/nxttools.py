'''
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004

Copyright (C) 2014 bcdev <nxt@bcdev.net>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.
'''

import subprocess

def id_from_secret(secret_phrase):
    return int(subprocess.check_output(["./id_from_pass", secret_phrase]))

def pubkey_from_secret(secret_phrase):
    return str(subprocess.check_output(["./pubkey_from_pass", secret_phrase]), 'ascii')

