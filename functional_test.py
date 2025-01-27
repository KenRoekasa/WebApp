import time

from django.forms import DateInput
from selenium import webdriver
import unittest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class CVEditTest(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        self.browser = webdriver.Chrome("D:\Desktop\chromedriver.exe",
                                        options=chrome_options)

        # self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test010_add_new_cv_education(self):
        # User opens site add a new to their education
        self.browser.get('http://127.0.0.1:8000')

        # User clicks on CV on the navigation bar
        cv_nav = self.browser.find_element_by_link_text('CV')
        cv_nav.click()

        time.sleep(1)

        # Sees the CV page
        # They notices the page title
        self.assertEqual('Kenny Roekasa', self.browser.title)

        # Locates the Education section
        headers = self.browser.find_elements_by_tag_name('h1')
        self.assertTrue(any('Education' in h.text for h in headers))

        # Notices there's no add button

        try:
            self.assertIsNone(self.browser.find_element_by_id('education_add_button'))
        except NoSuchElementException:
            pass

        # They login
        self.browser.get('http://127.0.0.1:8000/admin')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('kenny')
        password_box.send_keys('adminadmin123')
        password_box.send_keys(Keys.ENTER)
        time.sleep(1)

        time.sleep(1)
        # Goes back to cv page
        self.browser.get('http://127.0.0.1:8000/cv/')

        # Notices an add button
        add_button = self.browser.find_element_by_id('education_add_button')
        self.assertIsNotNone(add_button)
        # Presses the add button
        add_button.click()

        time.sleep(1)
        # Displays a form overlaying the cv page it has been greyed out in the background

        # User enters School
        input_school_box = self.browser.find_element_by_id('id_school')
        input_school_box.send_keys("University of Birmingham")

        # User enters location
        input_location_box = self.browser.find_element_by_id('id_location')
        input_location_box.send_keys('Edgbaston, Birmingham')

        # User enters the Start and End Year
        input_start_year = Select(self.browser.find_element_by_id('id_start_year'))
        input_end_year = Select(self.browser.find_element_by_id('id_end_year'))

        input_start_year.select_by_visible_text("2017")
        input_end_year.select_by_visible_text("2021")

        # Enter Field of study
        field_of_study = self.browser.find_element_by_id('id_field_of_study')
        field_of_study.send_keys('Computer Science')

        # Enters Description
        input_description_box = self.browser.find_element_by_id('id_description')
        input_description_box.send_keys(
            'First Year Software Workshop - 90% Robot Programming - 80% Introduction to Software Engineering - 71% First Year - Year Average 73%')
        # Press saves
        save_button = self.browser.find_element_by_class_name('btn')
        save_button.click()
        time.sleep(1)

        # Redirects to main cv page
        # Sees the changes have been affected to the page

        school_texts = self.browser.find_elements_by_class_name('school')
        year_text = self.browser.find_elements_by_class_name('year')

        location_text = self.browser.find_elements_by_class_name('location')

        description_text = self.browser.find_elements_by_tag_name('p')

        field_of_study_text = self.browser.find_elements_by_class_name('field_of_study')

        self.assertTrue(
            any(text.text == 'University of Birmingham' for text in school_texts)
        )

        self.assertTrue(
            any(text.text == 'Computer Science' for text in field_of_study_text)

        )

        self.assertTrue(
            any(year.text == '2017-2021' for year in year_text)
        )

        self.assertTrue(
            any(
                text.text == 'First Year Software Workshop - 90% Robot Programming - 80% Introduction to Software Engineering - 71% First Year - Year Average 73%'
                for text in description_text)
            , description_text)

        self.assertTrue(
            any(text.text == 'Edgbaston, Birmingham' for text in location_text)
        )

    def test020_edit_delete_cv_education(self):
        # They login
        self.browser.get('http://127.0.0.1:8000/admin')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('kenny')
        password_box.send_keys('adminadmin123')
        password_box.send_keys(Keys.ENTER)
        time.sleep(1)

        time.sleep(1)
        # Goes back to cv page
        self.browser.get('http://127.0.0.1:8000/cv/')

        # Notices Edit button next to University of Birmingham

        edit_button = self.browser.find_elements_by_id('edit_education_btn')[0]

        # Clicks edit button
        edit_button.click()
        time.sleep(1)

        # Sees the form has already been filed in with the existing information

        # User enters School
        input_school_box = self.browser.find_element_by_id('id_school')
        self.assertEqual('University of Birmingham', input_school_box.get_attribute('value'))

        # User enters location
        input_location_box = self.browser.find_element_by_id('id_location')
        self.assertEqual('Edgbaston, Birmingham', input_location_box.get_attribute('value'))

        # User enters the Start and End Year
        input_start_year = Select(self.browser.find_element_by_id('id_start_year'))
        input_end_year = Select(self.browser.find_element_by_id('id_end_year'))

        self.assertEqual("2017", input_start_year.first_selected_option.text)
        self.assertEqual("2021", input_end_year.first_selected_option.text)

        # Enter Field of study
        field_of_study = self.browser.find_element_by_id('id_field_of_study')
        self.assertEqual('Computer Science', field_of_study.get_attribute('value'))

        # Enters Description
        input_description_box = self.browser.find_element_by_id('id_description')
        self.assertEqual(
            'First Year Software Workshop - 90% Robot Programming - 80% Introduction to Software Engineering - 71% First Year - Year Average 73%',
            input_description_box.get_attribute('value'))

        # Edits field of study to Maths
        field_of_study = self.browser.find_element_by_id('id_field_of_study')
        field_of_study.clear()
        field_of_study.send_keys('Maths')

        # Save form
        save_button = self.browser.find_element_by_class_name('btn')
        save_button.click()
        time.sleep(1)

        # See changes
        field_of_study_text = self.browser.find_elements_by_class_name('field_of_study')

        self.assertTrue(
            any(text.text == 'Maths' for text in field_of_study_text)
        )

        # Clicks edit button again
        edit_button = self.browser.find_elements_by_id('edit_education_btn')[0]
        edit_button.click()

        delete_button = self.browser.find_element_by_id('delete_btn')
        delete_button.click()
        time.sleep(1)

        # See changes
        # Redirects to main cv page
        # Sees the changes have been affected to the page

        school_texts = self.browser.find_elements_by_class_name('school')
        year_text = self.browser.find_elements_by_class_name('year')

        location_text = self.browser.find_elements_by_class_name('location')

        description_text = self.browser.find_elements_by_tag_name('p')

        field_of_study_text = self.browser.find_elements_by_class_name('field_of_study')

        self.assertEqual([], school_texts)
        self.assertEqual([], year_text)
        self.assertEqual([], field_of_study_text)
        self.assertEqual([], location_text)
        self.assertEqual([], description_text)

    def test030_add_new_tech_skills(self):
        # They login
        self.browser.get('http://127.0.0.1:8000/admin')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('kenny')
        password_box.send_keys('adminadmin123')
        password_box.send_keys(Keys.ENTER)
        time.sleep(1)

        time.sleep(1)
        # Goes back to cv page
        self.browser.get('http://127.0.0.1:8000/cv/')

        # Locates the Tech Skills section
        headers = self.browser.find_elements_by_tag_name('h1')
        self.assertTrue(any('Tech Skills' in h.text for h in headers))

        # Notices Add button
        add_button = self.browser.find_elements_by_id('add_tech_skills_btn')[0]
        # Presses added button
        add_button.click()
        time.sleep(1)

        # Enters Django into Text box
        input_field = self.browser.find_element_by_id('id_skill')
        input_field.send_keys('Django')

        # Press saves
        # Save form
        save_button = self.browser.find_element_by_class_name('btn')
        save_button.click()
        time.sleep(1)
        # See changes
        techskills_list = self.browser.find_elements_by_css_selector('li')

        self.assertTrue(any('Django' in item.text for item in techskills_list))

    def test040_edit_delete_tech_skills(self):
        # They login
        self.browser.get('http://127.0.0.1:8000/admin')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('kenny')
        password_box.send_keys('adminadmin123')
        password_box.send_keys(Keys.ENTER)
        time.sleep(1)
        # Goes back to cv page
        self.browser.get('http://127.0.0.1:8000/cv/')

        # Notices Edit button next to a Tech Skills

        edit_button = self.browser.find_elements_by_id('edit_tech_skills_btn')[0]

        # Clicks edit button
        edit_button.click()
        time.sleep(1)

        # Sees form is prefilled
        skills_textbox = self.browser.find_element_by_id('id_skill')
        # Focuses on text box that is filled with django
        self.assertEqual('Django', skills_textbox.get_attribute('value'))
        skills_textbox.clear()
        skills_textbox.send_keys('Java')

        # Press save button
        # Save form
        save_button = self.browser.find_element_by_class_name('btn')
        save_button.click()
        time.sleep(1)

        # See changes
        techskills_list = self.browser.find_elements_by_css_selector('li')

        self.assertTrue(any('Java' in item.text for item in techskills_list))

        edit_button = self.browser.find_elements_by_id('edit_tech_skills_btn')[0]

        # clicks edit button again
        edit_button.click()
        time.sleep(1)

        # Press delete button
        delete_button = self.browser.find_element_by_id('delete_btn')
        delete_button.click()
        time.sleep(1)

        # See changes
        techskills_list = self.browser.find_elements_by_css_selector('li')

        self.assertTrue(any('Java' not in item.text for item in techskills_list))

    def test060_add_new_cv_work_experience(self):
        # They login
        self.browser.get('http://127.0.0.1:8000/admin')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('kenny')
        password_box.send_keys('adminadmin123')
        password_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # User opens site add a new to their education
        self.browser.get('http://127.0.0.1:8000/cv')

        time.sleep(1)

        # Locates the Work Experience section
        headers = self.browser.find_elements_by_tag_name('h1')
        self.assertTrue(any('Work Experience' in h.text for h in headers))

        # Notices an add button
        add_button = self.browser.find_element_by_id('work_experience_add_button')
        # Presses the add button
        add_button.click()

        time.sleep(1)
        # Displays a form overlaying the cv page it has been greyed out in the background

        # User enters School
        input_company_box = self.browser.find_element_by_id('id_company')
        input_company_box.send_keys("Google")

        # User enters location
        input_location_box = self.browser.find_element_by_id('id_location')
        input_location_box.send_keys('Silicon Valley')

        # User enters location
        input_location_box = self.browser.find_element_by_id('id_title')
        input_location_box.send_keys('CEO')

        # User enters the Start and End date
        input_start_date = self.browser.find_element_by_id('id_start_date')
        input_end_date = self.browser.find_element_by_id('id_end_date')
        input_start_date.click()
        # ONLY works on chrome
        input_start_date.send_keys("20072017")
        # input_start_date.send_keys("20-Aug-1985")

        input_end_date.click()
        input_end_date.send_keys("06032020")

        # Enters Description
        input_description_box = self.browser.find_element_by_id('id_description')
        input_description_box.send_keys(
            'I did this and this and this')

        # Press saves
        save_button = self.browser.find_element_by_class_name('btn')
        save_button.click()
        time.sleep(1)

        # Redirects to main cv page
        # Sees the changes have been affected to the page

        title_texts = self.browser.find_elements_by_class_name('title')
        company_text = self.browser.find_elements_by_class_name('company')

        location_text = self.browser.find_elements_by_class_name('location')
        date_text = self.browser.find_elements_by_class_name('date')

        description_text = self.browser.find_elements_by_tag_name('p')

        self.assertTrue(
            any(text.text == 'CEO' for text in title_texts)
        )

        self.assertTrue(
            any(year.text == 'Google' for year in company_text)
        )

        self.assertTrue(
            any(
                text.text == 'I did this and this and this'
                for text in description_text)
            , description_text)

        self.assertTrue(
            any(text.text == 'Silicon Valley' for text in location_text)
        )
        self.assertTrue(
            any(date.text == 'July 2017 - March 2020' for date in date_text)
        )

    def test070_edit_delete_cv_work_experience(self):
        # They login
        self.browser.get('http://127.0.0.1:8000/admin')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('kenny')
        password_box.send_keys('adminadmin123')
        password_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # User opens site add a new to their education
        self.browser.get('http://127.0.0.1:8000/cv')

        time.sleep(1)

        # Notices an edit button
        edit_button = self.browser.find_element_by_id('work_experience_edit_button')
        # Presses the edit button
        edit_button.click()

        time.sleep(1)
        # Displays a form overlaying the cv page it has been greyed out in the background

        # User enters company
        input_company_box = self.browser.find_element_by_id('id_company')
        self.assertEqual("Google", input_company_box.get_attribute('value'))

        # User enters location
        input_location_box = self.browser.find_element_by_id('id_location')

        self.assertEqual('Silicon Valley', input_location_box.get_attribute('value'))

        # User enters title
        input_title_box = self.browser.find_element_by_id('id_title')
        input_title_box.clear()
        input_title_box.send_keys('Owner')

        # User enters the Start and End date
        input_start_date = self.browser.find_element_by_id('id_start_date')
        input_end_date = self.browser.find_element_by_id('id_end_date')
        input_start_date
        # ONLY works on chrome
        self.assertEqual("2017-07-20", input_start_date.get_attribute('value'))

        self.assertEqual("2020-03-06", input_end_date.get_attribute('value'))

        # Enters Description
        input_description_box = self.browser.find_element_by_id('id_description')
        self.assertEqual(
            'I did this and this and this', input_description_box.get_attribute('value'))

        # Press saves
        save_button = self.browser.find_element_by_class_name('btn')
        save_button.click()
        time.sleep(1)

        # Redirects to main cv page
        # Sees the changes have been affected to the page

        title_texts = self.browser.find_elements_by_class_name('title')
        company_text = self.browser.find_elements_by_class_name('company')

        location_text = self.browser.find_elements_by_class_name('location')
        date_text = self.browser.find_elements_by_class_name('date')

        description_text = self.browser.find_elements_by_tag_name('p')

        self.assertTrue(
            any(text.text == 'Owner' for text in title_texts)
        )

        self.assertTrue(
            any(year.text == 'Google' for year in company_text)
        )

        self.assertTrue(
            any(
                text.text == 'I did this and this and this'
                for text in description_text)
            , description_text)

        self.assertTrue(
            any(text.text == 'Silicon Valley' for text in location_text)
        )
        self.assertTrue(
            any(date.text == 'July 2017 - March 2020' for date in date_text)
        )

        # clicks edit button again
        edit_button = self.browser.find_element_by_id('work_experience_edit_button')
        edit_button.click()
        time.sleep(1)

        # Press delete button
        delete_button = self.browser.find_element_by_id('delete_btn')
        delete_button.click()
        time.sleep(1)

        title_texts = self.browser.find_elements_by_class_name('title')
        company_text = self.browser.find_elements_by_class_name('company')

        location_text = self.browser.find_elements_by_class_name('location')
        date_text = self.browser.find_elements_by_class_name('date')

        description_text = self.browser.find_elements_by_tag_name('p')

        self.assertEqual([], title_texts)
        self.assertEqual([], company_text)
        self.assertEqual([], date_text)
        self.assertEqual([], location_text)
        self.assertEqual([], description_text)

    def test080_add_new_cv_academic_project(self):
        # They login
        self.browser.get('http://127.0.0.1:8000/admin')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('kenny')
        password_box.send_keys('adminadmin123')
        password_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # User opens site add a new to their education
        self.browser.get('http://127.0.0.1:8000/cv')

        time.sleep(1)

        # Locates the Work Experience section
        headers = self.browser.find_elements_by_tag_name('h1')
        self.assertTrue(any('Academic Projects' in h.text for h in headers))

        # Notices an add button
        add_button = self.browser.find_element_by_id('academic_projects_add_button')
        # Presses the add button
        add_button.click()

        time.sleep(1)
        # Displays a form overlaying the cv page it has been greyed out in the background

        # User enters Title
        input_title = self.browser.find_element_by_id('id_title')
        input_title.send_keys("Flappy Bird")

        # User enters the Start and End date
        input_start_date = self.browser.find_element_by_id('id_start_date')
        input_end_date = self.browser.find_element_by_id('id_end_date')
        input_start_date.click()
        # ONLY works on chrome
        input_start_date.send_keys("05022019")

        input_end_date.click()
        input_end_date.send_keys("20052019")

        # Enters Description
        input_description_box = self.browser.find_element_by_id('id_description')
        input_description_box.send_keys(
            'I did this and this and this \n also did this \n this aswell')

        # Press saves
        save_button = self.browser.find_element_by_class_name('btn')
        save_button.click()
        time.sleep(1)

        # Redirects to main cv page
        # Sees the changes have been affected to the page

        title_texts = self.browser.find_elements_by_class_name('project_title')
        date_texts = self.browser.find_elements_by_class_name('project_date')

        description_text = self.browser.find_elements_by_tag_name('p')

        self.assertTrue(
            any('Flappy Bird' in text.text for text in title_texts)
        )

        self.assertTrue(
            any('I did this and this and this' in text.text for text in
                description_text))
        self.assertTrue(
            any('also did this' in text.text for text in
                description_text))
        self.assertTrue(
            any('this aswell' in text.text for text in
                description_text))

        self.assertTrue(
            any(date.text == 'February 2019 - May 2019' for date in date_texts)

        )

    def test090_edit_delete_cv_academic_project(self):
        # They login
        self.browser.get('http://127.0.0.1:8000/admin')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('kenny')
        password_box.send_keys('adminadmin123')
        password_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # User opens site add a new to their education
        self.browser.get('http://127.0.0.1:8000/cv')

        time.sleep(1)

        # Notices an add button
        edit_button = self.browser.find_element_by_id('academic_projects_edit_button')
        # Presses the add button
        edit_button.click()

        time.sleep(1)
        # Displays a form overlaying the cv page it has been greyed out in the background

        # User enters School
        input_title_box = self.browser.find_element_by_id('id_title')
        self.assertEqual("Flappy Bird", input_title_box.get_attribute('value'))

        # User enters the Start and End date
        input_start_date = self.browser.find_element_by_id('id_start_date')
        input_end_date = self.browser.find_element_by_id('id_end_date')
        input_start_date
        # ONLY works on chrome
        self.assertEqual("2019-02-05", input_start_date.get_attribute('value'))

        self.assertEqual("2019-05-20",
                         input_end_date.get_attribute('value'))

        # Enters Description
        input_description_box = self.browser.find_element_by_id('id_description')
        input_description_box.clear()
        input_description_box.send_keys("I change to this")

        # Press saves
        save_button = self.browser.find_element_by_class_name('btn')
        save_button.click()
        time.sleep(1)

        # Redirects to main cv page
        # Sees the changes have been affected to the page

        title_texts = self.browser.find_elements_by_class_name('project_title')

        date_text = self.browser.find_elements_by_class_name('project_date')

        description_text = self.browser.find_elements_by_tag_name('p')

        self.assertTrue(
            any('Flappy Bird' in text.text for text in title_texts)
        )

        self.assertTrue(
            any(
                text.text == 'I change to this'
                for text in description_text)
        )

        self.assertTrue(
            any(date.text == 'February 2019 - May 2019' for date in date_text)
        )

        # clicks edit button again
        edit_button = self.browser.find_element_by_id('academic_projects_edit_button')
        edit_button.click()
        time.sleep(1)

        # Press delete button
        delete_button = self.browser.find_element_by_id('delete_btn')
        delete_button.click()
        time.sleep(1)

        title_texts = self.browser.find_elements_by_class_name('project_title')
        date_texts = self.browser.find_elements_by_class_name('project_date')

        description_text = self.browser.find_elements_by_tag_name('p')

        self.assertEqual([], title_texts)
        self.assertEqual([], date_texts)

        self.assertEqual([], description_text)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
