from django.contrib import admin
from django.apps import apps

# Register your models here.
class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        super(ListAdminMixin, self).__init__(model, admin_site)

# Register all models for admin panel
app_config = apps.get_app_config('apps')
app_models = app_config.get_models()

for model in app_models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass