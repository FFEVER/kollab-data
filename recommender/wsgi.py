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
from apps.ml.project_recommender.user_project_fields_based import ProjectToUserFieldsBased
from apps.ml.project_recommender.interacted_projects_based import InteractedProjectsBased
from apps.ml.project_recommender.fields_or_interacted_based import FieldsOrInteractedBased
from apps.ml.related_project.project_fields_based import ProjectFieldsBased
from apps.ml.user_recommender.user_to_project_fields_based import UserToProjectFieldsBased

try:
    registry = RecRegistry()  # create ML registry

    # add to ML registry
    ptufb = ProjectToUserFieldsBased()
    registry.add_algorithm(endpoint_name=ptufb.endpoint_name,
                           algorithm_object=ptufb,
                           algorithm_name=ptufb.algorithm_name,
                           algorithm_status=ptufb.status,
                           algorithm_version=ptufb.version,
                           owner=ptufb.owner,
                           algorithm_description=ptufb.description,
                           algorithm_code=inspect.getsource(ProjectToUserFieldsBased))

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

    pfb = ProjectFieldsBased()
    registry.add_algorithm(endpoint_name=pfb.endpoint_name,
                           algorithm_object=pfb,
                           algorithm_name=pfb.algorithm_name,
                           algorithm_status=pfb.status,
                           algorithm_version=pfb.version,
                           owner=pfb.owner,
                           algorithm_description=pfb.description,
                           algorithm_code=inspect.getsource(ProjectFieldsBased))

    utpfb = UserToProjectFieldsBased()
    registry.add_algorithm(endpoint_name=utpfb.endpoint_name,
                           algorithm_object=utpfb,
                           algorithm_name=utpfb.algorithm_name,
                           algorithm_status=utpfb.status,
                           algorithm_version=utpfb.version,
                           owner=utpfb.owner,
                           algorithm_description=utpfb.description,
                           algorithm_code=inspect.getsource(UserToProjectFieldsBased))

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))
