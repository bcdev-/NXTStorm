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

PACKET_BUFFER_LIMIT = 2**20

class NodeConn:
    def __init__(self, conn, address):
        self.packet_buffer = bytearray()
        self.conn = conn
        self.address = address
        self.logger = logging.getLogger(__name__)
        #TODO: Add greetings from node before accepting
        self.accepted = True
        self.name = address[0]

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
                command = str(self.packet_buffer[4:command_length + 4])
                self.packet_buffer = self.packet_buffer[command_length + 4:]
                parsed_a_command = True

                self.logger.debug("Command " + command + " from " + self.address[0])
                
        return parsed_a_command

