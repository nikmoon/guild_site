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
from tornado import gen
from tornado.concurrent import Future
from tornado.httputil import url_concat
from tornado.httpclient import HTTPRequest, HTTPClient, AsyncHTTPClient
from datetime import datetime
import json


from django.conf import settings as dj_settings
from django.core.urlresolvers import reverse
from guild_site import settings


dj_settings.configure(ROOT_URLCONF=settings.ROOT_URLCONF)


@gen.coroutine
def async_request_django(djangoURI, method='GET', body=None, args=None, headers=None, raw=False):
    fullURL = url_concat(settings.DJANGO_SERVER + djangoURI, args)
    client = AsyncHTTPClient()
    response = yield client.fetch(fullURL, method=method, body=body,  headers=headers)
    if raw:
        return response.body
    else:
        return json.loads(response.body.decode('utf-8'))


def request_django(djangoURI, args=None, headers=None, raw=False):
    fullURL = url_concat(settings.DJANGO_SERVER + djangoURI, args)
    client = HTTPClient()
    response = client.fetch(fullURL, headers=headers)
    if raw:
        return response.body
    else:
        return json.loads(response.body.decode('utf-8'))


# словарь клиентов, ожидающих новые сообщения
WAITERS = []


class MessagesHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        #
        #   Возвращаем клиенту те сообщения, которых у него нет
        #   или ждем новое сообщение и посылаем его клиенту
        #
        data = yield self.get_last_messages()
        if data and 'username' in data:
            if data['messages']:
                self.write(data)
            else:
                self.waitFuture = Future()
                WAITERS.append(self.waitFuture)
                msg = yield self.waitFuture
                self.write(msg)
        else:
            self.write({})
            self.set_status(403)
        return


    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8)'))
        if data.get('secret') != settings.SECRET_KEY:
            self.set_status(403)
            return
        del data['secret']
        for waiter in WAITERS:
            waiter.set_result(data)
        WAITERS.clear()


    @gen.coroutine
    def get_last_messages(self):
        sessionID = self.get_cookie('sessionid')
        if sessionID:
            lastID = self.get_argument('lastid','')
            args = {'lastid': lastID} if lastID else None
            headers = {'Cookie': 'sessionid=' + sessionID}
            result = yield async_request_django(reverse('messages'), args=args, headers=headers)
        else:
            result = {}
        return result

        

def make_app():
    return tornado.web.Application([
        (settings.COMET_MSG_URL, MessagesHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8001, "127.0.0.1")
    tornado.ioloop.IOLoop.current().start()

