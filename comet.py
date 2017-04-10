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
from tornado.httputil import url_concat
from tornado.httpclient import HTTPRequest, HTTPClient, AsyncHTTPClient
from datetime import datetime
import json


from django.conf import settings as dj_settings
from django.core.urlresolvers import reverse
from guild_site import settings


dj_settings.configure(ROOT_URLCONF=settings.ROOT_URLCONF)


def get_from_django(djURL, args=None):
    theUrl = url_concat('http://127.0.0.1:8000' + djURL, args)
    request = HTTPRequest(theUrl)
    return json.loads(HTTPClient().fetch(request).body.decode('utf-8'))


#result = get_from_django(reverse('latest'), {'count': 5})
#for record in result:
#    record['created'] = datetime.strptime(record['created'], "%c")
#    record['lastChanged'] = datetime.strptime(record['lastChanged'], "%c")
#print(result)


# словарь залогиненных пользователей
# sessionID: username
#request = HTTPRequest('http://127.0.0.1:8000' + reverse('users'), body=json.dumps({'secret': settings.SECRET_KEY}), allow_nonstandard_methods=True)
#result = HTTPClient().fetch(request).body
#USERS = json.loads(result.decode('utf-8'))
USERS = get_from_django(reverse('users'), { 'secret': settings.SECRET_KEY })
print(USERS)



# ID последнего сообщения в БД
#request = HTTPRequest('http://127.0.0.1:8000' + reverse('lastid'), body=json.dumps({'secret': settings.SECRET_KEY}), allow_nonstandard_methods=True)
#result = HTTPClient().fetch(request).body
#LAST_ID = int(result)
LAST_ID = get_from_django(reverse('lastid'), { 'secret': settings.SECRET_KEY })
print(LAST_ID)


# словарь клиентов, ожидающих новые сообщения
WAITERS = {}



class MessageHandler(tornado.web.RequestHandler):

    def get(self):
        sessionid = self.get_cookie('sessionid')
        #if sessionid not in Users:
        #   тут мы посылаем неизвестных лиц нахер

        clientLastID = int(self.get_argument('lastid'))
        if clientLastID < LAST_ID:
            messageBytes = get_from_django(reverse('latest'), { 'count': LAST_ID - clientLastID })
            messages = json.loads(messageBytes.decode('utf-8'))
            #for msgRecord in messages:
            #
            


class UserLogin(tornado.web.RequestHandler):
    #
    #   Обработчик уведомления о входе пользователя
    #   Через nginx данный URL не проходит, проверку прав доступа можно не делать
    #
    def post(self):
        userData = json.loads(self.request.body.decode("utf-8"))
        Users[userData['sessionid']] = userData['username']
        print('after login, Users = ', Users)


class UserLogout(tornado.web.RequestHandler):
    #
    #   Обработчик уведомления о выходе пользователя
    #   Через nginx данный URL не проходит, проверку прав доступа можно не делать
    #
    def post(self):
        userData = json.loads(self.request.body.decode('utf-8'))
        if userData['sessionid'] in Users:
            del Users[userData['sessionid']]
        print('after logout, Users = ', Users)


def make_app():
    return tornado.web.Application([
        (settings.COMET_URL_MESSAGE, MessageHandler),
        (settings.COMET_URL_NOTIFY_LOGIN, UserLogin),
        (settings.COMET_URL_NOTIFY_LOGOUT, UserLogout),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8001, "127.0.0.1")
    tornado.ioloop.IOLoop.current().start()

