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

class Coordinator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def start(self):
        self.logger.info("Starting coordinator")
        logging.info("Starting Network")
        self.network = Process(target=start_network_thread, args=(self,))
        self.network.start()

