import os
import requests
import logging

logger = logging.getLogger(__name__)


class KollabApi:

    def __init__(self):
        if os.getenv('KOLLAB_DATA_ENV') == 'production':
            self.kollab_domain = 'https://kollab-project.herokuapp.com'
        else:
            self.kollab_domain = 'http://localhost:5000'
        self.kollab_headers = {'Authorization': f'Bearer {os.getenv("KOLLAB_API_KEY")}',
                               'Accept': 'application/json'}

    def __get(self, path, headers=None):
        if headers is None:
            headers = self.kollab_headers
        url = self.kollab_domain + path

        response = requests.get(url, headers=headers)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            logger.error(f'Error in GET from {url}.')
            response.raise_for_status()

    def get_users(self):
        return self.__get('/api/v1/users')

    def get_expertises(self):
        return self.__get('/api/v1/expertises')
