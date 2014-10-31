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
import traceback

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
        self.node.nxt_api_is_ready.value = 0

    def _start_forging(self, account_id, secret_phrase):
        self.logger.info("Starting to forge")
        api = nxtapi.Nxt()
        account = api.get_account(account_id, secret_phrase)
        account.start_forging()

    def _send_money(self, recipient, secret_phrase, amountNQT):
        self.logger.info("Sending money")
        api = nxtapi.Nxt()
        account = api.get_account(None, secret_phrase)
        tx = account.send_money_tx(recipient, amountNQT)
        tx.send()
        self.logger.info("Done")

    def _handle_interrupt(self, command):
        self.logger.debug("Handling interrupt: " + command['name'])
        if command['name'] == 'start_nxt':
            self._start_nxt_client()
#        elif command.command_type == command.STOP_NXT:
#            self._stop_nxt_client()
        else:
            self.logger.error("Unknown interrupt: " + str(command))

    def _handle_command(self, command):
        self.logger.debug("Handling command: " + command['name'])
        if command['name'] == 'start_forging':
            self._start_forging(command['account_id'], command['secret_phrase'])
        if command['name'] == 'send_money':
            self._send_money(command['recipient'], command['secret_phrase'], command['amountNQT'])
        else:
            self.logger.error("Unknown command: " + str(command))

    def run(self):
        self.logger.info("Started")
        while True:
            #TODO: try except
            if not self.node.nxt_handler_interrupts.empty():
                try:
                    self._handle_interrupt(self.node.nxt_handler_interrupts.get())
                except Exception:
                    self.logger.error(traceback.format_exc())
            elif not self.node.nxt_handler_commands.empty() and self.node.nxt_api_is_ready.value:
                try:
                    self._handle_command(self.node.nxt_handler_commands.get())
                except Exception:
                    self.logger.error(traceback.format_exc())
            else:
                time.sleep(0.01)

