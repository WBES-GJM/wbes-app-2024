from django.contrib import admin
from django.apps import apps
# from allauth.account.models import EmailAddress

# Register your models here.
class ListAdminMixin(object):
    readonly_fields = ('id',)
    def __init__(self, model, admin_site):
        self.list_display = ("id",) + self.list_display
        super(ListAdminMixin, self).__init__(model, admin_site)

# admin.site.register(EmailAddress)

# Register all models for admin panel
app_config = apps.get_app_config('apps')
app_models = app_config.get_models()

for model in app_models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass