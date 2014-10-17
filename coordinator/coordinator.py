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
import traceback
import time
from multiprocessing import Queue, Process

from network import Network
from rawdatalogger import RawDataLogger

logger = logging.getLogger(__name__)

def start_network_thread(coordinator):
    running = True
    while running:
        try:
            network = Network(coordinator)
            running = network.run()
        except Exception as ex:
            logger.error(traceback.format_exc())
            logger.error("Restarting Network")
            time.sleep(1)

def start_raw_data_logger_thread(coordinator):
    running = True
    while running:
        try:
            raw_data_logger = RawDataLogger(coordinator)
            running = raw_data_logger.run()
        except Exception as ex:
            logger.error(traceback.format_exc())
            logger.error("Restarting RawDataLogger")
            time.sleep(1)

class Coordinator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.raw_data_logger_queue = Queue()
        self.nodes = []

    def start(self):
        self.logger.info("Starting coordinator")

        logging.info("Starting Network")
        self.network = Process(target=start_network_thread, args=(self,))
        self.network.start()

        logging.info("Starting RawDataLogger")
        self.raw_data_logger = Process(target=start_raw_data_logger_thread, args=(self,))
        self.raw_data_logger.start()

    #### Callbacks for Network ####
    def network_register_node(self, node):
        logging.info("Registering " + node.name)
        if not node in self.nodes:
            self.nodes.append(node)
        else:
            logging.warning(node.address[0] + " changed it's name!")

    def network_new_block(self, node, command):
        logging.info(node.name + " received new block " + str(node.block_id))

