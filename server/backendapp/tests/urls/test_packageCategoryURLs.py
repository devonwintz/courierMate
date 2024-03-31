from django.test import TestCase
from django.urls import reverse, resolve
from backendapp import views

class PackageCategoryURLTest(TestCase):
    def test_package_category_list_url(self):
        url = reverse('package-category-list')
        self.assertEqual(url, '/package-categories/')

    def test_package_category_list_url_resolve_to_correct_view(self):
        url = reverse('package-category-list')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.view_class, views.PackageCategoryList)

    def test_package_category_detail_url(self):
        package_category_id = 1
        url = reverse('package-category-detail', args=[package_category_id])
        self.assertEqual(url, f"/package-categories/{package_category_id}/")

    def test_package_category_detail_resolves_to_correct_view(self):
        package_category_id = 1
        url = reverse('package-category-detail', args=[package_category_id])
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.view_class, views.PackageCategoryDetail)
