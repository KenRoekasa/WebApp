from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import resolve

from .views import home, cv, project_list, blog_list
from .models import Blog, Project, Education


class CSRFTest(TestCase):
    def test_CSRF(self):
        csrf_client = self.client(enforce_csrf_checks=True);
        self.assertTrue(self, csrf_client)


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'app/home.html')


class BlogPageTest(TestCase):

    def test_root_url_resolves_to_blog_page_view(self):
        found = resolve('/blog/')
        self.assertEqual(found.func, blog_list)

    def test_blog_page_returns_correct_html(self):
        response = self.client.get('/blog/')
        self.assertTemplateUsed(response, 'app/blog.html')

    def test_blog_edit_page_returns_correct_html(self):
        response = self.client.get('/blog/new/')
        self.assertTemplateUsed(response, 'app/blog_new.html')

    def test_blog_edit_page_save_POST_request(self):
        response = self.client.post('/blog/new/',
                                    data={'title': 'Testing', 'text': 'This is testing if the post is working'})
        # self.assertIn('Testing', response.content.decode())
        # self.assertIn('This is testing if the post is working', response.content.decode())
        # Get last post
        latest_item = Blog.objects.order_by('id')[0]
        self.assertEqual(latest_item.title, "Testing")
        self.assertEqual(latest_item.text, "This is testing if the post is working")

    def test_redirects_after_POST(self):
        response = self.client.post('/blog/new/',
                                    data={'title': 'Testing', 'text': 'This is testing if the post is working'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'post_detail')

    def test_displays_all_blogs_ordered(self):
        Blog.objects.create(title='hello test', text='this is the text')
        Blog.objects.create(title='Testing the goat', text='Oh blah blah blah testing')

        response = self.client.get('/blog/')

        self.assertIn('hello test', response.content.decode())
        self.assertIn('Testing the goat', response.content.decode())
        self.assertIn('this is the text', response.content.decode())
        self.assertIn('Oh blah blah blah testing', response.content.decode())

    def test_saving_and_retrieving_blog(self):
        first_blog = Blog()
        first_blog.title = 'Blog post test 1'
        first_blog.text = 'Hello this is a blog post'
        first_blog.save()

        second_blog = Blog()
        second_blog.title = 'Blog post test 2'
        second_blog.text = 'Hello this is also blog post even longer'
        second_blog.save()

        saved_blogs = Blog.objects.all()
        self.assertEqual(saved_blogs.count(), 2)

        first_saved_blog = saved_blogs[0]
        second_save_blog = saved_blogs[1]
        self.assertEqual(first_saved_blog.Title, 'Blog post test 1')
        self.assertEqual(second_save_blog.Title, 'Blog post test 2')
        self.assertEqual(first_saved_blog.text, 'Hello this is a blog post')
        self.assertEqual(second_save_blog.text, 'Hello this is also blog post even longer')


class CVPageTest(TestCase):
    def test_root_url_resolves_to_cv_view(self):
        found = resolve('/cv/')
        self.assertEqual(found.func, cv)

    def test_cv_page_returns_correct_html(self):
        response = self.client.get('/cv/')
        self.assertTemplateUsed(response, 'app/cv.html')

    def test_education_new_url_resolves_to_cv_new_view(self):
        found = resolve('/cv/edit/education/new')
        self.assertEqual(found.func, cv_education_edit)

    def test_cv_education_new_edit_page_returns_correct_html(self):
        response = self.client.get('/cv/edit/education/new')
        self.assertTemplateUsed(response, 'app/cv_edit.html')

    def test_cv_edit_page_returns_correct_html(self):
        response = self.client.get('/cv/edit/')
        self.assertTemplateUsed(response, 'app/cv_edit.html')

    def test_cv_page_has_education_section(self):
        response = self.client.get('/cv/')
        html = response.content.decode('utf8')
        self.assertIn('<h1>Education</h1>', html)

    def test_cv_page_has_no_new_button_click_when_logged_out(self):
        response = self.client.get('/cv/')
        html = response.content.decode('utf8')
        self.assertNotIn('id = education_add_button', html)

    def test_cv_page_has_new_button_click_when_logged_in(self):
        c = Client()
        c.login(username='kenny', password='adminadmin123')
        response = self.client.get('/cv/')
        html = response.content.decode('utf8')
        self.assertIn('id = education_add_button', html)

    # def test_cv_edit_education_save_POST_request(self):
    #     response = self.client.post('/blog/new/',
    #                                 data={'title': 'Testing', 'text': 'This is testing if the post is working'})
    #     # self.assertIn('Testing', response.content.decode())
    #     # self.assertIn('This is testing if the post is working', response.content.decode())
    #     # Get last post
    #     latest_item = Blog.objects.order_by('id')[0]
    #     self.assertEqual(latest_item.title, "Testing")
    #     self.assertEqual(latest_item.text, "This is testing if the post is working")

    # def test_cv_edit_tech_skills_save_POST_request(self):
    #     response = self.client.post('/blog/new/',
    #                                 data={'title': 'Testing', 'text': 'This is testing if the post is working'})
    #     # self.assertIn('Testing', response.content.decode())
    #     # self.assertIn('This is testing if the post is working', response.content.decode())
    #     # Get last post
    #     latest_item = Blog.objects.order_by('id')[0]
    #     self.assertEqual(latest_item.title, "Testing")
    #     self.assertEqual(latest_item.text, "This is testing if the post is working")
    #
    # def test_cv_edit_academic_projects_save_POST_request(self):
    #     response = self.client.post('/blog/new/',
    #                                 data={'title': 'Testing', 'text': 'This is testing if the post is working'})
    #     # self.assertIn('Testing', response.content.decode())
    #     # self.assertIn('This is testing if the post is working', response.content.decode())
    #     # Get last post
    #     latest_item = Blog.objects.order_by('id')[0]
    #     self.assertEqual(latest_item.title, "Testing")
    #     self.assertEqual(latest_item.text, "This is testing if the post is working")
    #
    # def test_cv_edit_work_experience_save_POST_request(self):
    #     response = self.client.post('/blog/new/',
    #                                 data={'title': 'Testing', 'text': 'This is testing if the post is working'})
    #     # self.assertIn('Testing', response.content.decode())
    #     # self.assertIn('This is testing if the post is working', response.content.decode())
    #     # Get last post
    #     latest_item = Blog.objects.order_by('id')[0]
    #     self.assertEqual(latest_item.title, "Testing")
    #     self.assertEqual(latest_item.text, "This is testing if the post is working")
    #
    # def test_cv_edit_awards_save_POST_request(self):
    #     response = self.client.post('/blog/new/',
    #                                 data={'title': 'Testing', 'text': 'This is testing if the post is working'})
    #     # self.assertIn('Testing', response.content.decode())
    #     # self.assertIn('This is testing if the post is working', response.content.decode())
    #     # Get last post
    #     latest_item = Blog.objects.order_by('id')[0]
    #     self.assertEqual(latest_item.title, "Testing")
    #     self.assertEqual(latest_item.text, "This is testing if the post is working")
    #
    # def test_redirects_after_POST(self):
    #     response = self.client.post('/blog/new/',
    #                                 data={'title': 'Testing', 'text': 'This is testing if the post is working'})
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response['location'], 'post_detail')
    #
    # def test_displays_changes_cv(self):
    #     CV.objects.create(title='hello test', text='this is the text')
    #     Blog.objects.create(title='Testing the goat', text='Oh blah blah blah testing')
    #
    #     response = self.client.get('/blog/')
    #
    #     self.assertIn('hello test', response.content.decode())
    #     self.assertIn('Testing the goat', response.content.decode())
    #     self.assertIn('this is the text', response.content.decode())
    #     self.assertIn('Oh blah blah blah testing', response.content.decode())
    #
    # def test_saving_and_retrieving_education(self):
    #     first_blog = Blog()
    #     first_blog.title = 'Blog post test 1'
    #     first_blog.text = 'Hello this is a blog post'
    #     first_blog.save()
    #
    #     second_blog = Blog()
    #     second_blog.title = 'Blog post test 2'
    #     second_blog.text = 'Hello this is also blog post even longer'
    #     second_blog.save()
    #
    #     saved_blogs = Blog.objects.all()
    #     self.assertEqual(saved_blogs.count(), 2)
    #
    #     first_saved_blog = saved_blogs[0]
    #     second_save_blog = saved_blogs[1]
    #     self.assertEqual(first_saved_blog.Title, 'Blog post test 1')
    #     self.assertEqual(second_save_blog.Title, 'Blog post test 2')
    #     self.assertEqual(first_saved_blog.text, 'Hello this is a blog post')
    #     self.assertEqual(second_save_blog.text, 'Hello this is also blog post even longer')

    # def test_saving_and_retrieving_tech_skills(self):
    #     first_blog = Blog()
    #     first_blog.title = 'Blog post test 1'
    #     first_blog.text = 'Hello this is a blog post'
    #     first_blog.save()
    #
    #     second_blog = Blog()
    #     second_blog.title = 'Blog post test 2'
    #     second_blog.text = 'Hello this is also blog post even longer'
    #     second_blog.save()
    #
    #     saved_blogs = Blog.objects.all()
    #     self.assertEqual(saved_blogs.count(), 2)
    #
    #     first_saved_blog = saved_blogs[0]
    #     second_save_blog = saved_blogs[1]
    #     self.assertEqual(first_saved_blog.Title, 'Blog post test 1')
    #     self.assertEqual(second_save_blog.Title, 'Blog post test 2')
    #     self.assertEqual(first_saved_blog.text, 'Hello this is a blog post')
    #     self.assertEqual(second_save_blog.text, 'Hello this is also blog post even longer')

    # def test_saving_and_retrieving_academic_projects(self):
    #     first_blog = Blog()
    #     first_blog.title = 'Blog post test 1'
    #     first_blog.text = 'Hello this is a blog post'
    #     first_blog.save()
    #
    #     second_blog = Blog()
    #     second_blog.title = 'Blog post test 2'
    #     second_blog.text = 'Hello this is also blog post even longer'
    #     second_blog.save()
    #
    #     saved_blogs = Blog.objects.all()
    #     self.assertEqual(saved_blogs.count(), 2)
    #
    #     first_saved_blog = saved_blogs[0]
    #     second_save_blog = saved_blogs[1]
    #     self.assertEqual(first_saved_blog.Title, 'Blog post test 1')
    #     self.assertEqual(second_save_blog.Title, 'Blog post test 2')
    #     self.assertEqual(first_saved_blog.text, 'Hello this is a blog post')
    #     self.assertEqual(second_save_blog.text, 'Hello this is also blog post even longer')
    #
    # def test_saving_and_retrieving_awards(self):
    #     first_blog = Blog()
    #     first_blog.title = 'Blog post test 1'
    #     first_blog.text = 'Hello this is a blog post'
    #     first_blog.save()
    #
    #     second_blog = Blog()
    #     second_blog.title = 'Blog post test 2'
    #     second_blog.text = 'Hello this is also blog post even longer'
    #     second_blog.save()
    #
    #     saved_blogs = Blog.objects.all()
    #     self.assertEqual(saved_blogs.count(), 2)
    #
    #     first_saved_blog = saved_blogs[0]
    #     second_save_blog = saved_blogs[1]
    #     self.assertEqual(first_saved_blog.Title, 'Blog post test 1')
    #     self.assertEqual(second_save_blog.Title, 'Blog post test 2')
    #     self.assertEqual(first_saved_blog.text, 'Hello this is a blog post')
    #     self.assertEqual(second_save_blog.text, 'Hello this is also blog post even longer')
    #
    # def test_saving_and_retrieving_education(self):
    #     first_blog = Blog()
    #     first_blog.title = 'Blog post test 1'
    #     first_blog.text = 'Hello this is a blog post'
    #     first_blog.save()
    #
    #     second_blog = Blog()
    #     second_blog.title = 'Blog post test 2'
    #     second_blog.text = 'Hello this is also blog post even longer'
    #     second_blog.save()
    #
    #     saved_blogs = Blog.objects.all()
    #     self.assertEqual(saved_blogs.count(), 2)
    #
    #     first_saved_blog = saved_blogs[0]
    #     second_save_blog = saved_blogs[1]
    #     self.assertEqual(first_saved_blog.Title, 'Blog post test 1')
    #     self.assertEqual(second_save_blog.Title, 'Blog post test 2')
    #     self.assertEqual(first_saved_blog.text, 'Hello this is a blog post')
    #     self.assertEqual(second_save_blog.text, 'Hello this is also blog post even longer')


class PortfolioPageTest(TestCase):
    def test_root_url_resolves_to_project_view(self):
        found = resolve('/portfolio/')
        self.assertEqual(found.func, project_list)

    def test_cv_page_returns_correct_html(self):
        response = self.client.get('/portfolio/')
        self.assertTemplateUsed(response, 'app/portfolio.html')
