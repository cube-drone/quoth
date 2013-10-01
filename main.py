import config
import request_response_bot.bot
import imitation
import time

def main():
    irc_settings = config.config("irc_config.txt")
    
    c = request_response_bot.bot.RequestResponseBot(
                imitation.quote,                 
                irc_settings["server"], 
                int(irc_settings["port"]), 
                irc_settings["channel"], 
                irc_settings["nick"] )
    c.start()
    
if __name__ == "__main__":
    irc_settings = config.config("irc_config.txt")
    reconnect_interval = irc_settings["reconnect"]
    while True:
        try:
            main()
        except request_response_bot.bot.ServerNotConnectedError:
            print "Server Not Connected! Let's try again!"             
            time.sleep(float(reconnect_interval))
            
