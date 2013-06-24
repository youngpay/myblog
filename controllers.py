#coding: utf-8
import tornado.web
from models import db, Entry
from google.appengine.api import users

class BaseHandler(tornado.web.RequestHandler):
    def get_error_html(self, status_code, exception=None, **kwargs):
        return self.render_string("error.html", status_code=status_code, ex=exception)
    
    def view(self, template_name, **kwargs):
        """自定义输出的方法,替代render,加入几个内置参数
        """
        kwargs["themes"] = self.get_all_themes()
        kwargs["currentTheme"] = self.get_theme_current()
        self.render(template_name, **kwargs)
        
    def get_current_user(self):
        """获取当前用户,使用的Google用户API
        """
        return users.get_current_user()
    
    def get_all_themes(self):
        return [
            ThemeInfo("default", "白"),
            ThemeInfo("cerulean", "蓝"),
            ThemeInfo("readable","灰" ),
            ThemeInfo("slate","黑"),
        ]
    
    def get_theme_by_name_or_default(self, themename):
        defaultTheme = ThemeInfo("slate","黑")
        
        if themename is None:
            return defaultTheme
        
        search = [x for x in self.get_all_themes() if x.name == themename];
        if len(search) == 0:
            return defaultTheme
        else:
            return search[0]
        
    def get_theme_current(self):
        themeFromCookie = self.get_cookie("ypbtheme", default=None)
        return self.get_theme_by_name_or_default(themeFromCookie)
    
class ThemeInfo():
    def __init__(self, name, display):
        self.name = name
        self.display = display
        
    name = None
    display = None
        
class HomeHandler(BaseHandler):
    def get(self):
        entities = db.Query(Entry).order("-published").fetch(limit=10)
        self.view("home.html", entities=entities)

class PostHandler(BaseHandler):
    def get(self, key):
        post = Entry.get(key)
        self.view("post.html", post=post)
        
class ChangeThemeHandler(BaseHandler):
    def get(self, theme):
        theme = self.get_theme_by_name_or_default(theme)
        self.set_cookie("ypbtheme", theme.name)
        self.redirect(self.request.headers.get("referer", default="/"))

routes = [
    (r"/", HomeHandler),
    (r"/post/(.+)", PostHandler),
    (r"/changetheme/(.+)", ChangeThemeHandler),
]