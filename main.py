#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import logging
import tornado.web
import tornado.websocket
import tornado.ioloop

LOG = logging.getLogger('main')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        with open('html/index.html') as f:
            self.finish(f.read())

class ClientHandler(tornado.web.RequestHandler):
    def get(self):
        with open('html/client.html') as f:
            self.finish(f.read())

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    CLIENTS = set()

    def open(self):
        LOG.debug('open %s', id(self))
        self.CLIENTS.add(self)

    def on_message(self, message):
        for client in self.CLIENTS:
            if client != self:
                LOG.debug('message %s', id(client))
                client.write_message(message, binary=True)

    def on_close(self):
        LOG.debug('close %s', id(self))
        self.CLIENTS.remove(self)

if __name__ == '__main__':
    HOST = "0.0.0.0"
    PORT = 9666
    ENDPOINTS = [
        (r'/', IndexHandler),
        (r'/client', ClientHandler),
        (r'/ws', WebSocketHandler),
    ]
    logging.basicConfig(level=logging.DEBUG)
    APP = tornado.web.Application(ENDPOINTS)
    APP.listen(PORT, HOST)

    tornado.ioloop.IOLoop.current().start()
