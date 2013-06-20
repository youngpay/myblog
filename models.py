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
    email = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    displayname = db.StringProperty()
    lastLoginDate = db.DateTimeProperty(auto_now_add=True)
    lastLoginIp = db.StringProperty()
    
