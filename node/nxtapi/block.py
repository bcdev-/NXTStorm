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

import requests
import json

class Block:
    def __init__(self, nxt, block_id):
        self._nxt = nxt
        self.block_id = int(block_id)
        self._get_block()

    def _get_block(self):
        url = "http://" + self._nxt.host + "/nxt?requestType=" + "getBlock" + "&block=" + str(self.block_id)
        #TODO: Api error handling - create "nxt invalid response" exception
        r = requests.post(url)
        data = json.loads(r.text)
        self.height = data['height']
        self.number_of_transactions = data['numberOfTransactions']
        self.transactions = data['transactions']
        pass

