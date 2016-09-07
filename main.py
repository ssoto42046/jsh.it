# https://cloud.google.com/appengine/docs/python/console/managing-datastore
# delete embedded social media from deployed appspot^^


from google.appengine.api import users
import webapp2
import jinja2
from twitter_model import Twitter_models
from pinterest_model import Pinterest_models
from youtube_model import Youtube_models
from google.appengine.ext import ndb
import logging

#this is the line of code that allows for you to connect the main.py with the templates

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))


# the signIn class is taken from the 'googleusers' lab we did in class
# also (going to create) a template to make the pages in the 'if' () and 'else'
# statements look nicer
class signIn(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = env.get_template('mainHandler.html')
        if user:
            self.response.out.write(template.render())
        else:
            template = env.get_template('signIn.html')
            greeting = ('<a href="%s"></a>' % users.create_login_url('/'))
            self.response.out.write('<html><body>%s</body></html>' % greeting)
            variables = {
                "login" : users.create_login_url('/')
            }
            self.response.out.write(template.render(variables))

# the mainHandler class will be the page that allows the user to post photos/statuses
# and the list of all the social media apps will be displayed on this page as well
# you will also need to link the facebook/twitter/etc handlers and htmls to this class
class signOutHandler(webapp2.RequestHandler):
    def get(self):
        signouturl = users.create_logout_url('/')
        self.redirect(signouturl)

class twitterHandler(webapp2.RequestHandler):
    def get(self):
        pos = self.request.get("position")
        twitter_list = self.fetchUrls(pos)
        return self.render(pos, twitter_list)
    def post(self):
        pos = self.request.get("position")
        user = users.get_current_user().nickname()
        twitter_link = self.request.get("TwitterLink")
        if twitter_link != "":
            twitter_list = self.fetchUrls(pos)
            twitter_link = twitter_link[20:]
            twitter_link = '<a class="twitter-timeline" href="https://twitter.com/%s"></a> <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>' % twitter_link
            for twitter in twitter_list:
                if twitter.link==twitter_link:
                    self.render(pos, twitter_list)
                    return
            url = Twitter_models(link = twitter_link, author=user, position=int(pos))
            twitter_list.append(url)
            self.render(pos, twitter_list)
            url.put()
        else:
            self.redirect("/Twitter")

    def fetchUrls(self, pos):
        user = users.get_current_user().nickname()
        query = Twitter_models.query()
        query = query.filter(ndb.AND(Twitter_models.author==user))
        return query.fetch()

    def render(self, pos, urls):
        main_template = env.get_template('twitter.html')
        template_variables = {
            'TwitterLink':self.request.get("TwitterLink"),
            'position': pos,
            'urls': urls,
            }
        self.response.out.write(main_template.render(template_variables))

class youtubeHandler(webapp2.RequestHandler):
    def get(self):
        pos = self.request.get("position")
        youtube_list = self.fetchUrls(pos)
        return self.render(pos, youtube_list)
    def post(self):
        pos = self.request.get("position")
        user = users.get_current_user().nickname()
        youtube_link = self.request.get("YoutubeLink")
        if youtube_link != "":
            youtube_list = self.fetchUrls(pos)
            indexofequal = youtube_link.index('=')
            youtube_link = youtube_link[indexofequal+1:]
            youtube_link = '<iframe width="420" height="315" src="https://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>' % youtube_link
            for youtube in youtube_list:
                if youtube.link==youtube_link:
                    self.render(pos, youtube_list)
                    return
            print youtube_link
            url = Youtube_models(link = youtube_link, author=user, position=int(pos))
            youtube_list.append(url)
            self.render(pos, youtube_list)
            url.put()
        else:
            self.redirect("/Youtube")

    def fetchUrls(self, pos):
        user = users.get_current_user().nickname()
        query = Youtube_models.query()
        query = query.filter(ndb.AND(Youtube_models.author==user))
        return query.fetch()

    def render(self, pos, urls):
        main_template = env.get_template('youtube.html')
        template_variables = {
            'YoutubeLink':self.request.get("YoutubeLink"),
            'position': pos,
            'urls': urls,
            }
        self.response.out.write(main_template.render(template_variables))

class pinterestHandler(webapp2.RequestHandler):
    def get(self):
        pos = self.request.get("position")
        pinterest_list = self.fetchUrls(pos)
        return self.render(pos, pinterest_list)
    def post(self):
        pos = self.request.get("position")
        user = users.get_current_user().nickname()
        pinterest_link = self.request.get("PinterestLink")
        if pinterest_link != "":
            pinterest_list = self.fetchUrls(pos)
            pinterest_link = pinterest_link
            pinterest_link = '<a data-pin-do="embedUser" data-pin-board-width="400" data-pin-scale-height="240" data-pin-scale-width="80" href="%s"></a>' % pinterest_link
            for pinterest in pinterest_list:
                if pinterest.link==pinterest_link:
                    self.render(pos, pinterest_list)
                    return
            print pinterest_link
            url = Pinterest_models(link = pinterest_link, author=user, position=int(pos))
            pinterest_list.append(url)
            self.render(pos, pinterest_list)
            url.put()
        else:
            self.redirect("/Pinterest")

    def fetchUrls(self, pos):
        user = users.get_current_user().nickname()
        query = Pinterest_models.query()
        query = query.filter(ndb.AND(Pinterest_models.author==user))
        return query.fetch()

    def render(self, pos, urls):
        main_template = env.get_template('pinterest.html')
        template_variables = {
            'PinterestLink':self.request.get("PinterestLink"),
            'position': pos,
            'urls': urls,
            }
        self.response.out.write(main_template.render(template_variables))

class aboutUsHandler(webapp2.RequestHandler):
    def get(self):
        main_template = env.get_template('aboutUs.html')
        self.response.out.write(main_template.render())

class aboutItHandler(webapp2.RequestHandler):
    def get(self):
        main_template = env.get_template('aboutIt.html')
        self.response.out.write(main_template.render())

class howToUseHandler(webapp2.RequestHandler):
    def get(self):
        main_template = env.get_template('howToUse.html')
        self.response.out.write(main_template.render())

app = webapp2.WSGIApplication([
    ('/', signIn),
    ('/signOutHandler', signOutHandler),
    ('/Twitter', twitterHandler),
    ('/Youtube', youtubeHandler),
    ('/Pinterest', pinterestHandler),
    ('/aboutUs', aboutUsHandler),
    ('/aboutIt', aboutItHandler),
    ('/howToUse', howToUseHandler),

], debug=True)
