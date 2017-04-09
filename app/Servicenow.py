import requests
import json
import logging
import sys

FORMAT = '%(asctime)-15s :: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('Servicenow')
logger.setLevel('INFO')

class Servicenow(object):
    def __init__(self):
        self.url = 'https://securityondemand.service-now.com/api/now/table/incident'
        self.session = requests.Session()
        self.session.headers = {"Content-Type":"application/json", "Accept":"application/json"}

    def authenticate(self, user, passwd):
        self.session.auth = (user, passwd)
        response = self.get('/fa7d5bf6dbf97240b3bbd211ce9619c5')
        if response.status_code != 200:
            return "Authentication Failed"
        return True

    def fetch(self, func, uri, data=None):
        success_codes = {'get': 200, 'post': 201, 'put': 200, 'patch': 200, 'delete': 204}
        if not self.session.auth:
            return "User Not Authenticated"
        try:
            response = func(uri, data=data)
        except:
            logger.error("Unexpected Error: {}".format(sys.exec_info()[0]))
        if response.status_code != success_codes[func.__name__]:
            msg =('Status:', response.status_code,
                  'Headers:', response.headers,
                  'Error Response:', response.json())
            logger.info(msg)
        return response

    def get(self, uri):
        return self.fetch(self.session.get, self.url + uri)

    def delete(self, uri):
        return self.fetch(self.session.delete, self.url + uri)

    def post(self, uri, data):
        return self.fetch(self.session.post, self.url + uri, data=json.dumps(data))

    def put (self, uri, data):
        return self.fetch(self.session.put, self.url + uri, data=json.dumps(data))

    def patch(self, uri, data):
        return self.fetch(self.session.patch, self.url + uri, data=json.dumps(data))
