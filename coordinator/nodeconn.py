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
import struct
import json
import socket

PACKET_BUFFER_LIMIT = 2**20

#TODO: Maybe mutex this class?
class NodeConn:
    def __init__(self, coordinator, conn, address):
        self.packet_buffer = bytearray()
        self.conn = conn
        self.address = address
        self.logger = logging.getLogger(__name__)
        #TODO: Add greetings from node before accepting
        self.accepted = False
        self.name = address[0]
        self.coordinator = coordinator

        self.block_id = 0
        self.block_height = 0

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass

    def fetch_packets(self):
        buff = self.conn.recv(1024)
        self.packet_buffer += buff
        if len(self.packet_buffer) > PACKET_BUFFER_LIMIT:
            self.logger.error(self.address[0] + " is trying to flood us with data!")
            raise OverflowError

    def parse_command(self):
        parsed_a_command = False
        if len(self.packet_buffer) > 4:
            command_length = struct.unpack('!I', self.packet_buffer[:4])[0]
            if command_length + 4 >= len(self.packet_buffer):
                try:
                    command = bytes(self.packet_buffer[4:command_length + 4])
                    command = command.decode("utf-8")
                    command = json.loads(command)
                except Exception:
                    self.logger.error(self.name + " sent a malformed json!")
                    raise SyntaxError
                self.packet_buffer = self.packet_buffer[command_length + 4:]
                parsed_a_command = True

                self.logger.debug("Command " + str(command) + " from " + self.address[0])
                self._process_command(command)

                
        return parsed_a_command

    #### Command definitions ####
    def _process_command(self, command):
        name = command['name']
        if name == 'hello':
            self._hello(command)
        elif name == 'new_block':
            self._new_block(command)
        else:
            self.logger.warning(self.name + ": Unknown command - " + str(command))

    def _hello(self, command):
        self.name = command['node_name']
        self.logger.info(self.address[0] + " is now known as " + self.name)
        self.accepted = True
        self.coordinator.network_register_node(self)

    def _new_block(self, command):
        self.block_id = int(command['block_id'])
        self.height = int(command['height'])
        self.coordinator.network_new_block(self, command)
