#coding: utf-8
import tornado.web
from models import db, Entry
from google.appengine.api import users


class BaseHandler(tornado.web.RequestHandler):
    pass

class HomeHandler(BaseHandler):
    def get(self):
        entities = db.Query(Entry).order("-published").fetch(limit=10)
        self.render("home.html", entities=entities)

class PostHandler(BaseHandler):
    def get(self, id):
        try:
            post = Entry.get(id)
            self.render("post.html", post=post)
        except Exception:
            raise tornado.web.HTTPError(404)
        
    
