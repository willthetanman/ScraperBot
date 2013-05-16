# -*- coding: utf-8 -*-

"""
Bot: main entry point for the bot

"""
import chatbot
import random
import time

import Skype4Py
import sqlalchemy as sql

import parse
import dispatch
import model

# Modules
import testing
import intel
import help


__all__ = ["Bot"]


INVALID_RESPONSES = ("no.",
                     "i can't understand your jabber.",
                     "forgettaboutit.",
                     "leave me alone.",
                     "i'm ignoring you...")

AFFIRMATIVE_COUNT = 27

AFFIRMATIVE_RESPONSES = ("yes.", 
                         "i agree.", 
                         "i didn't know that", 
                         "what do you mean?",
                         "learn something new everyday.")




class Bot(object):
    def __init__(self, name="chatbot", send_announcements=False):
        self.skype = None
        self.name = name
        self.send_announcements = send_announcements
        self.count = 0
        
        import sqlalchemy as sql
        self.db = sql.create_engine("sqlite:///logs/messages.sqlite3")

        chatbot.model.use_engine(self.db)
    

    def connect_and_listen(self):
        self.skype = Skype4Py.Skype()
        self.skype.Attach()
        self.skype.OnMessageStatus = self.message_status
        
        self.announce("ChatBot Ready...")
        
        try:
            while self.skype.AttachmentStatus == Skype4Py.apiAttachSuccess:
                time.sleep(10)
        except KeyboardInterrupt:
            self.announce("Signing off. Goodbye!")
            print
    
    
    def get_name(self):
        name = self.name
        if self.is_attached():
            user = self.skype.CurrentUser
            name = user.DisplayName
            if not name:
                name = user.FullName
        return "@" + name.lower()

        
    def is_attached(self):
        return self.skype.AttachmentStatus == Skype4Py.apiAttachSuccess

        
    def announce(self, message, force=False):
        print message
        if not self.is_attached() or (not force and not self.send_announcements):
            return
        for chat in self.skype.Chats:
            chat.SendMessage(message)
    
    
    def added_to_chat(self, chat):
        chat.SendMessage("Hello!")
    
    
    def message_status(self, message, status):
        # Dispatch all messages
        # if status == Skype4Py.cmsUnknown:
        if status == Skype4Py.cmsReceived:
            self.message_received(message)
            
        # Dispatch everytime chatbot is added to a chat
        if message.Type == Skype4Py.cmeAddedMembers:
            for user in message.Users:
                if user.Handle == self.skype.CurrentUser.Handle:
                    self.added_to_chat(message.Chat)
                    return
    

    def get_random_negative_response(self):
        try:
            q = chatbot.model.phrases.select().where(chatbot.model.phrases.c.type < 0)
            phrases = [result.phrase for result in chatbot.model.engine.execute(q).fetchall()]
            return random.choice(phrases)

        except Exception, e:
            print e
            pass

        return random.choice(INVALID_RESPONSES)
    

    def get_random_positive_response(self):
        try:
            q = chatbot.model.phrases.select().where(chatbot.model.phrases.c.type > 0)
            phrases = [result.phrase for result in chatbot.model.engine.execute(q).fetchall()]
            return random.choice(phrases)

        except Exception, e:
            print e
            pass

        return random.choice(AFFIRMATIVE_RESPONSES)


    def message_received(self, message):
        try:
            if (message.Body.lower().startswith("{0} ".format(self.get_name())) or message.Body.lower().startswith('@tanbot') or message.Body.lower().startswith('@tbot')):
                result = self.process_command(message)
                if not result:                    
                    result = self.get_random_negative_response()
            else:
                result = self.process_message(message)
        
        except Exception, e:
            import traceback
            result = "Error: {0}".format(e)
            print result
            traceback.print_exc()
            
        if result:
            self.send_reply(message, result)
    
    
    def send_reply(self, message, result):
        message.Chat.SendMessage(result)
        
    
    def process_command(self, message):
        body = message.Body.strip()
        parsed_body = body.split()
        parsed_body[0] = self.get_name()  # Replacing any alias names with original skype handle to ensure parsing works
        body = ' '.join(parsed_body)
        
        command_string = body[len(self.get_name()):]
        command_string = command_string.strip()
        command, arguments = chatbot.parse.parse_command(command_string)
        command = str(command)

        if chatbot.parse.parse_command_check(command) == True:
            arguments = command
            return self.dispatch_command("ip", arguments, message=message, bot=self)
        else:
            return self.dispatch_command(command, arguments, message=message, bot=self)

    def process_message(self, message):
        result = chatbot.dispatch.dispatch_to_handlers("__message__", message=message, bot=self)
        
        if not result:
            self.count += 1
            
            if self.count % AFFIRMATIVE_COUNT == 0:
                result = self.get_random_positive_response()
        
        return result
    
    
    def dispatch_command(self, command, *args, **kwargs):
        return chatbot.dispatch.dispatch_to_handlers(command, *args, **kwargs)

    
    
if __name__ == "__main__":
    pass
