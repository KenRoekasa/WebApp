from django.test import TestCase
from app.views import home,project_list,cv,blog_list
from django.urls import resolve


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

class CVPageTest(TestCase):

    def test_root_url_resolves_to_cv_view(self):
        found = resolve('/cv/')
        self.assertEqual(found.func, cv)



class PortfolioPageTest(TestCase):
    def test_root_url_resolves_to_project_view(self):
        found = resolve('/portfolio/')
        self.assertEqual(found.func, project_list)


class BlogPageTest(TestCase):

    def test_root_url_resolves_to_blog_page_view(self):
        found = resolve('/blog/')
        self.assertEqual(found.func, blog_list)
