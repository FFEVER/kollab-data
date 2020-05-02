import os
import requests
import logging

KOLLAB_HEADERS = {'Authorization': f'Bearer {os.getenv("KOLLAB_API_KEY")}',
                  'Accept': 'application/json'}
logger = logging.getLogger(__name__)


def kollab_domain():
    if os.getenv('KOLLAB_DATA_ENV') == 'production':
        return 'https://kollab-project.herokuapp.com'
    else:
        return 'http://localhost:5000'


def get_users():
    domain = kollab_domain()
    path = '/api/v1/users'
    url = domain + path
    response = requests.get(url, headers=KOLLAB_HEADERS)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        logger.error(f'Error retrieving users from {url}.')
        response.raise_for_status()
