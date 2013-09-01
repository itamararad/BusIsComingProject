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

###
class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/admin_map.html")
        
class UserHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/client_map.html")
 
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        #print 'new connection'
        #self.write_message("connected")
        log.info("Opened socket %r" % self)
        global WEBSOCKS
        WEBSOCKS.append(self)
        
 
    def on_message(self, message):

        print 'message received %s' % message
        #deviceHandler = MessageHandler.invoke(message)
        commMessageInstance = CommMessage.parse(message)
 
        if commMessageInstance.Source.lower() == "bus":
            lati, longi = commMessageInstance.CommandData.split(';')
            print lati, longi
            
            global WEBSOCKS
            log.debug("pinging: %r" % WEBSOCKS)

            latlng = {
                'lat': lati,
                'lng': longi,
                'title': "Bus Data",
            }

            data = json.dumps(latlng)
            for sock in WEBSOCKS:
                sock.write_message(data)
                
        #print deviceHandler
        #if (isinstance(deviceHandler, BusHandler)):
        #    print deviceHandler.Position.toString()
        
        
 
    def on_close(self):
        #print 'connection closed'
        log.info("Closed socket %r" % self)
        global WEBSOCKS
        WEBSOCKS.remove(self)

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