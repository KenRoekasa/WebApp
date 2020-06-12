from django.contrib.auth.models import User
from django.db.models.functions import datetime
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import resolve
from django.utils import timezone

from .views import home, cv, project_list, blog_list, cv_education_new, cv_education_edit
from .models import Blog, Project, Education


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
        self.assertTemplateUsed(response, 'app/blog_list.html')

    def test_blog_edit_page_returns_correct_html(self):
        response = self.client.get('/blog/new/')
        self.assertTemplateUsed(response, 'app/blog_new.html')

    def test_blog_edit_page_save_POST_request(self):
        password = 'mypassword'

        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)

        # You'll need to log him in before you can send requests through the client
        self.client.login(username=my_admin.username, password=password)

        response = self.client.post('/blog/new/',
                                    data={'title': 'Testing', 'text': 'This is testing if the post is working'})
        # self.assertIn('Testing', response.content.decode())
        # self.assertIn('This is testing if the post is working', response.content.decode())
        # Get last post
        latest_item = Blog.objects.order_by('id')[0]
        self.assertEqual(latest_item.title, "Testing")
        self.assertEqual(latest_item.text, "This is testing if the post is working")

    def test_redirects_after_POST(self):
        password = 'mypassword'

        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)

        # You'll need to log him in before you can send requests through the client
        self.client.login(username=my_admin.username, password=password)

        response = self.client.post('/blog/new/',
                                    data={'title': 'Testing', 'text': 'This is testing if the post is working'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/blog/1/')

    def test_displays_all_blogs_ordered(self):
        password = 'mypassword'

        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)

        Blog.objects.create(title='hello test', text='this is the text', author_id=1, created_date=timezone.now())
        Blog.objects.create(title='Testing the goat', text='Oh blah blah blah testing', author_id=1,
                            created_date=timezone.now())

        response = self.client.get('/blog/')

        self.assertIn('hello test', response.content.decode())
        self.assertIn('Testing the goat', response.content.decode())
        self.assertIn('this is the text', response.content.decode())
        self.assertIn('Oh blah blah blah testing', response.content.decode())

    def test_saving_and_retrieving_blog(self):
        password = 'mypassword'

        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)

        first_blog = Blog()
        first_blog.title = 'Blog post test 1'
        first_blog.text = 'Hello this is a blog post'
        first_blog.author_id = 1;
        first_blog.created_date = timezone.now()
        first_blog.save()

        second_blog = Blog()
        second_blog.title = 'Blog post test 2'
        second_blog.text = 'Hello this is also blog post even longer'
        second_blog.author_id = 1;
        second_blog.created_date = timezone.now()
        second_blog.save()

        saved_blogs = Blog.objects.all()
        self.assertEqual(saved_blogs.count(), 2)

        first_saved_blog = saved_blogs[0]
        second_save_blog = saved_blogs[1]
        self.assertEqual(first_saved_blog.title, 'Blog post test 1')
        self.assertEqual(second_save_blog.title, 'Blog post test 2')
        self.assertEqual(first_saved_blog.text, 'Hello this is a blog post')
        self.assertEqual(second_save_blog.text, 'Hello this is also blog post even longer')


class CVEducationSectionTest(TestCase):
    def test_education_new_url_resolves_to_cv_new_view(self):
        found = resolve('/cv/edit/education/new/')
        self.assertEqual(found.func, cv_education_new)

    def test_cv_education_new_edit_page_returns_correct_html(self):
        response = self.client.get('/cv/edit/education/new/')
        self.assertTemplateUsed(response, 'app/cv_education_edit.html')

    def test_cv_page_has_education_section(self):
        response = self.client.get('/cv/')
        html = response.content.decode('utf8')
        self.assertIn('<h1>Education</h1>', html)

    def test_cv_new_education_save_POST_request(self):
        response = self.client.post('/cv/edit/education/new/',
                                    data={'school': 'The school of education', 'location': 'London',
                                          'description': '1st class degree',
                                          'field_of_study': 'Comp Sci', 'start_year': "2017", 'end_year': "2021"})

        latest_item = Education.objects.all()[0]

        self.assertEqual(latest_item.school, "The school of education")
        self.assertEqual(latest_item.description, "1st class degree")
        self.assertEqual(latest_item.location, "London")
        self.assertEqual(latest_item.start_year, 2017)
        self.assertEqual(latest_item.end_year, 2021)
        self.assertEqual(latest_item.field_of_study, "Comp Sci")

    def test_displays_all_cv_education_items(self):
        Education.objects.create(school='The school of education', location='London', description='1st class degree',
                                 start_year
                                 =2017, end_year=2021, field_of_study='Comp Sci')
        response = self.client.get('/cv/')
        self.assertIn('The school of education', response.content.decode())
        self.assertIn('London', response.content.decode())
        self.assertIn('1st class degree', response.content.decode())
        self.assertIn('2017', response.content.decode())
        self.assertIn('2021', response.content.decode())
        self.assertIn('Comp Sci', response.content.decode())

    def test_education_edit_url_resolves_to_cv_edit_view(self):
        Education.objects.create(school='The school of education', location='London', description='1st class degree',
                                 start_year
                                 =2017, end_year=2021, field_of_study='Comp Sci', id=1)
        found = resolve('/cv/edit/education/edit/1')
        self.assertEqual(found.func, cv_education_edit)

    def test_cv_education_new_edit_page_returns_correct_html(self):
        Education.objects.create(school='The school of education', location='London', description='1st class degree',
                                 start_year
                                 =2017, end_year=2021, field_of_study='Comp Sci', id=1)
        response = self.client.get('/cv/edit/education/1/')
        self.assertTemplateUsed(response, 'app/cv_education_edit.html')

    def test_cv_education_edit_save_POST(self):
        Education.objects.create(school='The school of education', location='London', description='1st class degree',
                                 start_year
                                 =2017, end_year=2021, field_of_study='Comp Sci', id=1)
        response = self.client.post('/cv/edit/education/1/',
                                    data={'school': 'The school of education', 'location': 'London',
                                          'description': '1st class degree',
                                          'field_of_study': 'Maths', 'start_year': "2017", 'end_year': "2021"})

        latest_item = Education.objects.all()[0]

        self.assertEqual(latest_item.school, "The school of education")
        self.assertEqual(latest_item.description, "1st class degree")
        self.assertEqual(latest_item.location, "London")
        self.assertEqual(latest_item.start_year, 2017)
        self.assertEqual(latest_item.end_year, 2021)
        self.assertEqual(latest_item.field_of_study, "Maths")


