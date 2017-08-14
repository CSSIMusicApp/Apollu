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
from models import User, Article, ArticleCreatorHandler, UserCreatorHandler, LogOutHandler
from google.appengine.api import users

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
    #set on main handler too to change value of 'Log In/Log Out'
        user = users.get_current_user()
        template = env.get_template('home.html')

    #if logged in(data with post option and "logout") else "LogIn" and keep everything

        if user:

            page_users = []
            articles = []
            user_data = User.query().fetch()
            #common_data = User.query(User.common).fetch()
            #print('Common Data: %d') %(common_data)

            article_data = Article.query().order(-Article.date).fetch()
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
                    'user': user
                }
                articles.append(article)

            vars = {
                "title": "Name",
                "login": '<li id="menu"><a href="%s">Log Out</a></li>' %(users.create_logout_url('/loggedout')),
                "post_label": '<li id="menu"><a href="%s">Post</a></li>' %('/createarticle'),
                "profile_label": '<li id="menu"><a href="%s">Profile</a></li>' %('/profile'),
                "users": page_users,
                "articles": articles
            }
        else:
            page_users = []
            articles = []
            user_data = User.query().fetch()
            article_data = Article.query().order(-Article.date).fetch()

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
                    'user': user
                }
                articles.append(article)

            vars = {
                "title": "Name",
                "login": '<li id="right"><a href="%s">Log In</a></li>' %(users.create_login_url('/usercreate')),
                "post_label": '<li></li>',
                "profile_label": '<li></li>',
                "users": page_users,
                "articles": articles
            }

        self.response.write(template.render(vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/createarticle', ArticleCreatorHandler),
    ('/usercreate', UserCreatorHandler),
    ('/loggedout', LogOutHandler)
], debug=True)
