import tornado.web
from google.appengine.api import users

class AdminBaseHandler(tornado.web.RequestHandler):
    def view(self, template_name, **kwargs):
        if "navIndex" not in kwargs:
            kwargs["navIndex"] = -1
        self.render(template_name, **kwargs)

class HomeHandler(AdminBaseHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            self.redirect(users.create_login_url("/admin/"))
        else:
            self.view("admin/home.html", navIndex = 0)
            
class LogoutHandler(AdminBaseHandler):
    def get(self):
        self.redirect(users.create_logout_url("/"))
        
class ProfileHandler(AdminBaseHandler):
    def get(self):
        self.view("admin/profile.html", user=users.get_current_user())
        
routes = [
    (r"/admin[/]*", HomeHandler),
    (r"/admin/profile", ProfileHandler),
    (r"/admin/logout", LogoutHandler),
]
    

