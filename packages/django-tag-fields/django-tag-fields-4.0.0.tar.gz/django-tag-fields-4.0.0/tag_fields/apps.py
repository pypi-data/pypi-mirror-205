from django.apps import AppConfig as BaseConfig
from django.utils.translation import gettext_lazy as _


class TaggitAppConfig(BaseConfig):
    name = "tag_fields"
    verbose_name = _("Tag Fields")
    default_auto_field = "django.db.models.AutoField"
