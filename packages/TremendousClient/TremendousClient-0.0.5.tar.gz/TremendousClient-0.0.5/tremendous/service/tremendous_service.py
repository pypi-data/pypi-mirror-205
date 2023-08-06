import os
from tremendous.exception import TremendousException, ErrorCodes
from tremendous.service.http_service import HttpService


class TremendousService(HttpService):
    params = dict()
    API_DEV_URL = 'https://testflight.tremendous.com/'
    API_PROD_URL = 'https://api.tremendous.com/'

    def __init__(self, environment="dev", token=None):
        self.environment = os.environ.get('TREMENDOUS_ENV', environment)
        if self.environment is None:
            raise ValueError(ErrorCodes.ENVIRONMENT_ERROR)
        self.token = os.environ.get('TREMENDOUS_TOKEN', token)
        if self.token is None:
            raise ValueError(ErrorCodes.ACCESS_TOKEN_ERROR)
        api_url = self.API_DEV_URL if self.environment == 'dev' else self.API_PROD_URL
        super().__init__(api_url)
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'content-type': 'application/json',
            'accept': 'application/json'
        }

    def getRequest(self, key):
        endpoint = f'/api/v2/{key}'
        response = self.connect('GET', endpoint, headers=self.headers)
        if key not in response:
            raise AttributeError(ErrorCodes.INVALID_ATTRIBUTE)
        return response[key]

    def getFundingSource(self):
        return self.getRequest('funding_sources')

    def getProducts(self):
        return self.getRequest('products')

    def createOrder(self, body):
        key = 'order'
        endpoint = '/api/v2/orders'
        response = self.connect('POST', endpoint, body, headers=self.headers)
        if key not in response:
            raise AttributeError(ErrorCodes.INVALID_ATTRIBUTE)
        return response[key]
