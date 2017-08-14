import webapp2
import jinja2
import urllib2
from google.appengine.api import users
from user import User

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

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
