#coding:utf-8
import controllers
from models import Entry, db, User
from tornado.web import authenticated
import datetime

class AdminBaseHandler(controllers.BaseHandler):
    def view(self, template_name, **kwargs):
        if "navIndex" not in kwargs:
            kwargs["navIndex"] = 0
        if "menuIndex" not in kwargs:
            kwargs["menuIndex"] = 0
        super(AdminBaseHandler, self).view(template_name, **kwargs)

class HomeHandler(AdminBaseHandler):
    @authenticated
    def get(self):
        self.view("admin/home.html")

class RegisterHandler(AdminBaseHandler):
    def get(self):
        self.view("admin/register.html", error="", email="")

    def post(self):
        canRegister = db.Query(User).count() == 0
        if canRegister is False:
            return self.view("admin/register.html", error=u"目前只支持单用户,无法再注册", email="")

        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        User(email=email, password=password, nickname=email).put()
        self.dispatch(msg=u"注册成功", to="登录页", toUrl="/admin/login")
            
class LoginHandler(AdminBaseHandler):
    def get(self):
        canRegister = db.Query(User).count() == 0
        self.view("admin/login.html", error=None, email="", canRegister=canRegister)
            
    def post(self):
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        user = User.gql("WHERE email = :1 AND password = :2", email, password).get()
        if user:
            user.lastLoginTime = datetime.datetime.now()
            user.lastLoginIp = self.request.remote_ip
            user.put()
            self.set_secure_cookie(self.settings["auth_cookie_name"], email, httponly=True)
            self.redirect("/admin")
        else:
            self.view("admin/login.html", error=u"用户名或密码错误", email=email, canRegister=True)
        
class LogoutHandler(AdminBaseHandler):
    @authenticated
    def get(self):
        self.clear_cookie(self.settings["auth_cookie_name"])
        self.redirect("/")
        
class ProfileHandler(AdminBaseHandler):
    @authenticated
    def get(self):
        email = self.get_current_user()
        user = User.gql("WHERE email = :1", email).get()
        if user is None:
            self.send_error(404)
        else:
            self.view("admin/profile.html", user=user,navIndex=1, menuIndex=2, error="")

    def post(self):
        email = self.get_current_user()
        user = User.gql("WHERE email = :1", email).get()
        nickname = self.get_argument("nickname", None)
        if nickname:
            try:
                user.nickname = nickname
                user.put()
                self.dispatch(msg=u"保存成功", to=u"账户信息页", toUrl="/admin/profile", seconds=2)
            except Exception as e:
                self.view("admin/profile.html", user=user,navIndex=1, menuIndex=2, error=e)
        else:
            self.view("admin/profile.html", user=user,navIndex=1, menuIndex=2, error=u"昵称不能为空")
        
class ArticleHandler(AdminBaseHandler):
    @authenticated
    def get(self):
        entities = db.Query(Entry).order("-published").fetch(limit=10)
        self.view("admin/article.html", menuIndex=1, entities=entities)
        
class ArticleNewHandler(AdminBaseHandler):
    @authenticated
    def get(self):
        self.view("admin/article-new.html", menuIndex=1)
        
    @authenticated
    def post(self):
        title = self.get_argument("title", default=None)
        if title is None or len(title) == 0:
            self.view("admin/article-new.html", menuIndex=1, error=u"请输入标题")
            return
        
        email = self.get_current_user()
        user = User.gql("WHERE email = :1", email).get()

        source = self.get_argument("cleanSource", default=None)
        html = self.get_argument("content", default=None)
        entry = Entry(author=user.key(),
            slug=source.replace("\r\n", " ").replace("\t", "  ")[0:200], 
            title=title, 
            html=html, 
            body_source=source)
        try:
            entry.put()
            self.dispatch(msg=u"创建成功", to=u"文章列表页", toUrl="/admin/article", seconds=2)
        except:
            self.view("admin/article-new.html", menuIndex=1, error=u"创建失败")
        
class ArticleEditHandler(AdminBaseHandler):
    @authenticated
    def get(self, key):
        try:
            entry = Entry.get(key)
            self.view("admin/article-edit.html", key=key,entry=entry, menuIndex=1)
        except:
            self.send_error(500, exception="没有找到此文章")
            
    def post(self, key):
        entry = Entry.get(key)
        
        title = self.get_argument("title", default=None)
        if title is None or len(title) == 0:
            self.view("admin/article-edit.html", menuIndex=1, error=u"请输入标题")
            return
        source = self.get_argument("cleanSource", default="没有内容")
        html = self.get_argument("content", default="<h4>没有内容</h4>")
        slug = self.get_argument("slug", default="没有内容")

        entry.title = title
        entry.body_source = source
        entry.html = html
        entry.slug = slug
        entry.updated = datetime.datetime.now()
        entry.put()
        self.redirect("/admin/article")
        
class ArticleDeleteHandler(AdminBaseHandler):
    @authenticated
    def get(self, key):
        try:
            entry = Entry.get(key)
            entry.delete()
            self.json({"success":1})
        except:
            self.json({"success":0, "error": "参数错误"})
    
routes = [
    (r"/admin[/]*", HomeHandler),
    (r"/admin/register", RegisterHandler),
    (r"/admin/profile", ProfileHandler),
    (r"/admin/login", LoginHandler),
    (r"/admin/logout", LogoutHandler),
    (r"/admin/article", ArticleHandler),
    (r"/admin/article/new", ArticleNewHandler),
    (r"/admin/article/edit/(.+)", ArticleEditHandler),
    (r"/admin/article/delete/(.+)", ArticleDeleteHandler),
]
    

