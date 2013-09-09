import os
import time
import tornado.wsgi

import controllers
from admin import admin
import uimodules

settings = {
    "debug": False,
    "blog_title": u"YoungPay's Blog",
    "blog_url": u"http://yangpei.appsp0t.com",
    "blog_page_size": 10,
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "xsrf_cookies": True,
    "ui_modules": uimodules,
    "cookie_secret": '\xd9\xaf6yV\x1cM\x10\x9f0\xdaS%\x17\xdcg\x12\xa3u\xbc\xf1z\xda\x85',
    "auth_cookie_name": "ypbauth",
    "login_url": "/admin/login",
}

application = tornado.wsgi.WSGIApplication(controllers.routes + admin.routes, **settings)
