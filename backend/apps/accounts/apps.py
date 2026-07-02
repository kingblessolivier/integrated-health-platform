from copy import copy

from django.apps import AppConfig
from django.contrib.admin.templatetags import admin_list
from django.template import Node
from django.template.context import BaseContext, Context


class EmptyNode(Node):
    def render(self, context):
        return ""


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"

    def ready(self):
        def copy_base_context(self):
            duplicate = object.__new__(self.__class__)
            duplicate.dicts = self.dicts[:]
            return duplicate

        def copy_context(self):
            duplicate = object.__new__(self.__class__)
            duplicate.dicts = self.dicts[:]
            duplicate.autoescape = self.autoescape
            duplicate.use_l10n = self.use_l10n
            duplicate.use_tz = self.use_tz
            duplicate.template_name = self.template_name
            duplicate.render_context = copy(self.render_context)
            duplicate.template = self.template
            return duplicate

        BaseContext.__copy__ = copy_base_context
        Context.__copy__ = copy_context

        def change_list_object_tools_tag(parser, token):
            return EmptyNode()

        admin_list.register.tags["change_list_object_tools"] = change_list_object_tools_tag