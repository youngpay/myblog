from google.appengine.ext import db

class User(db.Model):
    """User Model"""
    email = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    nickname = db.StringProperty(required=True)
    lastLoginTime = db.DateTimeProperty()
    lastLoginIp = db.StringProperty()

class Entry(db.Model):
    """A single blog entry."""
    author = db.ReferenceProperty(User)
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    body_source = db.TextProperty(required=True)
    html = db.TextProperty(required=True)
    published = db.DateTimeProperty()
    updated = db.DateTimeProperty()