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

from .account import Account
from .block import Block

import json
import requests

class Nxt:
    def __init__(self, host='localhost:7876'):
        self.host = host

    def get_account(self, account_id, secret_phrase=None):
        return Account(self, account_id, secret_phrase)

    def get_state(self):
        url = "http://" + self.host + "/nxt?requestType=getState"
        #TODO: Error handling
        r = requests.get(url)
        return json.loads(r.text)

    def get_last_block(self):
        last_block_id = self.get_state()["lastBlock"]
        return self.get_block(last_block_id)

    def get_block(self, block_id):
        return Block(self, block_id)

    def get_tx(self, transaction_id):
        url = "http://" + self.host + "/nxt?requestType=getTransaction" + "&transaction=" + str(transaction_id)
        #TODO: Error handling
        r = requests.get(url)
        return json.loads(r.text)

    def does_tx_exist(self, transaction_id):
        status = self.get_tx(transaction_id)
        if 'transaction' in status:
            return True
        return False

