from google.appengine.ext import ndb

class Article(ndb.Model):
    article_name = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True)
    post = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    comments = ndb.StringProperty(repeated=True)
    user = ndb.KeyProperty()
    
