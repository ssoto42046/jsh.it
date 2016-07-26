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
        if user:
            self.response.out.write(template.render())
            #after the user logs in, the website will be redirected to the
            #mainHandler page (which has all the options and etc.) there will
            #also be a 'signout' option which will redirect to the 'signin' page
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


app = webapp2.WSGIApplication([
    ('/', signIn),
    #('/mainHandler', mainHandler),
    ('/signOutHandler', signOutHandler)

], debug=True)
