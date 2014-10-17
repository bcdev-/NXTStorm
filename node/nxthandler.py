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

class NxtHandler:
    def __init__(self, node):
        self.node = node
        self.logger = logging.getLogger(__name__)

    def _start_nxt_client(self):
        self._stop_nxt_client()
        self.logger.info("Starting NXT client")
        self.nxt_client = subprocess.Popen(config.nxt_start_command, shell=True, stderr=subprocess.STDOUT, stdout = subprocess.PIPE)
        #TODO: Log handling in another thread
#        while True:
#            print(self.nxt_client.stdout.readline())

    def _stop_nxt_client(self):
        self.logger.info("Stopping NXT client")
        nxt_killer = subprocess.call(config.nxt_stop_command, shell=True, stderr=subprocess.STDOUT, stdout = subprocess.PIPE)

    def _start_forging(self, account_id, secret_phrase):
        self.logger.info("Starting to forge")
        api = nxtapi.Nxt()
        account = api.get_account(account_id, secret_phrase)
        account.start_forging()

    def _handle_command(self, command):
        self.logger.debug("Handling command: " + command.name)
        if command.command_type == command.START_NXT:
            self._start_nxt_client()
        elif command.command_type == command.STOP_NXT:
            self._stop_nxt_client()
        elif command.command_type == command.START_FORGING:
            self._start_forging(command.account_id, command.secret_phrase)
        else:
            self.logger.error("Unknown command: " + str(command.command_type) + " " + str(command.name))

    def run(self):
        self.logger.info("Started")
        while True:
            if self.node.nxt_handler_commands.empty():
                time.sleep(0.001)
            else:
                #TODO: try except
                self._handle_command(self.node.nxt_handler_commands.get())

