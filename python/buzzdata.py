
import urllib, urllib2, json

class API:
    def call(self, url, getparams, postparams):
        url += "/?%s" % urllib.urlencode(getparams)
        post = urllib.urlencode(postparams)
        #post = "&".join(["%s=%s" % (pair[0], pair[1]) for pair in params.items()])
        try:
            if '' == post:
                return json.load(urllib2.urlopen(url))
            else:
                return json.load(urllib2.urlopen(url, data=post))
        except Exception as e:
            return "Error: %s" % str(e)
    
    def get(self, url, params):
        return self.call(url, params, {})
    
    def post(self, url, params):
        return self.call(url, {}, params)

class DataRoom(API):
    def __init__(self, user, dataroom, api = None):
        
        if not isinstance(user, User):
            self.user = User(user, api)
        else:
            self.user = user
        
        self.dataroom = dataroom
        self.api = api
    
    def details(self):
        params = {}
        if self.api:
            params['api_key'] = self.api
        url = "https://buzzdata.com/api/%s/%s" % (str(self.user), self.dataroom)
        return self.get(url, params)
    
    def list_datafiles(self):
        params = {}
        if self.api:
            params['api_key'] = self.api
        url = "https://buzzdata.com/api/%s/%s/list_datafiles" % (str(self.user), self.dataroom)
        return self.get(url, params)        
    
    def __str__(self):
        return self.dataroom
    
    def __repr__(self):
        return self.__str__()
    
class User(API):
    def __init__(self, user, api = None):
        self.user = user
        self.api = api
    
    def list_datarooms(self):
        params = {}
        if self.api:
            params['api_key'] = self.api
        url = "https://buzzdata.com/api/%s/datasets/list" % self.user
        return self.get(url, params)     
    
    def __str__(self):
        return self.user
    
    def __repr__(self):
        return self.__str__()
