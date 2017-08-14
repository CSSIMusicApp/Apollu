import webapp2
import jinja2
import urllib2
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from random import *

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
user = users.get_current_user()

class Article(ndb.Model):
    article_name = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True)
    post = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    comments = ndb.StringProperty(repeated=True)
    id = ndb.IntegerProperty()

class Friends(ndb.Model):
    follower = ndb.KeyProperty()
    followee = ndb.KeyProperty()
    date = ndb.DateTimeProperty()

class User(ndb.Model):
    username = ndb.StringProperty()
    interests = ndb.StringProperty(repeated=True)
    email = ndb.StringProperty()
    common = ndb.IntegerProperty()
    favorites = ndb.KeyProperty(repeated=True)
    # image = ndb.StringProperty()


class ArticleCreatorHandler(webapp2.RequestHandler):
    def get(self):
        #template variable and html file will change
        template = env.get_template('createarticle.html')
        self.response.write(template.render({"title": 'Name'}))

    def post(self):

        spotifyinput = self.request.get('spotify-data')
        youtubeinput = self.request.get('youtube-data')
        textinput = self.request.get('text-data')
        spotifybase = "https://open.spotify.com/embed?uri="

        if not spotifyinput and not youtubeinput:
            template = env.get_template('textarticle.html')
            articledata = textinput

        if not spotifyinput and not textinput:
            template = env.get_template('youtubearticle.html')
            articledata = youtubeinput

        if not textinput and not youtubeinput:
            template = env.get_template('spotifyarticle.html')
            articledata = spotifyinput

        # i=0
        # while i<1:
        #     idtemp = randint(0, 10001)
        #
        #     if not Article.query(Article.id == idtemp).article_name:
        #         i=0
        #     else:
        #         i=1

            #change with database info
        idtemp = randint(0, 1000001)

        article = Article(
            article_name = self.request.get('article_name'),
            post = articledata,
            date = datetime.datetime.now(),
            id = idtemp
        )

        article.put()

        self.redirect('/')

class UserCreatorHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        user_data = User.query().fetch()

        for db_user in user_data:
            if db_user.email == user.email():
                pass
                self.redirect('/')

        vars = {"title": "Name"}
        template = env.get_template('signup.html')
        self.response.write(template.render(vars))

    #post change
    def post(self):

        user = User(
            username = self.request.get('username'),
            interests = self.request.get('interests'),
            email = self.request.get('email')
        )

        user.put()

        self.redirect('/')

class LogOutHandler(webapp2.RequestHandler):
    def get(self):

        vars = {
            "title": "Name",
            #change
            "username": "username",
            "login": '<li id="right"><a href="%s">Log In</a></li>' %(users.create_login_url('/usercreate')),
            "post_label": '<li></li>'
        }
        template = env.get_template('logged_out.html')
        self.response.write(template.render(vars))
