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
from apps.ml.project_recommender.interacted_projects_based import InteractedProjectsBased

try:
    registry = MLRegistry()  # create ML registry
    # Random Forest classifier
    upb = UserProjectFieldsBased()
    # add to ML registry
    registry.add_algorithm(endpoint_name=upb.endpoint_name,
                           algorithm_object=upb,
                           algorithm_name=upb.algorithm_name,
                           algorithm_status=upb.status,
                           algorithm_version=upb.version,
                           owner=upb.owner,
                           algorithm_description=upb.description,
                           algorithm_code=inspect.getsource(UserProjectFieldsBased))

    ipb = InteractedProjectsBased()
    registry.add_algorithm(endpoint_name=ipb.endpoint_name,
                           algorithm_object=upb,
                           algorithm_name=ipb.algorithm_name,
                           algorithm_status=ipb.status,
                           algorithm_version=ipb.version,
                           owner=ipb.owner,
                           algorithm_description=ipb.description,
                           algorithm_code=inspect.getsource(UserProjectFieldsBased))

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))
