import time

from selenium import webdriver
import unittest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class CVEditTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

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
            any('University of Birmingham' in text.text for text in school_texts)
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

    def test020_add_edit_cv_education(self):
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

    def test040_edit_new_tech_skills(self):
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

        # Notices Edit button next to Tech Skills

        edit_button = self.browser.find_elements_by_id('edit_tech_skills_btn')[0]

        # Clicks edit button
        edit_button.click()
        time.sleep(1)

        # Sees the listed tech skills changes to text boxes

        # See changes
        techskills_text_boxes = self.browser.find_elements_by_class('edit_tech_skills_box')

        # Focuses on text box that is filled with django
        for skills in techskills_text_boxes:
            if skills.get_attribute('value') == 'Django':
                skills.clear()

                # Replace with Java
                skills.send_keys('Java')
                break

        # Press save button
        # Save form
        save_button = self.browser.find_element_by_class_name('btn')
        save_button.click()
        time.sleep(1)

        # See changes
        techskills_list = self.browser.find_elements_by_css_selector('li')

        self.assertTrue(any('Java' in item.text for item in techskills_list))


if __name__ == '__main__':
    unittest.main(warnings='ignore')
