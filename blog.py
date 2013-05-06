import os.path
import tornado.wsgi

import controllers

settings = {
    "blog_title": u"YoungPay's Blog",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "xsrf_cookies": True,
}
application = tornado.wsgi.WSGIApplication([
    (r"/", controllers.HomeHandler),
    (r"/post/(.+)", controllers.PostHandler),
], **settings)
