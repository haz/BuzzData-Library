
import urllib, urllib2, json, time

class API:
    """
    Class to wrap the RESTful web service calls.
    """
    def call(self, url, getparams, postparams):
        """
        Make a GET or POST call, depending on the supplied
        parameters, and return the json parsed result. If
        an error is thrown, that is returned instead.
        """
        if getparams:
            url += "/?%s" % urllib.urlencode(getparams)
        post = json.dumps(postparams)
        
        try:
            if postparams:
                req = urllib2.Request(url)
                req.add_header('Content-Type', 'application/json')
                return json.load(urllib2.urlopen(req, post))
            else:
                return json.load(urllib2.urlopen(url))
        except Exception as e:
            return "Error: %s" % str(e)
    
    def get(self, url, params):
        """
        Make a GET call with the given parameters.
        """
        return self.call(url, params, {})
    
    def post(self, url, params):
        """
        Make a POST call with the given parameters using
        json to encode the options.
        """
        return self.call(url, {}, params)
    
    def www_post(self, url, params):
        """
        Make a POST call with the given parameters, but use
        urlencode for the parameters instead of json encoding.
        """
        data = urllib.urlencode(params)
        try:
            return json.load(urllib2.urlopen(url, data))
        except Exception as e:
            return "Error: %s" % str(e)
    
    def delete(self, url, params):
        """
        Make a DELETE call with the given parameters using
        json to encode the options.
        """
        data = json.dumps(params)
        req = RequestWithMethod(url, method='DELETE', data=data)
        req.add_header('Content-Type', 'application/json')
        return json.load(urllib2.urlopen(req))
    
    def put(self, url, params, www=False):
        """
        Make a DELETE call with the given parameters. If www
        is set to True, then urlencode is used for the options.
        Otherwise, json is used.
        """
        if www:
            data = urllib.urlencode(params)
        else:
            data = json.dumps(params)
        req = RequestWithMethod(url, method='PUT', data=data)
        if not www:
            req.add_header('Content-Type', 'application/json')
        return json.load(urllib2.urlopen(req))

class DataRoom(API):
    """
    Class that represents a data room.
    """
    def __init__(self, user, dataroom, api = None, hive = ''):
        if not isinstance(user, User):
            self.user = User(user, api)
        else:
            self.user = user
        
        self.dataroom = dataroom
        self.api = api
        self.hive = hive
        
        if hive:
            self.hive += '.'
    
    @staticmethod
    def create(user, api, name, public, readme, license, topics, hive = ''):
        """
        Create a new data room on BuzzData and return the
        corresponding DataRoom object.
        
        Keyword arguments:
        user    -- User object or username
        api     -- string of the BuzzData API key
        name    -- string of the name of the new data room
        public  -- boolean flag for the data room's privacy
        readme  -- string of the readme text for the data room
        license -- string of the license for the data room
        topics  -- array of topics for the data room
        hive    -- name of the hive for the data room
        """
        room_details = {'name':name,
                        'public':public,
                        'readme':readme,
                        'license':license,
                        'topics':topics}
        params = {'api_key': api, 'dataset':room_details}
        if hive:
            hive += '.'
        url = "https://%sbuzzdata.com/api/%s/datasets" % (hive, str(user))
        room = DataRoom(user, name, api)
        response = room.post(url, params)
        return (response, room)
    
    def destroy(self):
        """
        Delete the data room corresponding to this object.
        """
        if not self.api:
            return "Error: Must specify an api."
        params = {'api_key': self.api}
        url = "https://%sbuzzdata.com/api/%s/%s" % (self.hive, str(self.user), self.dataroom)
        return self.delete(url, params)
    
    def details(self):
        """
        Fetch the details for the data room.
        """
        params = {}
        if self.api:
            params['api_key'] = self.api
        url = "https://%sbuzzdata.com/api/%s/%s" % (self.hive, str(self.user), self.dataroom)
        return self.get(url, params)
    
    def list_datafiles(self):
        """
        List the data files for this data room.
        """
        params = {}
        if self.api:
            params['api_key'] = self.api
        url = "https://%sbuzzdata.com/api/%s/%s/list_datafiles" % (self.hive, str(self.user), self.dataroom)
        return self.get(url, params)
    
    def create_datafile(self, name):
        """
        Create a new data file for this data room.
        """
        if not self.api:
            return "Error: Must specify an api."
        params = {'data_file_name': name, 'api_key': self.api}
        url = "https://%sbuzzdata.com/api/%s/%s/create_datafile" % (self.hive, str(self.user), self.dataroom)
        
        response = self.post(url, params)
        if 'datafile_uuid' not in response:
            return ("Error: Bad response -- %s" % str(response), None)
        
        datafile = DataFile(self, response['datafile_uuid'])
        return (response, datafile)
    
    def __str__(self):
        return self.dataroom
    
    def __repr__(self):
        return self.__str__()

