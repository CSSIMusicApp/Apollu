from google.appengine.ext import ndb
import user

class Friends(ndb.Model):
    follower: ndb.KeyProperty(user.User)
    followee: ndb.KeyProperty(user.User)
    date: ndb.DateTimeProperty(auto_now_add=True)
