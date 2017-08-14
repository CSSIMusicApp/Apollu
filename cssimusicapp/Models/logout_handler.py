import webapp2
import jinja2
import urllib2
from google.appengine.api import users


env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

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
