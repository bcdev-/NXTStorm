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
import traceback

GREETINGS_NODE_TO_COORDINATOR = hashlib.sha256(b"NodeToCoordinatorReportingForDuty").digest()
GREETINGS_COORDINATOR_TO_NODE = hashlib.sha256(b"CoordinatorToNodeReportingForDuty").digest()

class Network:
    def __init__(self, node):
        self.node = node
        self.logger = logging.getLogger(__name__)
        self.connected = False
        self.packet_buffer = bytearray()

    def _connect(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((config.coordinator_host, config.coordinator_port))
            self.logger.info("Connected to coordinator")
            self.connected = True
            self._send_command(bytes(json.dumps({"name": "hello", "node_name": config.name}), "utf-8"))
            self.s.setblocking(False)
        except Exception:
            #TODO: After some failed connections, a bogus socket seems to be made, that "looks like" it works...
            self.logger.warning("Connection from coordinator refused")
            self.connected = False
            time.sleep(1)

    def _send_command(self, data):
        try:
            self.s.sendall(struct.pack('!I', len(data)))
            self.s.sendall(data)
        except BrokenPipeError:
            self.logger.warning("Disconnected from coordinator")
            self.connected = False
            time.sleep(1)

    def _fetch_packets(self):
        #TODO: Networking in another thread [to save cpu consumption]
        #TODO: Heartbeats - sometimes node thinks that connection is still on, when it's off.
        try:
            buff = self.s.recv(1024)
            self.packet_buffer += buff
        except BlockingIOError:
            pass
        except Exception:
            self.logger.warning("Disconnected from coordinator")
            self.connected = False
            time.sleep(1)

    def _process_command(self, command):
        name = command['name']
        if name == "hello":
            pass # TODO: Process this command
        if name == "start_nxt":
            self.node.push_nxt_handler_interrupt(command)
#            self.node.start_nxt()
        if name == "start_forging":
            self.node.push_nxt_handler_command(command)
#            self.node.start_forging(command['account_id'], command['secret_phrase'])
        if name == "prepare_send_money_tx":
#            self.node.push_nxt_handler_command(command)
#            self.node.prepare_send_money_tx(command['secret_phrase'], command['recipient'], command['amountNQT'])
            pass
        if name == "send_money":
            self.node.push_nxt_handler_command(command)
#            self.node.send_money(command['secret_phrase'], command['recipient'], command['amountNQT'])

    def _parse_incoming_command(self):
        parsed_a_command = False
        if len(self.packet_buffer) > 4:
            command_length = struct.unpack('!I', self.packet_buffer[:4])[0]
            if command_length + 4 <= len(self.packet_buffer):
                try:
                    command = bytes(self.packet_buffer[4:command_length + 4])
                    command = command.decode("utf-8")
                    command = json.loads(command)

                    self.packet_buffer = self.packet_buffer[command_length + 4:]
                    parsed_a_command = True

                    self.logger.debug("Command " + str(command) + " from coordinator")
                    self._process_command(command)
                except Exception:
                    self.logger.error("Coordinator sent a malformed json: " + str(command))
                    self.logger.error(traceback.format_exc())
                    self.connected = False
                    return False


        return parsed_a_command

    def _handle_command(self, command):
        self.logger.debug("Handling command: " + command.name)
        self._send_command(command.serialize())

    def run(self):
        self.logger.info("Started")
        while True:
            if not self.connected:
                self._connect()
            if self.connected:
                self._fetch_packets()
                while self._parse_incoming_command():
                    pass
                if self.node.network_commands.empty():
                    time.sleep(0.01)
                elif self.connected:
                    #TODO: try except
                    self._handle_command(self.node.network_commands.get())
                else:
                    time.sleep(0.01)
            else:
                time.sleep(0.01)


