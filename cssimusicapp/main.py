#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import webapp2
import jinja2
import urllib2
import datetime
from models import User, Article, ArticleCreatorHandler, UserCreatorHandler, LogOutHandler, ProfileHandler, ArticleHandler
from google.appengine.api import users

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        interestselected = self.request.get('interest')

        if not interestselected:
            self.redirect('/?interest=all')
    #set on main handler too to change value of 'Log In/Log Out'
        user = users.get_current_user()
        currentuser = ''

        template = env.get_template('home.html')
        article_data = Article.query(Article.tags == interestselected).order(-Article.date).fetch(limit=5)
        video_IDs = list()

    #if logged in(data with post option and "logout") else "LogIn" and keep everything

        for article in article_data:
            if article.articletype == 'youtube':
                video_IDs.append(article.post)

        if user:
            page_users = []
            articles = []
            user_data = User.query().fetch()
            currentuser = User.query(User.email == user.email()).get()
            #common_data = User.query(User.common).fetch()
            #print('Common Data: %d') %(common_data)

            #print article_key

            for user in user_data:
                user = {
                    'username': user.username,
                    'interests': user.interests,
                }
                page_users.append(user)

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
                "title": "Name",
                "login": '<li id="menu"><a href="%s">Log Out</a></li>' %(users.create_logout_url('/loggedout')),
                "post_label": '<li id="menu"><a href="%s">Post</a></li>' %('/createarticle'),
                "profile_label": '<li id="menu"><a href="%s">Profile</a></li>' %("/profile?name=" + currentuser.username),
                "users": page_users,
                "articles": articles,
                "user": user,
                "video_div": '<div id="player"></div>',
                "video_IDs": video_IDs,
                "articles": articles,
                "currentuser": currentuser,
                "currentinterest": interestselected
            }
        else:
            page_users = []
            articles = []
            user_data = User.query().fetch()
            article_data = Article.query().order(-Article.date).fetch(limit=5)
            currentuser = {
            "username": "Blank",
            "interests": ["Log in to see your interests."]
            }

            for user in user_data:
                user = {
                    'username': user.username,
                    'interests': user.interests
                }
                page_users.append(user)

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
                "title": "Name",
                "login": '<li id="right"><a href="%s">Log In</a></li>' %(users.create_login_url('/usercreate')),
                "post_label": '<li></li>',
                "profile_label": '<li></li>',
                "player_count": 0,
                "video_IDs": video_IDs,
                "users": page_users,
                "user": user,
                "articles": articles,
                "currentuser": currentuser
            }

        self.response.write(template.render(vars))

    def post(self):
        interestselected = self.request.get('interest')
        if not interestselected:
            self.redirect('/?interest=all')
        user = users.get_current_user()
        limit = int(self.request.get('limit') or '10')
        article_data = Article.query(Article.tags == interestselected).order(-Article.date).fetch(limit=limit)
        template = env.get_template('home.html')
        if user:
            currentuser = User.query(User.email == user.email()).get()
        else:
            currentuser = {
            "username": "Blank",
            "interests": ["Log in to see your interests."]
            }
        video_IDs = list()

    #if logged in(data with post option and "logout") else "LogIn" and keep everything

        for article in article_data:
            if article.articletype == 'youtube':
                video_IDs.append(article.post)

        if user:

            page_users = []
            articles = []
            user_data = User.query().fetch()
            currentuser = User.query(User.email == user.email()).get()

            #common_data = User.query(User.common).fetch()
            #print('Common Data: %d') %(common_data)

            #print article_key

            for user in user_data:
                user = {
                    'username': user.username,
                    'interests': user.interests,
                }
                page_users.append(user)

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
                "title": "Name",
                "login": '<li id="menu"><a href="%s">Log Out</a></li>' %(users.create_logout_url('/loggedout')),
                "post_label": '<li id="menu"><a href="%s">Post</a></li>' %('/createarticle'),
                "profile_label": '<li id="menu"><a href="%s">Profile</a></li>' %('/profile'),
                "users": page_users,
                "articles": articles,
                "user": user,
                "video_div": '<div id="player"></div>',
                "next_limit": limit + 5,
                "video_IDs": video_IDs,
                "articles": articles,
                "currentuser": currentuser
            }
        else:
            page_users = []
            articles = []
            user_data = User.query().fetch()
            currentuser = {
            "username": "Blank",
            "interests": ["Log in to see your interests."]
            }


            for user in user_data:
                user = {
                    'username': user.username,
                    'interests': user.interests
                }
                page_users.append(user)

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
                "title": "Name",
                "login": '<li id="right"><a href="%s">Log In</a></li>' %(users.create_login_url('/usercreate')),
                "post_label": '<li></li>',
                "profile_label": '<li></li>',
                "player_count": 0,
                "video_IDs": video_IDs,
                "users": page_users,
                "next_limit": limit + 5,
                "user": user,
                "articles": articles,
                "currentuser": currentuser
            }

        #AJAX 'POST' stops request
        #self.redirect('/')
        self.response.write(template.render(vars))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/createarticle', ArticleCreatorHandler),
    ('/usercreate', UserCreatorHandler),
    ('/loggedout', LogOutHandler),
    ('/profile', ProfileHandler),
    ('/article', ArticleHandler)
], debug=True)
