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

scenario_list = []

TPS = 1
SEND_TX_INTERVAL = 1. / TPS
COOLDOWN = 4

class ScenarioRunner:
    def __init__(self, coordinator):
        self.logger = logging.getLogger(__name__)
        self.coordinator = coordinator
        self.scenario = None
        self.progress = None
        self.scenario_start = time.time()
        self.tx_sent = 0

    def _start_node(self, node):
        node.start_nxt()
        node.start_forging()
        node.scenario_progress = {'started': True, 'start_time': time.time()}

    def _send_money(self, node):
        if self.time > SEND_TX_INTERVAL * self.tx_sent:
            node.send_money(17211701776878284146, 100000000)
            self.tx_sent += 1

    def _tick_node(self, node):
        if node.scenario_progress == None:
            self._start_node(node)
        elif node.scenario_progress['started'] == True:
            self._send_money(node)

    def run(self):
        self.logger.info("Started")
        self.scenario_start = time.time()
        while True:
            time.sleep(0.01)
            self.time = time.time() - self.scenario_start - COOLDOWN
            if self.time < 0:
                self.time = 0
            for node in self.coordinator.nodes:
                self._tick_node(node)
            

