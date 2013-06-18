#coding: utf-8
import tornado.web
from models import db, Entry
from google.appengine.api import users


class BaseHandler(tornado.web.RequestHandler):
    def get_error_html(self, status_code, exception=None, **kwargs):
        self.render("error.html", status_code=status_code, ex=exception)

class HomeHandler(BaseHandler):
    def get(self):
        entities = db.Query(Entry).order("-published").fetch(limit=10)
        self.render("home.html", entities=entities)

class PostHandler(BaseHandler):
    def get(self, key):
        post = Entry.get(key)
        self.render("post.html", post=post)
