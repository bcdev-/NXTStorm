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
import socket
import config
import hashlib
import struct
import time
import traceback

GREETINGS_NODE_TO_COORDINATOR = hashlib.sha256(b"NodeToCoordinatorReportingForDuty").digest()
GREETINGS_COORDINATOR_TO_NODE = hashlib.sha256(b"CoordinatorToNodeReportingForDuty").digest()

from nodeconn import NodeConn

class Network:
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self.logger = logging.getLogger(__name__)
        self.nodes = []

    def _open_socket(self):
        #TODO: Try catch for ports < 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((config.host, config.port))
        self.socket.setblocking(0)
        self.socket.listen(1)

    def _accept_connections(self):
        while True:
            try:
                conn, address = self.socket.accept()
                conn.setblocking(0)
                #TODO: Send greetings
                self.nodes.append(NodeConn(self.coordinator, conn, address))

                self.logger.info("Connection accepted from " + address[0])
            except BlockingIOError:
                break

    def _manage_nodes(self):
        for node in self.nodes:
            #TODO: Try&remove if conn failed
            try:
                node.fetch_packets()
                while node.parse_command():
                    pass
            except Exception:
                self.logger.error(traceback.format_exc())
                self.logger.error("Node " + node.address[0] + " caused an error, removing.")
                #TODO: Close connection properly
                self.nodes.remove(node)
                continue

    def run(self):
        self.logger.info("Started")
        self._open_socket()

        while True:
            time.sleep(0.001)
            self._accept_connections()
            self._manage_nodes()

