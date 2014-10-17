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
import hashlib
import json

GREETINGS_NODE_TO_COORDINATOR = hashlib.sha256(b"NodeToCoordinatorReportingForDuty").digest()
GREETINGS_COORDINATOR_TO_NODE = hashlib.sha256(b"CoordinatorToNodeReportingForDuty").digest()

class Network:
    def __init__(self, node):
        self.node = node
        self.logger = logging.getLogger(__name__)
        self.connected = False

    def _connect(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((config.coordinator_host, config.coordinator_port))
            self.logger.info("Connected to coordinator")
            self.connected = True
            self._send_command(bytes(json.dumps({"name": "hello", "node_name": config.name}), "utf-8"))
            self.s.setblocking(False)
        except ConnectionRefusedError:
            self.connected = False

    def _send_command(self, data):
        try:
            self.s.sendall(struct.pack('!I', len(data)))
            self.s.sendall(data)
        except BrokenPipeError:
            self.logger.warning("Disconnected from coordinator")
            self.connected = False

    def _handle_command(self, command):
        self.logger.debug("Handling command: " + command.name)
        self._send_command(command.serialize())

    def run(self):
        self.logger.info("Started")
        while True:
            if not self.connected:
                self._connect()
            if self.connected:
                if self.node.network_commands.empty():
                    time.sleep(0.01)
                elif self.connected:
                    #TODO: try except
                    self._handle_command(self.node.network_commands.get())
                else:
                    time.sleep(0.01)
            else:
                time.sleep(0.01)


