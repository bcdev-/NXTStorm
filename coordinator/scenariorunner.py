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

import logging
import time
import nxttools

scenario_list = []

NQT = 100000000
TOTAL_NXT = 999999000
NODES = 1
TPS = 5
SEND_TX_INTERVAL = 1. / TPS
BLOCKCHAIN_PREPARE_COOLDOWN = 10

class ScenarioRunner:
    def __init__(self, coordinator):
        self.logger = logging.getLogger(__name__)
        self.coordinator = coordinator
        self.scenario = None
        self.progress = None
        self.scenario_start = time.time()
        self.tx_sent = 0
        self.funds_distributed = False

    def _start_node(self, node):
#        node.start_nxt()
#        for account in node.accounts:
#            node.start_forging(account[1], account[0])
        node.scenario_progress = {'started': True, 'start_time': time.time()}

    def _distribute_funds(self):
        if len(self.coordinator.nodes) == 0:
            return False
        node = self.coordinator.nodes[0]
#        node.start_nxt()
        for i in range(TPS):
            secret_phrase = "%.4dx%.4d" % (0, i)
            account_id = nxttools.id_from_secret(secret_phrase)
            pubkey = nxttools.pubkey_from_secret(secret_phrase)
            node.add_account(account_id, secret_phrase, pubkey)
            node.send_money(account_id, int(3600 * NQT), "aaa", pubkey)
#            node.send_money(account_id, int((TOTAL_NXT / TPS - 1) * NQT), "aaa", pubkey)
        time.sleep(3)
        node.start_forging("aaa", nxttools.id_from_secret("aaa"))
        self.logger.info(str(node.accounts))
        return True

    def _send_money(self, node):
        if self.time > SEND_TX_INTERVAL * self.tx_sent:
            account = node.accounts[node.account_revolver]
            node.send_money(17211701776878284146, 100000000, account[1])
            node.account_revolver += 1
            node.account_revolver %= len(node.accounts)
            self.tx_sent += 1

    def _tick_node(self, node):
        if node.scenario_progress == None:
            self._start_node(node)
        elif node.scenario_progress['started'] == True:
            self._send_money(node)

    def run(self):
        self.logger.info("Started")
        while not self._distribute_funds(): pass
        self.scenario_start = time.time()
        while True:
            time.sleep(0.01)
            self.time = time.time() - self.scenario_start - BLOCKCHAIN_PREPARE_COOLDOWN
            if self.time < 0:
                self.time = 0
            for node in self.coordinator.nodes:
                self._tick_node(node)
            

