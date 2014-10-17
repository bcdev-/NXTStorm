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

class RawDataLogger:
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self.logger = logging.getLogger(__name__)

    def _execute(self):
        if self.coordinator.raw_data_logger_queue.empty():
            return False
        #TODO: try catch
        command = self.coordinator.raw_data_logger_queue.get()
        print(command)
        return True

    def run(self):
        self.logger.info("Started")
        while True:
            time.sleep(0.001)
            while self._execute():
                pass
