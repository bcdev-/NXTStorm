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

from multiprocessing import Queue, Process, Value
import logging
import traceback
import time

from nxthandler import NxtHandler
from nxtchecker import NxtChecker
from network import Network

from nxthandlercommand import NxtHandlerCommand
from networkcommand import NetworkCommand

logger = logging.getLogger(__name__)

def start_network_thread(nxt_handler):
    running = True
    while running:
        try:
            network = Network(nxt_handler)
            running = network.run()
        except Exception as ex:
            logger.error(traceback.format_exc())
            logger.error("Restarting Network")
            time.sleep(1)

def start_nxt_handler_thread(nxt_handler):
    running = True
    while running:
        try:
            nxt_handler = NxtHandler(nxt_handler)
            running = nxt_handler.run()
        except Exception as ex:
            logger.error(traceback.format_exc())
            logger.error("Restarting NxtHandler")
            time.sleep(1)

def start_nxt_checker_thread(nxt_handler):
    running = True
    while running:
        try:
            nxt_checker = NxtChecker(nxt_handler)
            running = nxt_checker.run()
        except Exception as ex:
            logger.error(traceback.format_exc())
            logger.error("Restarting NxtChecker")
            time.sleep(1)

class Node:
    def __init__(self):
        self.nxt_handler_thread = None
        self.nxt_handler_commands = Queue()
        self.nxt_handler_interrupts = Queue()
        self.network_commands = Queue()
        self.responses = Queue()
        self.logger = logging.getLogger(__name__)
        self.nxt_api_is_ready = Value('i', 0)

    def start(self):
        logging.info("Starting NxtHandler")
        self.nxt_handler = Process(target=start_nxt_handler_thread, args=(self,))
        self.nxt_handler.start()
        logging.info("Starting NxtChecker")
        self.nxt_checker = Process(target=start_nxt_checker_thread, args=(self,))
        self.nxt_checker.start()
        logging.info("Starting Network")
        self.network = Process(target=start_network_thread, args=(self,))
        self.network.start()

    def stop(self):
        logging.info("Stopping NxtHandler")
        #TODO

    def push_nxt_handler_command(self, command):
        self.nxt_handler_commands.put(command)

    def push_nxt_handler_interrupt(self, command):
        self.nxt_handler_interrupts.put(command)

    '''
    def start_nxt(self):
        self.nxt_handler_interrupts.put(NxtHandlerCommand.start_nxt())

    def start_forging(self, account_id, secret_phrase):
        #TODO account ID is redundant
        self.nxt_handler_commands.put(NxtHandlerCommand.start_forging(account_id, secret_phrase))

    def stop_nxt(self):
        self.nxt_handler_interrupts.put(NxtHandlerCommand.stop_nxt())

    def send_money(self, secret_phrase, recipient, amountNQT):
        self.nxt_handler_commands.put(NxtHandlerCommand.send_money(secret_phrase, recipient, amountNQT))
    '''

    #### Callbacks for NxtChecker ####
    def nxtchecker_new_block(self, block_id, height, transactions):
        # TODO: Backup buffer file
        self.logger.debug("Found new block: %d - %d - %s" % (height, block_id, str(transactions)))
        self.network_commands.put(NetworkCommand.new_block(block_id, height, transactions))

    def nxtchecker_api_is_ready(self):
        self.logger.info("Nxt API is ready")
        self.nxt_api_is_ready.value = 1

    #### Callbacks for Network ####
    def network_start_forging(self, account_id, secret_phrase):
        self.start_forging()

