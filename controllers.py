#coding: utf-8
import tornado.web
from models import db,Entry

class BaseHandler(tornado.web.RequestHandler):
    pass

class HomeHandler(BaseHandler):
    def get(self):
        entities = db.Query(Entry).order("-published").fetch(limit=10)
        self.render("home.html", entities = entities)