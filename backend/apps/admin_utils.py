from django.contrib import admin
from django.apps import apps as django_apps
from django.contrib.admin.sites import AlreadyRegistered


def register_app_models(app_label: str) -> None:
    app_config = django_apps.get_app_config(app_label)
    for model in app_config.get_models():
        try:
            admin.site.register(model)
        except AlreadyRegistered:
            continue
