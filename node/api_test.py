#!/usr/bin/env python3
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

import sys
if sys.version_info < (3, 0):
    sys.stdout.write("Node requires Python 3.x\n")
    sys.exit(1)

import nxtapi

account_id = 828683301869051229
secret_phrase = "aaa"

#account_id = int(sys.argv[1])
#secret_phrase = sys.argv[2]

api = nxtapi.Nxt()
#print(api.get_last_block().block_id)

account = api.get_account(account_id, secret_phrase)

tx = account.send_money_tx(17211701776878284146, 100000000)
print(tx.transaction_id)
tx_id = tx.send()
print(api.does_tx_exist(tx.transaction_id))
'''
account.start_forging()
account.send_money(17211701776878284146, 100000000)
print(api.get_state())
print(api.get_last_block().block_id)
'''
