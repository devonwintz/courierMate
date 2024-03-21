from django.test import TestCase
from django.contrib import admin
from django.apps import apps

class AdminRegistrationTest(TestCase):
    def test_admin_registration(self):
        models = apps.get_app_config('backendapp').get_models()
        admin_site = admin.site

        for model in models:
            try:
                admin_site.register(model)
            except admin.sites.AlreadyRegistered:
                pass

