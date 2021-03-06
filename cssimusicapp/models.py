import webapp2
import jinja2
import urllib2
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from random import *
import logging

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class Article(ndb.Model):
    article_name = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True)
    post = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    comments = ndb.StringProperty(repeated=True)
    articletype = ndb.StringProperty()
    user = ndb.StringProperty()
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
    #favorites = ndb.KeyProperty(repeated=True)
    # image = ndb.StringProperty()

class Comment(ndb.Model):
    user = ndb.StringProperty()
    comment_data = ndb.StringProperty()
    article = ndb.StringProperty()
    date = ndb.DateTimeProperty()


class ArticleCreatorHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        #template variable and html file will change
        template = env.get_template('createarticle.html')
        self.response.write(template.render({"title": 'Name'}))

    def post(self):
        user = users.get_current_user()
        youtubeinput = self.request.get('youtube-data')
        textinput = self.request.get('text-data')
        tagsinput = self.request.get('tags').lower() + ", all"

        if not youtubeinput:
            template = env.get_template('textarticle.html')
            articletype = "text"
            articledata = textinput

        if not textinput:
            template = env.get_template('youtubearticle.html')
            articletype = "youtube"
            articledata = youtubeinput

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
        currentuser = User.query(User.email == users.get_current_user().email()).get()
        if not currentuser:
            currentUserName = ''
        else:
            currentUserName = currentuser.username

        article = Article(
            article_name = self.request.get('article_name'),
            post = articledata,
            date = datetime.datetime.now(),
            id = idtemp,
            articletype = articletype,
            user = currentuser.username,
            tags = tagsinput.split(', ')
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
            interests = self.request.get('interests').lower().split(', '),
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

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('name')
        usergrabbed = User.query(User.username == username)
        user = usergrabbed.get()
        currentuser = User.query(User.email == user.email).get()
        articles = []
        article_data = Article.query(Article.user == username).order(-Article.date).fetch()
        friends = Friends.query(Friends.follower == currentuser.key).fetch()
        friends_data = []
        video_IDs = list()
        for friend in friends:
            # f = User.query(User.key == friend.key).get()
            f = friend.followee.get()
            friends_data.append(f)

        for article in article_data:
            if article.articletype == 'youtube':
                video_IDs.append(article.post)

        for article in article_data:
            article = {
                'article_name': article.article_name,
                'tags': article.tags,
                'post': article.post,
                'articletype': article.articletype,
                'user': user
            }
            articles.append(article)



        vars = {
        "name": user.username,
        "interests": user.interests,
        "friends": friends_data,
        #Friends
        #articles
        #profile pictures
        "articles": articles,
        "video_IDs": video_IDs,
        "title": "Name",
        "login": '<li id="menu"><a href="%s">Log Out</a></li>' %(users.create_logout_url('/loggedout')),
        "post_label": '<li id="menu"><a href="%s">Post</a></li>' %('/createarticle')
        }
        template = env.get_template('profile.html')
        self.response.write(template.render(vars))

    def post(self):
        username = self.request.get('name')
        user = users.get_current_user()
        # get follower and followee from database
        followee = User.query(User.username == username).get()
        follower = User.query(User.email == user.email()).get()
        article_data = Article.query(Article.user == username).order(-Article.date).fetch()

        friend = Friends(
            followee= followee.key,
            follower= follower.key
        )
        friend.put()
        self.redirect("/profile?name=%s" %(username))



class ArticleHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        articlename = self.request.get('name')
        articlegrabbed = Article.query(Article.article_name == articlename)
        article = articlegrabbed.get()
        comments = Comment.query(Comment.article == articlename).order(-Comment.date).fetch()

        if comments == None:
            vars = {
            "user_username": article.user,
            "name": article.article_name,
            "tags": article.tags,
            "post": article.post,
            "comment": "",
            "comment-date": ""
            }
        else:
            vars = {
            "user_username": article.user,
            "name": article.article_name,
            "tags": article.tags,
            "post": article.post,
            "comments": comments
            }

        if article.articletype == "text":
            template = env.get_template('textarticle.html')
        elif article.articletype == "youtube":
            template = env.get_template('youtubearticle.html')
        self.response.write(template.render(vars))

    def post(self):
        user = users.get_current_user()
        comment = self.request.get('comment-data')
        article_name = self.request.get('article_name')

        if user:
            currentuser = User.query(User.email == user.email()).get()

            print currentuser

            comment_data = Comment(
                user = currentuser.username,
                comment_data = comment,
                article = article_name,
                date = datetime.datetime.now()
            )

            comment_data.put()
        else:
            currentuser = {
            "username": "Blank",
            "interests": ["Log in to see your interests."]
            }

            print currentuser

            comment_data = Comment(
                user = currentuser['username'],
                comment_data = comment,
                article = article_name,
                date = datetime.datetime.now()
            )

            comment_data.put()

        self.redirect('/article?name=%s' %(article_name))