class CVTechSkillsSectionTest(TestCase):
    def test_tech_skills_new_url_resolves_to_tech_skills_new_view(self):
        found = resolve('/cv/edit/techskills/new/')
        self.assertEqual(found.func, cv_tech_skills_new)

    def test_cv_tech_skills_new_page_returns_correct_html(self):
        response = self.client.get('/cv/edit/techskills/new/')
        self.assertTemplateUsed(response, 'app/cv_tech_skills_edit.html')

    def test_tech_skills_edit_url_resolves_to_tech_skills_edit_view(self):
        TechSkills.objects.create(skill='Django', id=1)
        found = resolve('/cv/edit/tech_skills/edit/1')
        self.assertEqual(found.func, cv_tech_skills_edit)

    def test_cv_tech_skills_edit_page_returns_correct_html(self):
        TechSkills.objects.create(skill='Django', id=1)
        response = self.client.get('/cv/edit/techskills/1')
        self.assertTemplateUsed(response, 'app/cv_tech_skills_edit.html')

    def test_cv_page_has_tech_skills_section(self):
        response = self.client.get('/cv/')
        html = response.content.decode('utf8')
        self.assertIn('<h1>Tech Skills</h1>', html)

    def test_displays_all_tech_skills_items(self):
        TechSkills.objects.create(skill='Django')
        TechSkills.objects.create(skill='Python')
        TechSkills.objects.create(skill='Java')

        response = self.client.get('/cv/')
        self.assertIn('Django', response.content.decode())
        self.assertIn('Python', response.content.decode())
        self.assertIn('Java', response.content.decode())

    def test_cv_new_tech_skills_save_POST_request(self):
        response = self.client.post('/cv/edit/techskills/new/',
                                    data={'skill': 'Django'})

        latest_item = TechSkills.objects.all()[0]

        self.assertEqual(latest_item.skill, "Django")

    def test_cv_tech_skills_edit_save_POST(self):
        TechSkills.objects.create(skill='Django', id=1)
        response = self.client.post('/cv/edit/techskills/1/',
                                    data={'skill': 'Python'})

        latest_item = Education.objects.all()[0]

        self.assertEqual(latest_item.skill, "Python")


class CVPageTest(TestCase):
    def test_root_url_resolves_to_cv_view(self):
        found = resolve('/cv/')
        self.assertEqual(found.func, cv)

    def test_cv_page_returns_correct_html(self):
        response = self.client.get('/cv/')
        self.assertTemplateUsed(response, 'app/cv.html')

    def test_cv_page_has_no_new_button_click_when_logged_out(self):
        response = self.client.get('/cv/')
        html = response.content.decode('utf8')
        self.assertNotIn('education_add_button', html)

    def test_cv_page_has_new_button_click_when_logged_in(self):
        password = 'mypassword'
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)
        self.client.login(username=my_admin.username, password=password)
        response = self.client.get('/cv/')
        html = response.content.decode('utf8')
        self.assertIn("education_add_button", html)


class PortfolioPageTest(TestCase):
    def test_root_url_resolves_to_project_view(self):
        found = resolve('/portfolio/')
        self.assertEqual(found.func, project_list)

    def test_cv_page_returns_correct_html(self):
        response = self.client.get('/portfolio/')
        self.assertTemplateUsed(response, 'app/portfolio_list.html')