class DataFile(API):
    """
    Class that represents a data file.
    """
    def __init__(self, dataroom, uuid):
        self.dataroom = dataroom
        self.api = dataroom.api
        self.hive = dataroom.hive
        self.uuid = uuid
        self.stage = None
    
    def history(self):
        """
        Fetch the history of this data file.
        """
        params = {}
        if self.api:
            params['api_key'] = self.api
        url = "https://%sbuzzdata.com/api/data_files/%s/history" % (self.hive, self.uuid)
        return self.get(url, params)
    
    def download(self, version=None, filename=None):
        """
        Download a version of this data file.
        
        If filename is not provided, the file is named according
        to <dataroom>.<uuid>.<version>, where <version> is 'head'
        when no version is provided.
        
        Keyword arguments:
        version  -- integer version of the data file
        filename -- string of the filename to save to
        """
        params = {}
        if version:
            params['version'] = version
        if self.api:
            params['api_key'] = self.api
        url = "https://%sbuzzdata.com/api/%s/%s/%s/download_request" % (self.hive, self.dataroom.user, self.dataroom, self.uuid)
        location = self.post(url, params)['download_request']['url']
        u = urllib2.urlopen(location)
        if not filename:
            if not version:
                version = 'head'
            filename = "%s.%s.%s" % (self.dataroom, self.uuid, str(version))
        f = open(filename, 'w')
        f.write(u.read())
        f.close()
    
    def upload(self, filename, release_notes):
        """
        Upload a new version of a data file.
        
        Keyword arguments:
        filename      -- string of the filename to upload
        release_notes -- string of the new file's release notes
        """
        # First we get an upload request
        if not self.api:
            return "Error: Must specify an api."
        params = {'api_key':self.api, 'datafile_uuid':self.uuid}
        url = "https://%sbuzzdata.com/api/%s/%s/upload_request" % (self.hive, self.dataroom.user, self.dataroom)
        response = self.post(url, params)
        upload_code = response['upload_request']['upload_code']
        upload_url = response['upload_request']['url']
        
        # Next, get the data we want to upload
        f = open(filename, 'r')
        data = f.read()
        f.close()
        
        # Next, we attempt to post the file
        return json.loads(posturl(upload_url,
                       [('api_key', self.api),
                        ('upload_code', upload_code),
                        ('release_notes', release_notes)],
                       [('file', filename, data)])[1:-1])
    
    def create_stage(self):
        """Create a new Stage object for this data file."""
        if self.stage:
            return "Error: Data file already has a stage."
        self.stage = Stage(self)
    
    def save(self):
        """Save the changes made to the current stage so far."""
        if not self.stage:
            return "Error: Data file does not currently have a stage."
        resp = self.stage.commit()
        self.stage = None
        return resp
    
    def rollback(self):
        """Roll back any changes made to the data file so far."""
        if not self.stage:
            return "Error: Data file does not currently have a stage."
        resp = self.stage.rollback()
        self.stage = None
        return resp
    
    def insert_rows(self, rows):
        """Insert new rows to the end of this data file."""
        commit = False
        if not self.stage:
            self.create_stage()
            commit = True
        resp = "Stage id: %s" % self.stage.stage_id
        resp += "\n" + str(self.stage.insert_rows(rows))
        if commit:
            resp += "\n" + str(self.stage.commit())
        return resp
    
    def update_row(self, row, row_num):
        """Update a particular row given a row array and number."""
        commit = False
        if not self.stage:
            self.create_stage()
            commit = True
        resp = "Stage id: %s" % self.stage.stage_id
        resp += "\n" + str(self.stage.update_row(row, row_num))
        if commit:
            resp += "\n" + str(self.stage.commit())
        return resp
    
    def delete_row(self, row_num):
        """Delete a specific row from the data file."""
        commit = False
        if not self.stage:
            self.create_stage()
            commit = True
        resp = "Stage id: %s" % self.stage.stage_id
        resp += "\n" + str(self.stage.delete_row(row_num))
        if commit:
            resp += "\n" + str(self.stage.commit())
        return resp
    
    def __str__(self):
        return self.uuid
    
    def __repr__(self):
        return self.__str__()


