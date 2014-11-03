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
from queue import Queue

PACKET_BUFFER_LIMIT = 2**20

class NodeConn:
    def __init__(self, coordinator, conn, address):
        self.packet_buffer = bytearray()
        self.conn = conn
        self.address = address
        self.logger = logging.getLogger(__name__)
        #TODO: Add greetings from node before accepting
        #TODO: Drop connection if not greeted for 5 sec
        #TODO: Greeting uses a secret message
        self.accepted = False
        self.name = address[0]
        self.coordinator = coordinator
        self.scenario_progress = None
        self.secret_phrase = "aaa"
        self.account_id = 828683301869051229
        self.accounts = []

        self.command_buffer = Queue()

        self.block_id = 0
        self.block_height = 0
        self.account_revolver = 0

    def add_account(self, account_id, secret_phrase, pubkey):
        self.accounts.append([account_id, secret_phrase, pubkey])

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass

    def fetch_packets(self):
        try:
            buff = self.conn.recv(1024)
            self.packet_buffer += buff
            if len(self.packet_buffer) > PACKET_BUFFER_LIMIT:
                self.logger.error(self.address[0] + " is trying to flood us with data!")
                raise OverflowError
        except BlockingIOError:
            pass

    def parse_command(self):
        parsed_a_command = False
        if len(self.packet_buffer) > 4:
            command_length = struct.unpack('!I', self.packet_buffer[:4])[0]
            if command_length + 4 <= len(self.packet_buffer):
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

    #### Commands from Scenario Runner ####
    def start_nxt(self):
        self.command_buffer.put(json.dumps({"name": "start_nxt"}))

    def start_forging(self, secret_phrase, account_id):
        self.command_buffer.put(json.dumps({"name": "start_forging", "secret_phrase": secret_phrase, "account_id": account_id}))

    def send_money(self, recipient, amountNQT, secret_phrase, pubkey=None):
        self.command_buffer.put(json.dumps({"name": "send_money", "secret_phrase": secret_phrase,
                                            "recipient": recipient, "amountNQT": amountNQT, "pubkey": pubkey}))

