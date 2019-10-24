import requests
import urllib.request, urllib.parse, urllib.error

class Book_Request:
#makes requests to google book API and returns the response object

    url = "https://www.googleapis.com/books/v1/volumes"

    def __init__(self):
        self.data = []
        self.params = {'q':'',
                       'maxResults':40,
                       'startIndex':0}

    def get_books(self, search=None, maxResults=None, startIndex=None):
        if len(search) == 0:
            return None
        self.params['q']=search

        if maxResults != None:
            self.params['maxResults'] = maxResults

        if startIndex != None:
            self.params['startIndex'] = startIndex


        url = self.url + '?' + urllib.parse.urlencode(self.params)
        r = requests.get(url, verify=False)
        return r

