import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

import json

import logging
import os
 
from tornado.options import define, options
from messageHandler import *

log = logging.getLogger(__name__)
WEBSOCKS = []
USER_CLIENTS = dict()
ADMIN_CLIENTS = []

testCounter = 0

###
class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/admin_map.html")
        
class UserHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/client_map.html")
 
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        log.info("Opened socket %r" % self)
        global WEBSOCKS
        WEBSOCKS.append(self)
        
 
    def on_message(self, message):
        print 'message received %s' % message
        commMessageInstance = CommMessage.parse(message)
 
        global USER_CLIENTS, ADMIN_CLIENTS
        
        # Handle Bus websockets
        if commMessageInstance.SourceType.lower() == "bus":

            lati, longi = commMessageInstance.CommandData.split(';')
            
            log.debug("pinging: %r" % WEBSOCKS)

            latlng = {
                'lat': lati,
                'lng': longi,
                'title': "Bus Data",
            }

            # Update admins of bus location
            data = json.dumps(latlng)
            for sock in ADMIN_CLIENTS:
                sock.write_message(data)
              
            global testCounter
            testCounter = testCounter + 1
            if (testCounter % 5 == 0):
                print "Message sent to user"
                for user in USER_CLIENTS.keys():
                    user_ws = USER_CLIENTS[user]['websocket']
                    
                    if user_ws is not None:
                        user_ws.write_message("data received for server")
            
             
             
        # Handle Users websockets
        elif commMessageInstance.SourceType.lower() == "user":
            username = commMessageInstance.SourceName 
            user_lati, user_longi = commMessageInstance.CommandData.split(';')
            
            userdata = {
               'lat': user_lati,
               'lng': user_longi,
               'websocket': self,                
            }

            USER_CLIENTS[username] = userdata
            print USER_CLIENTS
                
            # Handle Admin websockets
        elif commMessageInstance.SourceType.lower() == "admin":
            ADMIN_CLIENTS.append(self)
            
 
    def on_close(self):
        #print 'connection closed'
        log.info("Closed socket %r" % self)
        global WEBSOCKS, USER_CLIENTS, ADMIN_CLIENTS
        WEBSOCKS.remove(self)
        
        ''' 
        # TODO: fix USERS_CLIENT, ADMIN_CLIENTS removal
        try:
            ADMIN_CLIENTS.remove(self)
            print "Admin websocket removed from ADMIN_CLIENTS"
            
        except:
            print "Current Websocket not in ADMIN_CLIENTS"
            
        
        for user in USER_CLIENTS.key():
            user_wb = USER_CLIENTS[user]['websocket']
            if user_wb == self:
                USER_CLIENTS.pop(user)
        '''
        

''' 
class WebSocketBroadcaster(tornado.websocket.WebSocketHandler):
    """Keeps track of all websocket connections in
    the global WEBSOCKS variable.
	"""
    def open(self):
        log.info("Opened socket %r" % self)
        global WEBSOCKS
        WEBSOCKS.append(self)

    def on_message(self, message):
        log.info(u"Got message from websocket: %s" % message)

    def on_close(self):
        log.info("Closed socket %r" % self)
        global WEBSOCKS
        WEBSOCKS.remove(self)
'''

settings = {
	'static_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
}

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", UserHandler),
            (r"/admin", AdminHandler),
            (r"/ws", WebSocketHandler),
        ],
		**settings
    )

    define("port", default=8888, help="Run server on a specific port", type=int)
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    print "[SERVER Started] Listening on port:", options.port
    tornado.ioloop.IOLoop.instance().start()