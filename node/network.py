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
import socket
import config
import struct

class Network:
    def __init__(self, node):
        self.node = node
        self.logger = logging.getLogger(__name__)
        self.connected = False

    def _connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((config.coordinator_host, config.coordinator_port))
        self.s.sendall(b"NodeReporting")
        self.s.setblocking(True)
        '''
        response = self.s.recv(15)
        if response != b"CoordinatorHere":
            self.logger.error("Coordinator is an imposter! " + str(response))
        else:
            self.logger.info("Connected to coordinator")
        '''
        self.connected = True
        self.s.setblocking(False)

    def _send_command(self, data):
        #TODO: Try catch socket errors
        self.s.sendall(struct.pack('!I', len(data)))
        self.s.sendall(data)

    def _handle_command(self, command):
        self.logger.debug("Handling command: " + command.name)
        self._send_command(command.serialize())

    def run(self):
        self.logger.info("Started")
        self._connect()
        while True:
            if self.node.network_commands.empty():
                time.sleep(0.05)
            elif self.connected:
                #TODO: try except
                self._handle_command(self.node.network_commands.get())
            else:
                time.sleep(0.05)


