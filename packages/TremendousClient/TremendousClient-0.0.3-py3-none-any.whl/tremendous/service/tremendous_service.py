import os
from tremendous.exception import TremendousException, ErrorCodes


class TremendousService:
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
