from google.appengine.api import users
import webapp2
#import jinja2

# the signIn class is taken from the 'googleusers' lab we did in class
# also (going to create) a template to make the pages in the 'if' () and 'else'
# statements look nicer
class signIn(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                (user.nickname(), users.create_logout_url('/mainHandler'))) #this should be our mainHandler page

            greeting = ('<a href="%s">Sign in or register</a>.' %
                users.create_login_url('/')) #we just need to edit the CSS so it looks nicer

        self.response.out.write('<html><body>%s</body></html>' % greeting)

app = webapp2.WSGIApplication([
    ('/', signIn),
    #('/mainHandler', mainHandler )
], debug=True)
