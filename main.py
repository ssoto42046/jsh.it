from google.appengine.api import users
import webapp2
import jinja2

#this is the line of code that allows for you to connect the main.py with the templates

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))


# the signIn class is taken from the 'googleusers' lab we did in class
# also (going to create) a template to make the pages in the 'if' () and 'else'
# statements look nicer
class signIn(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        # if user:
            # greeting = ('Get ready to post.it, %s! (<a href="%s">sign out</a>)' %
            #       (user.nickname(), users.create_logout_url('/')))

        template = env.get_template('mainHandler.html')
        if user:  # If the user exists.
            self.response.out.write(template.render())
        else:
            template = env.get_template('signIn.html')
            greeting = ('<button class="btnExample" align=center><a href="%s">Sign in</a></button>' % users.create_login_url('/'))
            self.response.out.write('<html><body>%s</body></html>' % greeting)
            self.response.out.write(template.render())

        # else:
        #     greeting = ('<a href="%s">Sign in or register</a>.' %
        #         users.create_login_url('/')
        #     self.response.out.write('<html><body>%s</body></html>' % greeting)
            #we just need to edit the CSS so it looks nicer

# the mainHandler class will be the page that allows the user to post photos/statuses
# and the list of all the social media apps will be displayed on this page as well
# you will also need to link the facebook/twitter/etc handlers and htmls to this class

class signOutHandler(webapp2.RequestHandler):
    def get(self):
        signouturl = users.create_logout_url('/')
        self.redirect(signouturl)
        #self.response.out.write('<html><body>%s</body></html>' % greeting)

class twitterHandler(webapp2.RequestHandler):
    def get(self):
        main_template = env.get_template('twitter.html')
        self.response.out.write(main_template.render())
    def post(self):
        main_template = env.get_template('twitterResult.html')
        template_variables = {
            'TwitterLink':self.request.get("TwitterLink"),
            }
        if template_variables['TwitterLink'] != "":
            template_variables['TwitterLink'] = template_variables['TwitterLink'][20:]
            print template_variables['TwitterLink']
            url = ('<a class="twitter-timeline" href="https://twitter.com/%s"></a> <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>' % template_variables['TwitterLink'])
            print url
            self.response.out.write(url)
        else:
            self.redirect("/")
        self.response.out.write(main_template.render(template_variables))

class youtubeHandler(webapp2.RequestHandler):
    def get(self):
        main_template = env.get_template('youtube.html')
        self.response.out.write(main_template.render())
    def post(self):
        main_template = env.get_template('result.html')
        template_variables = {
            'YoutubeLink':self.request.get("YoutubeLink"),
            }
        if template_variables['YoutubeLink'] != "":
            indexofequal = template_variables['YoutubeLink'].index('=')
            template_variables['YoutubeLink'] = template_variables['YoutubeLink'][indexofequal+1:]
            # print template_variables['YoutubeLink']
            url = ('<iframe width="420" height="315" src="https://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>' % template_variables['YoutubeLink'])
            self.response.out.write(url)
        else:
            self.redirect("/")
        self.response.out.write(main_template.render(template_variables))

class pinterestHandler(webapp2.RequestHandler):
    def get(self):
        main_template = env.get_template('pinterest.html')
        self.response.out.write(main_template.render())
    def post(self):
        main_template = env.get_template('pinterestResult.html')
        template_variables = {
            'PinterestLink':self.request.get("PinterestLink"),
            }
        if template_variables['PinterestLink'] != "":
            # template_variables['TwitterLink'] = template_variables['TwitterLink'][20:]
            # print template_variables['TwitterLink']
            url = ('<a data-pin-do="embedUser" data-pin-board-width="400" data-pin-scale-height="240" data-pin-scale-width="80" href="%s"></a>' % template_variables['PinterestLink'])
            print url
            self.response.out.write(url)
        else:
            self.redirect("/")
        self.response.out.write(main_template.render(template_variables))

app = webapp2.WSGIApplication([
    ('/', signIn),
    #('/mainHandler', mainHandler),
    ('/signOutHandler', signOutHandler),
    ('/Twitter', twitterHandler),
    ('/Youtube', youtubeHandler),
    ('/Pinterest', pinterestHandler)

], debug=True)
