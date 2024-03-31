from django.test import TestCase
from django.urls import reverse, resolve
from backendapp import views

class PackageStatusURLTest(TestCase):
    def test_package_status_list_url(self):
        url = reverse('package-status-list')
        self.assertEqual(url, '/package-statuses/')

    def test_package_status_list_url_resolve_to_correct_view(self):
        url = reverse('package-status-list')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.view_class, views.PackageStatusList)

    def test_package_status_detail_url(self):
        package_status_id = 1
        url = reverse('package-status-detail', args=[package_status_id])
        self.assertEqual(url, f"/package-statuses/{package_status_id}/")

    def test_package_status_detail_resolves_to_correct_view(self):
        package_status_id = 1
        url = reverse('package-status-detail', args=[package_status_id])
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.view_class, views.PackageStatusDetail)
