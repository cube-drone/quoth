#! /usr/bin/env python
#

#libs
from ircbot import SingleServerIRCBot
import irclib
import sys
import re
import time
import datetime
        
ServerNotConnectedError = irclib.ServerNotConnectedError

class RequestResponseBot(irclib.SimpleIRCClient):
    """
        This IRC bot takes a string-to-string transformation function as an argument.
        
        So, if we were to create a RequestResponseBot with 'reverse' as the function

        And someone were to talk to the bot, like so: 
            <dudeguy> bot_name: arglebargle

        it would respond with"
            <bot_name> dudeguy: elgrabelgra 
    """
    
    def __init__(self, request_response_function, server, port, channel, nick): 
    
        irclib.SimpleIRCClient.__init__(self)
        
        #IRC details
        self.server = server
        self.port = port
        self.target = channel
        self.channel = channel
        self.nick = nick
        
        #Regexes
        self.nick_reg = re.compile("^" + nick + "[:,](?iu)")
        
        self.ircobj.delayed_commands.append( (time.time()+5, self._no_ping, [] ) )
    
        self.connect(self.server, self.port, self.nick)
        self.last_ping = 0
    
        # RequestResponse
        self.request_response_function = request_response_function

    
    def _no_ping(self):
        if self.last_ping >= 1200:
            raise irclib.ServerNotConnectedError
        else:
            self.last_ping += 10
        self.ircobj.delayed_commands.append( (time.time()+10, self._no_ping, [] ) )


    def _dispatcher(self, c, e):
    # This determines how a new event is handled. 
        if(e.eventtype() == "pubmsg"):
            try: 
                source = e.source().split("!")[0]
            except IndexError:
                source = ""
            try:
                text = e.arguments()[0]
            except IndexError:
                text = ""
            
        m = "on_" + e.eventtype()   
        if hasattr(self, m):
            getattr(self, m)(c, e)

    def on_nicknameinuse(self, c, e):
        self.nick = c.get_nickname() + "_"
        self.nick_reg = re.compile("^" + self.nick + "[:,](?iu)")
        c.nick(self.nick)

    def on_welcome(self, connection, event):
        if irclib.is_channel(self.target):
            connection.join(self.target)

    def on_disconnect(self, connection, event):
        connection.disconnect()
        raise irclib.ServerNotConnectedError

    def on_ping(self, connection, event):
		self.last_ping = 0

    def on_pubmsg(self, connection, event):
        text = event.arguments()[0]
        
        try: 
            source = event.source().split("!")[0]
        except IndexError:
            source = ""

        # If you talk to the bot, this is how he responds.
        if self.nick_reg.search(text):
            if len(text.split(":")) > 1:
                message = ":".join(text.split(": ")[1:])
                connection.privmsg(self.channel, source+": "+self.request_response_function(message)) 
            else:
                print text

