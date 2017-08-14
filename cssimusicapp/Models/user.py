from google.appengine.ext import ndb

class User(ndb.Model):
    username = ndb.StringProperty()
    interests = ndb.StringProperty(repeated=True)
    email = ndb.StringProperty()
    common = ndb.IntegerProperty()
    favorites = ndb.KeyProperty(repeated=True)
    # image = ndb.StringProperty()
