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
from apps.ml.registry import RecRegistry
from apps.ml.project_recommender.user_project_fields_based import UserProjectFieldsBased
from apps.ml.project_recommender.interacted_projects_based import InteractedProjectsBased
from apps.ml.project_recommender.fields_or_interacted_based import FieldsOrInteractedBased

try:
    registry = RecRegistry()  # create ML registry

    # add to ML registry
    upb = UserProjectFieldsBased()
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
                           algorithm_object=ipb,
                           algorithm_name=ipb.algorithm_name,
                           algorithm_status=ipb.status,
                           algorithm_version=ipb.version,
                           owner=ipb.owner,
                           algorithm_description=ipb.description,
                           algorithm_code=inspect.getsource(InteractedProjectsBased))

    foib = FieldsOrInteractedBased()
    registry.add_algorithm(endpoint_name=foib.endpoint_name,
                           algorithm_object=foib,
                           algorithm_name=foib.algorithm_name,
                           algorithm_status=foib.status,
                           algorithm_version=foib.version,
                           owner=foib.owner,
                           algorithm_description=foib.description,
                           algorithm_code=inspect.getsource(FieldsOrInteractedBased))

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))
