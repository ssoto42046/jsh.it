from google.appengine.ext import ndb

class Twitter_models(ndb.Model):
    author = ndb.StringProperty(required=True)
    link = ndb.StringProperty(required=True)
    position = ndb.IntegerProperty(required=True)
