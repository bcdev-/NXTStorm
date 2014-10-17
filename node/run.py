#!/usr/bin/env python3
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

import sys
if sys.version_info < (3, 0):
    sys.stdout.write("Node requires Python 3.x\n")
    sys.exit(1)

import config
import time

from node import Node

node = Node()
node.start()

node.start_nxt()
node.start_forging(config.account_id, config.secret_phrase)
time.sleep(600000)
node.stop_nxt()
time.sleep(2)

