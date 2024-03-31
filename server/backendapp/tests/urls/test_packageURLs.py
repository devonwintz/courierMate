from django.test import TestCase
from django.urls import reverse, resolve
from backendapp import views

class PackageURLTest(TestCase):
    def test_package_list_url(self):
        url = reverse('package-list')
        self.assertEqual(url, '/packages/')

    def test_package_list_url_resolve_to_correct_view(self):
        url = reverse('package-list')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.view_class, views.PackageList)

    def test_package_detail_url(self):
        package_id = 1
        url = reverse('package-detail', args=[package_id])
        self.assertEqual(url, f"/packages/{package_id}/")

    def test_package_detail_resolves_to_correct_view(self):
        package_id = 1
        url = reverse('package-detail', args=[package_id])
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.view_class, views.PackageDetail)