class User(API):
    """
    Class that represents a BuzzData user.
    """
    def __init__(self, user, api = None, hive = ''):
        self.user = user
        self.api = api
        self.hive = hive
        
        if hive:
            self.hive += '.'
    
    def details(self):
        """
        Fetch the details for this user.
        """
        params = {}
        if self.api:
            params['api_key'] = self.api
        url = "https://%sbuzzdata.com/api/%s" % (self.hive, self.user)
        return self.get(url, params)
    
    def list_datarooms(self):
        """
        List the data rooms for this user.
        """
        params = {}
        if self.api:
            params['api_key'] = self.api
        url = "https://%sbuzzdata.com/api/%s/datasets/list" % (self.hive, self.user)
        return self.get(url, params)
    
    def __str__(self):
        return self.user
    
    def __repr__(self):
        return self.__str__()


class Stage(API):
    """
    Class that represents a Stage for updating BuzzData.
    """
    def __init__(self, datafile):
        self.datafile = datafile
        self.api = datafile.api
        self.hive = datafile.hive
        self.load_stage()
    
    def load_stage(self):
        """Start (load) a new stage for updating."""
        if not self.api:
            return "Error: Must specify an api."
        params = {'api_key': self.api}
        url = "https://%sbuzzdata.com/api/%s/%s/%s/stage" % (self.hive, self.datafile.dataroom.user, self.datafile.dataroom, self.datafile)
        response = self.post(url, params)
        self.stage_id = response['id']
    
    def insert_rows(self, rows):
        """Insert new rows to the end of this data file."""
        if not self.api:
            return "Error: Must specify an api."
        params = {'datafile_uuid':str(self.datafile),
                  'stage_id':self.stage_id,
                  'api_key':self.api,
                  'rows':json.dumps(rows)}
        url = "https://%sbuzzdata.com/api/%s/%s/%s/stage/%s/rows" % (self.hive,
                                                                     self.datafile.dataroom.user,
                                                                     self.datafile.dataroom,
                                                                     self.datafile,
                                                                     self.stage_id)
        return self.www_post(url, params)
    
    def update_row(self, row, row_num):
        """Update a particular row given a row array and number."""
        if not self.api:
            return "Error: Must specify an api."
        params = {'api_key':self.api,
                  'row':json.dumps(row)}
        url = "https://%sbuzzdata.com/api/%s/%s/%s/stage/%s/rows/%d" % (self.hive,
                                                                        self.datafile.dataroom.user,
                                                                        self.datafile.dataroom,
                                                                        self.datafile,
                                                                        self.stage_id,
                                                                        row_num)
        return self.put(url, params, True)
    
    def delete_row(self, row_num):
        """Delete a specific row from the data file."""
        if not self.api:
            return "Error: Must specify an api."
        params = {'api_key':self.api}
        url = "https://%sbuzzdata.com/api/%s/%s/%s/stage/%s/rows/%d" % (self.hive,
                                                                        self.datafile.dataroom.user,
                                                                        self.datafile.dataroom,
                                                                        self.datafile,
                                                                        self.stage_id,
                                                                        row_num)
        return self.delete(url, params)
    
    def commit(self):
        """Commit the stage and all changes made."""
        if not self.api:
            return "Error: Must specify an api."
        params = {'datafile_uuid':str(self.datafile),
                  'stage_id':self.stage_id,
                  'api_key':self.api}
        url = "https://%sbuzzdata.com/api/%s/%s/%s/stage/%s/commit" % (self.hive,
                                                                       self.datafile.dataroom.user,
                                                                       self.datafile.dataroom,
                                                                       self.datafile,
                                                                       self.stage_id)
        # Record the response and sleep to avoid server issues
        resp = self.post(url, params)
        time.sleep(1)
        return resp
    
    def rollback(self):
        """Rollback the changes made to this stage."""
        if not self.api:
            return "Error: Must specify an api."
        params = {'datafile_uuid':str(self.datafile),
                  'api_key':self.api}
        url = "https://%sbuzzdata.com/api/%s/%s/%s/stage/%s/rollback" % (self.hive,
                                                                         self.datafile.dataroom.user,
                                                                         self.datafile.dataroom,
                                                                         self.datafile,
                                                                         self.stage_id)
        return self.post(url, params)
    
    def __str__(self):
        return self.stage_id
    
    def __repr__(self):
        return self.__str__()

