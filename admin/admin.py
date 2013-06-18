import tornado.web

class AdminBaseHandler(tornado.web.RequestHandler):
    pass

class HomeHandler(AdminBaseHandler):
    def get(self):
        self.render("admin/base.html")

class LoginHandler(AdminBaseHandler):
    def get(self):
        self.render("admin/login.html")
        
    def post(self):
        username = self.get_argument("username", default=None)
        
        password = self.get_argument("password", default=None)
        
        self.write(username + password)
    
        
routes = [
    (r"/admin[/]*", HomeHandler),
    (r"/admin/login", LoginHandler),
]
    

