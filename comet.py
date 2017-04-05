#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 nikbird <nikbird@server>
#
# Distributed under terms of the MIT license.

"""

"""

import tornado.ioloop
import tornado.web
from tornado.httpclient import HTTPClient, AsyncHTTPClient
import json

from guild_site import settings


Users = {}


class GetMessage(tornado.web.RequestHandler):
    def get(self):
        def handle_response(response):
            content = response.body
            print(content)
            print(type(content))
            json_content = json.loads(content.decode("utf-8"))
            print(json_content)
            print(type(json_content))
            print()
        #sessionid = self.get_cookie("sessionid")
        #print(sessionid, type(sessionid))

        client = AsyncHTTPClient()
        url = 'http://127.0.0.1:8001' + settings.COMET_URL_POST_MESSAGE
        print(url)
        client.fetch(url, handle_response)


class PostMessage(tornado.web.RequestHandler):
    def post(self):
        pass
        #s = json.dumps({'username': 'Вася', 'sessionid': 'mymegasessionid'})
        #self.write(s)

    get = post


class UserLogin(tornado.web.RequestHandler):
    def post(self):
        userData = json.loads(self.request.body.decode("utf-8"))
        Users[userData['sessionid']] = userData['username']
        print('after login, Users = ', Users)


class UserLogout(tornado.web.RequestHandler):
    def post(self):
        userData = json.loads(self.request.body.decode('utf-8'))
        if userData['sessionid'] in Users:
            del Users[userData['sessionid']]
        print('after logout, Users = ', Users)


def make_app():
    return tornado.web.Application([
        (settings.COMET_URL_GET_MESSAGE, GetMessage),
        (settings.COMET_URL_POST_MESSAGE, PostMessage),
    
        (settings.COMET_URL_NOTIFY_USER_LOGIN, UserLogin),
        (settings.COMET_URL_NOTIFY_USER_LOGOUT, UserLogout),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8001, "127.0.0.1")
    tornado.ioloop.IOLoop.current().start()

