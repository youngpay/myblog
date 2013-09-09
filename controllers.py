#coding: utf-8
import tornado.web
from models import db, Entry, User
from tornado.escape import json_encode
import tornado.locale

class BaseHandler(tornado.web.RequestHandler):
    def get_error_html(self, status_code, exception="", **kwargs):
        return self.render_string("error.html", status_code=status_code, ex=exception, themes=self.get_all_themes(), currentTheme=self.get_theme_current())

    def view(self, template_name, **kwargs):
        """自定义输出的方法,替代render,加入几个内置参数
        """
        kwargs["themes"] = self.get_all_themes()
        kwargs["currentTheme"] = self.get_theme_current()
        self.render(template_name, **kwargs)

    def dispatch(self, msg="正在加载", to=None, toUrl="/", seconds=3):
        self.view("dispatch.html", msg=msg,to=to,toUrl=toUrl,seconds=seconds)

    def json(self, value):
        self.set_header("Content-Type", "application/json")
        self.finish(json_encode(value))

    def get_current_user(self):
        """获取当前用户"""
        return self.get_secure_cookie(self.settings["auth_cookie_name"])

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

    def get_user_locale(self):
        return tornado.locale.get("zh_CN")

class ErrorHandler(BaseHandler):
    """Generates an error response with status_code for all requests."""
    def __init__(self, application, request, status_code):
        tornado.web.RequestHandler.__init__(self, application, request)
        self.set_status(status_code)

    def prepare(self):
        raise tornado.web.HTTPError(self._status_code)

## override the tornado.web.ErrorHandler with our default ErrorHandler
tornado.web.ErrorHandler = ErrorHandler

class ThemeInfo():
    def __init__(self, name, display):
        self.name = name
        self.display = display

    name = None
    display = None

class HomeHandler(BaseHandler):
    def get(self, page):
        if len(page) == 0:
            page = 1
        else:
            page = int(page)

        if page == 0:
            return self.redirect('/1')

        pagesize = self.settings["blog_page_size"]
        count = db.Query(Entry).count()
        pageCount = count / pagesize if count % pagesize == 0 else count / pagesize + 1
        entities = db.Query(Entry).order("-published").fetch(limit=pagesize, offset=((page - 1) * pagesize))
        self.view("home.html", entities=entities, page = page, total = pageCount)

class PostHandler(BaseHandler):
    def get(self, key):
        post = Entry.get(key)
        self.view("post.html", post=post)

class ChangeThemeHandler(BaseHandler):
    def get(self, theme):
        theme = self.get_theme_by_name_or_default(theme)
        self.set_cookie("ypbtheme", theme.name)
        self.redirect(self.request.headers.get("referer", default="/"))

class DispatchHandler(BaseHandler):
    def get(self):
        msg = self.get_argument("msg", None)
        to = self.get_argument("to", None)
        toUrl = self.get_argument("toUrl", None)
        seconds = self.get_argument("seconds", None)
        self.dispatch(msg=msg, to=to, toUrl=toUrl, seconds=seconds)

class RssHandler(BaseHandler):
    def get(self):
        from feedformatter import Feed
        import time
        feed = Feed()

        feed.feed["title"] = self.settings["blog_title"]
        feed.feed["link"] = self.settings["blog_url"]
        feed.feed["author"] = "yangpei@gmail.com"
        feed.feed["description"] = u"C#, Objective-C, Python;"

        entities = db.Query(Entry).order("-published").fetch(limit=100)
        for x in entities:
            item = {}
            item["title"] = x.title
            item["link"] = self.settings["blog_url"] + "/post/" + str(x.key())
            item["description"] = x.slug
            item["pubDate"] = x.published
            item["guid"] = str(x.key())
            feed.items.append(item)

        self.set_header("Content-Type", "text/xml")
        self.write(feed.format_rss2_string())

routes = [
    (r"/(\d*)", HomeHandler),
    (r"/post/(.+)", PostHandler),
    (r"/changetheme/(.+)", ChangeThemeHandler),
    (r"/dispatch", DispatchHandler),
    (r"/rss", RssHandler),
]