import http

import django.test
import django.urls

__all__ = ()


class StaticURLTests(django.test.TestCase):
    def test_homepage_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse(
                "homepage:homepage",
            ),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
