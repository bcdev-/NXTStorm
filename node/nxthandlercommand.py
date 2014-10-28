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

#TODO: This class is redundant, remove!
class NxtHandlerCommand:
    START_NXT = 0
    STOP_NXT = 1
    START_FORGING = 2
    SEND_MONEY = 2

    def __init__(self, command_type):
        self.command_type = command_type

    @classmethod
    def start_nxt(cls):
        command = cls(cls.START_NXT)
        command.name = "Start NXT"
        return command

    @classmethod
    def stop_nxt(cls):
        command = cls(cls.STOP_NXT)
        command.name = "Stop NXT"
        return command

    @classmethod
    def start_forging(cls, account_id, secret_phrase):
        command = cls(cls.START_FORGING)
        command.name = "Start forging"
        command.account_id = account_id
        command.secret_phrase = secret_phrase
        return command

    @classmethod
    def send_money(cls, secret_phrase, recipient, amountNQT):
        command = cls(cls.SEND_MONEY)
        command.name = "Send money"
        command.secret_phrase = secret_phrase
        command.recipient = recipient
        command.amountNQT = amountNQT
        return command