def buzz_search(query, api = None, hive = ''):
    """Search BuzzData for a particular query."""
    params = {'query':query}
    if api:
        params['api_key'] = api
    if hive:
        hive += '.'
    return API().get("https://%sbuzzdata.com/api/search" % hive, params)

def buzz_licenses(api = None, hive = ''):
    """Fetch the list of BuzzData licenses."""
    params = {}
    if api:
        params['api_key'] = api
    if hive:
        hive += '.'
    return API().get("https://%sbuzzdata.com/api/licenses" % hive, params)

def buzz_topics(api = None, hive = ''):
    """Fetch the list of BuzzData topics."""
    params = {}
    if api:
        params['api_key'] = api
    if hive:
        hive += '.'
    return API().get("https://%sbuzzdata.com/api/topics" % hive, params)









##################################################
##                                                              
##  In order to POST multipart data, the code below was extracted from:
##  * http://code.activestate.com/recipes/146306-http-client-to-post-using-multipartform-data/
##
##  It has been modified with some of the comments to update the library,
##   as well as HTTPSConnection is used since the only POST requests the
##   library makes are over https.
##


import httplib, mimetypes, urlparse

def posturl(url, fields, files):
    urlparts = urlparse.urlsplit(url)
    return post_multipart(urlparts[1], urlparts[2], fields,files)


def post_multipart(host, selector, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTPSConnection(host)
    headers = {
        'User-Agent': 'INSERT USERAGENTNAME',
        'Content-Type': content_type
        }
    h.request('POST', selector, body, headers)
    res = h.getresponse()
    return res.read()


def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


##################################################
##                                                              
##  In order to send PUT and DELETE requests, the code below was extracted from:
##  * http://stackoverflow.com/questions/4511598/how-to-make-http-delete-method-using-urllib2
##

class RequestWithMethod(urllib2.Request):
    def __init__(self, *args, **kwargs):
        self._method = kwargs.get('method')
        if self._method:
            del kwargs['method']
        urllib2.Request.__init__(self, *args, **kwargs)
  
    def get_method(self):
        return self._method if self._method else super(RequestWithMethod, self).get_method()
