import os.path
import tornado.wsgi

import controllers
from admin import admin
import uimodules

settings = {
    "blog_title": u"YoungPay's Blog",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "xsrf_cookies": True,
    "ui_modules": uimodules,
}
application = tornado.wsgi.WSGIApplication(controllers.routes + admin.routes, **settings)
