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

from .send_money_tx import SendMoneyTx

class Account:
    def __init__(self, nxt, account_id, secret_phrase):
        self._nxt = nxt
        #TODO What if account_id == None?
        self.account_id = account_id
        self.secret_phrase = secret_phrase

    def start_forging(self):
        url = "http://" + self._nxt.host + "/nxt?requestType=" + "startForging" + "&secretPhrase=" + self.secret_phrase
        #TODO: Error handling
        r = requests.post(url)

    def get_forging(self):
        url = "http://" + self._nxt.host + "/nxt?requestType=" + "getForging" + "&secretPhrase=" + self.secret_phrase
        #TODO: Error handling
        r = requests.post(url)
        return json.loads(r.text)

    def send_money(self, recipient, amountNQT, feeNQT = 100000000, deadline = 1440):
        url = ("http://" + self._nxt.host + "/nxt?requestType=" + "sendMoney" + "&secretPhrase=" + self.secret_phrase +
            "&recipient=" + str(int(recipient)) + "&amountNQT=" + str(int(amountNQT)) + "&feeNQT=" + str(int(feeNQT)) + "&deadline=" + str(int(deadline)))
        #TODO: Error handling
        r = requests.post(url)

    def send_money_tx(self, recipient, amountNQT):
        return SendMoneyTx(self._nxt, self, recipient, amountNQT)
