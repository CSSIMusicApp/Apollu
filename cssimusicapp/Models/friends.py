from google.appengine.ext import ndb

class Friends(ndb.Model):
    follower: ndb.KeyProperty()
    followee: ndb.KeyProperty()
    date: ndb.DateTimeProperty()
