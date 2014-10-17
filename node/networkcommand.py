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

import time
import json

class NetworkCommand:
    NEW_BLOCK = 0

    def __init__(self, command_type):
        self.command_type = command_type

    @classmethod
    def new_block(cls, block_id, height):
        command = cls(cls.NEW_BLOCK)
        command.name = "new_block"
        command.timestamp = time.time()
        command.block_id = block_id
        command.height = height
        command.serialize = command.serialize_new_block
        return command

    def serialize_new_block(self):
        data = {'name': self.name}
        data['block_id'] = self.block_id
        data['height'] = self.height
        data['timestamp'] = self.timestamp
        return bytes(json.dumps(data), "ascii")

