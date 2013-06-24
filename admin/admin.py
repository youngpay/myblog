#coding:utf-8
import controllers
from models import Entry, db
from google.appengine.api import users

class AdminBaseHandler(controllers.BaseHandler):
    def view(self, template_name, **kwargs):
        if "navIndex" not in kwargs:
            kwargs["navIndex"] = 0
        if "menuIndex" not in kwargs:
            kwargs["menuIndex"] = 0
        super(AdminBaseHandler, self).view(template_name, **kwargs)

class HomeHandler(AdminBaseHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            self.redirect(users.create_login_url("/admin/"))
        else:
            self.view("admin/home.html")
            
class LogoutHandler(AdminBaseHandler):
    def get(self):
        self.redirect(users.create_logout_url("/"))
        
class ProfileHandler(AdminBaseHandler):
    def get(self):
        self.view("admin/profile.html", user=users.get_current_user(),navIndex=1, menuIndex=4)
        
class ArticleHandler(AdminBaseHandler):
    def get(self):
        entities = db.Query(Entry).order("-published").fetch(limit=10)
        self.view("admin/article.html", menuIndex=1, entities=entities)
        
class ArticleNewHandler(AdminBaseHandler):
    def get(self):
        self.view("admin/article-new.html", menuIndex=1)
        
    def post(self):
        title = self.get_argument("title", default=None)
        if title is None or len(title) == 0:
            self.view("admin/article-new.html", menuIndex=1, error=u"请输入标题")
            return
        
        source = self.get_argument("cleanSource", default=None)
        html = self.get_argument("content", default=None)
        entry = Entry(author=users.get_current_user(), slug=source.replace("\r\n", " ").replace("\t", "  ")[0:200], title=title, html=html, body_source=source)
        try:
            entry.put()
            self.redirect("/admin/article")
        except:
            self.view("admin/article-new.html", menuIndex=1, error=u"创建失败")
        
class ArticleEditHandler(AdminBaseHandler):
    def get(self):
        self.redirect("/admin/article")
        
class ArticleDeleteHandler(AdminBaseHandler):
    def get(self):
        self.redirect("/admin/article")
    
class TagHandler(AdminBaseHandler):
    def get(self):
        self.view("admin/tag.html", menuIndex=2)
        
class CatalogHandler(AdminBaseHandler):
    def get(self):
        self.view("admin/catalog.html", menuIndex=3)
        
routes = [
    (r"/admin[/]*", HomeHandler),
    (r"/admin/profile", ProfileHandler),
    (r"/admin/logout", LogoutHandler),
    (r"/admin/article", ArticleHandler),
    (r"/admin/tag", TagHandler),
    (r"/admin/catalog", CatalogHandler),
    (r"/admin/article/new", ArticleNewHandler),
    (r"/admin/article/edit/(.+)", ArticleEditHandler),
    (r"/admin/article/delete/(.+)", ArticleDeleteHandler),
]
    

