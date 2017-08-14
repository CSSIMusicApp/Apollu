import webapp2
import jinja2
import urllib2
from article import Article
import datetime

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

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

            #change with database info
        article = Article(
            article_name = self.request.get('article_name'),
            post = articledata,
            date = datetime.datetime.now()
        )

        article.put()

        self.redirect('/')
