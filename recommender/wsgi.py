"""
WSGI config for recommender project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recommender.settings')

application = get_wsgi_application()

# ML registry
import inspect
from apps.ml.registry import MLRegistry
from apps.ml.project_recommender.user_project_fields_based import UserProjectFieldsBased

try:
    registry = MLRegistry()  # create ML registry
    # Random Forest classifier
    upb = UserProjectFieldsBased()
    # add to ML registry
    registry.add_algorithm(endpoint_name=UserProjectFieldsBased.endpoint_name,
                           algorithm_object=upb,
                           algorithm_name=UserProjectFieldsBased.algorithm_name,
                           algorithm_status=UserProjectFieldsBased.status,
                           algorithm_version=UserProjectFieldsBased.version,
                           owner=UserProjectFieldsBased.owner,
                           algorithm_description=UserProjectFieldsBased.description,
                           algorithm_code=inspect.getsource(UserProjectFieldsBased))

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))
