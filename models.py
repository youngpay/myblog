from google.appengine.ext import db

class Entry(db.Model):
    """A single blog entry."""
    author = db.UserProperty()
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    body_source = db.TextProperty(required=True)
    html = db.TextProperty(required=True)
    published = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    
class User(db.Model):
    """User Model"""
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    email = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    nickname = db.StringProperty(required=True)
    lastLoginTime = db.DateTimeProperty(auto_now=True)
    lastLoginIp = db.StringProperty()
