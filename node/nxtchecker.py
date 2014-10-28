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
import subprocess
import config
import nxtapi
import time
import requests
import traceback

class NxtChecker:
    def __init__(self, node):
        self.node = node
        self.logger = logging.getLogger(__name__)
        self.newest_block_id = 0

    def _check_for_new_block(self):
        api = nxtapi.Nxt()
        block = api.get_last_block()
        if block.block_id != self.newest_block_id:
            self.newest_block_id = block.block_id
            self.node.nxtchecker_new_block(block.block_id, block.height, block.transactions)

    def _is_api_ready(self):
        try:
            api = nxtapi.Nxt()
            state = api.get_state()

            self.node.nxtchecker_api_is_ready()
        except ConnectionRefusedError:
            pass
        except requests.exceptions.ConnectionError:
            pass

    def _periodic_tasks(self):
        try:
            self._check_for_new_block()
        except requests.exceptions.ConnectionError:
            pass
        except Exception as e:
            #TODO: message
            self.logger.error(traceback.format_exc())

    def run(self):
        self.logger.info("Started")
        while True:
            if not self.node.nxt_api_is_ready.value:
                self._is_api_ready()
            else:
                self._periodic_tasks()
            time.sleep(0.05)

