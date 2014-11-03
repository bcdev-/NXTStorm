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

import json
import requests

TIMEOUT = None

class SendMoneyTx:
    def __init__(self, nxt, account, recipient, amountNQT, pubkey=None, feeNQT=100000000, deadline=900):
        self._nxt = nxt
        self._account = account
        self._recipient = str(int(recipient))
        self._amountNQT = str(int(amountNQT))
        self._feeNQT = str(int(feeNQT))
        #TODO Pubkey
        self._deadline = str(int(deadline))
        self._pubkey = pubkey
        self._prepare()

    def _prepare(self):
        url = ("http://" + self._nxt.host + "/nxt?requestType=" + "sendMoney" + "&secretPhrase=" + self._account.secret_phrase
            + "&recipient=" + self._recipient + "&amountNQT=" + self._amountNQT + "&feeNQT=" + self._feeNQT + "&deadline=" + self._deadline
            + "&broadcast=false")
        if self._pubkey != None:
            url += "&recipientPublicKey=" + self._pubkey
        #TODO: Error handling
        r = requests.post(url, timeout=TIMEOUT)
        response = json.loads(r.text)
        if not 'transactionBytes' in response:
            print('ERROR ' + url + ' ' + str(response))
        self._transaction_bytes = response['transactionBytes']
        self.transaction_id = int(response['transaction'])

    def send(self):
        url = "http://" + self._nxt.host + "/nxt?requestType=" + "broadcastTransaction" + "&transactionBytes=" + str(self._transaction_bytes)
        r = requests.post(url, timeout=TIMEOUT)
        response = json.loads(r.text)

