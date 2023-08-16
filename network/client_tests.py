from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from django.conf import settings

from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


class MySeleniumTests(StaticLiveServerTestCase):

    def setUp(self):
        settings.SELENIUM_LOGIN_START_PAGE = 'http://127.0.0.1:8000'
        settings.CSRF_COOKIE_SECURE = False
        settings.SESSION_COOKIE_SECURE = False
        
        self.selenium = WebDriver(service=Service(GeckoDriverManager().install()))
        self.selenium.implicitly_wait(10)

    def tearDown(self):
        self.selenium.quit()

    def selenium_login(self):
        self.selenium.get('http://127.0.0.1:8000/login')
        username = self.selenium.find_element(By.ID, "username")
        password = self.selenium.find_element(By.ID, "password")
        submit  = self.selenium.find_element(By.ID, "submit")
        username.send_keys("Marwan")
        password.send_keys("apple")
        submit.click()

    def test_like(self):
        self.selenium_login()
        like = self.selenium.find_element(By.ID, "like-button")
        p = like.find_element(By.XPATH, "..")
        likes = int(p.get_attribute('innerHTML')[114: ])
        like.click()
        unlike = self.selenium.find_element(By.ID, "unlike-button")
        likes += 1
        self.assertEqual(int(p.get_attribute('innerHTML')[122: ]), likes)

    def test_unlike(self):
        self.selenium_login()
        unlike = self.selenium.find_element(By.ID, "unlike-button")
        p = unlike.find_element(By.XPATH, "..")
        likes = int(p.get_attribute('innerHTML')[122: ])
        unlike.click()
        like = self.selenium.find_element(By.ID, "like-button")
        likes -= 1
        self.assertEqual(int(p.get_attribute('innerHTML')[114: ]), likes)

    def test_edit(self):
        self.selenium_login()
        edit_button = self.selenium.find_element(By.ID, "edit_btn")
        post_box = edit_button.find_element(By.XPATH, "..")
        post_text = post_box.find_element(By.ID, "post-text")
        text = post_text.text
        edit_button.click()
        text_box = post_box.find_element(By.ID, "text-box")
        save_button = post_box.find_element(By.ID, "save-btn")
        text_box.send_keys("Apple")
        save_button.click()
        post_text = post_box.find_element(By.ID, "post-text")
        self.assertEqual(post_text.text, "Apple")
        edit_button = post_box.find_element(By.ID, "edit_btn")
        edit_button.click()
        text_box = post_box.find_element(By.ID, "text-box")
        save_button = post_box.find_element(By.ID, "save-btn")
        text_box.send_keys(text)
        save_button.click()
    
    def test_arrow(self):
        self.selenium.get('http://127.0.0.1:8000/')
        next = self.selenium.find_element(By.ID, "next-button")
        date = self.selenium.find_element(By.ID, "date")
        text = date.text
        colon_pos = text.find(":")
        first_pg_minutes = text[colon_pos + 1: colon_pos + 3]
        prev_current_pg = int(self.selenium.execute_script("return current_pg"))
        next.click()
        current_pg = int(self.selenium.execute_script("return current_pg"))
        date = self.selenium.find_element(By.ID, "date")
        text = date.text
        colon_pos = text.find(":")
        second_pg_minutes = text[colon_pos + 1: colon_pos + 3]
        if prev_current_pg != current_pg:
            self.assertNotEqual(first_pg_minutes, second_pg_minutes)
        else:
            self.assertEqual(first_pg_minutes, second_pg_minutes)
    
    def test_num(self):
        self.selenium.get('http://127.0.0.1:8000/')
        one = self.selenium.find_element(By.ID, "1")
        date = self.selenium.find_element(By.ID, "date")
        text = date.text
        colon_pos = text.find(":")
        first_pg_minutes = text[colon_pos + 1: colon_pos + 3]
        prev_current_pg = int(self.selenium.execute_script("return current_pg"))
        one.click()
        current_pg = int(self.selenium.execute_script("return current_pg"))
        date = self.selenium.find_element(By.ID, "date")
        text = date.text
        colon_pos = text.find(":")
        second_pg_minutes = text[colon_pos + 1: colon_pos + 3]
        self.assertEqual(prev_current_pg, current_pg)
        self.assertEqual(first_pg_minutes, second_pg_minutes)

    def test_follow_fail(self):
        self.selenium_login()
        self.selenium.get('http://127.0.0.1:8000/user?name=Marwan')
        try:
            follow_button = self.selenium.find_element(By.ID, "follow")
            unfollow_button = self.selenium.find_element(By.ID, "unfollow")
        except NoSuchElementException:
            follow_button = False
            unfollow_button = False
        self.assertFalse(follow_button)
        self.assertFalse(unfollow_button)
    
    def test_follow(self):
        self.selenium_login()
        self.selenium.get('http://127.0.0.1:8000/user?name=An')
        prev_followers = int(self.selenium.find_element(By.ID, "followers").text[11: ])
        try:
            button = WebDriverWait(self.selenium, 1).until(EC.element_to_be_clickable((By.ID, 'follow')))
            button_id = "follow"
        except TimeoutException:
            button = WebDriverWait(self.selenium, 1).until(EC.element_to_be_clickable((By.ID, 'unfollow')))
            button_id = "unfollow"
        button.click()
        if button_id == "follow":
            cur_followers = int(self.selenium.find_element(By.ID, "followers").text[11: ])
            self.assertEqual(cur_followers, prev_followers + 1)
            button = self.selenium.find_element(By.ID, "unfollow")
            button.click()
            cur_followers = int(self.selenium.find_element(By.ID, "followers").text[11: ])
            self.assertEqual(cur_followers, prev_followers)
            button = self.selenium.find_element(By.ID, "follow")
        else:
            cur_followers = int(self.selenium.find_element(By.ID, "followers").text[11: ])
            self.assertEqual(cur_followers, prev_followers - 1)
            button = self.selenium.find_element(By.ID, "follow")
            button.click()
            cur_followers = int(self.selenium.find_element(By.ID, "followers").text[11: ])
            self.assertEqual(cur_followers, prev_followers)
            button = self.selenium.find_element(By.ID, "unfollow")

    def test_post(self):
        self.selenium_login()
        text_box = self.selenium.find_element(By.ID, "id_text")
        submit_post = self.selenium.find_element(By.ID, "post-submit")
        text_box.send_keys("AA")
        submit_post.click()
        poster = self.selenium.find_element(By.CSS_SELECTOR, "h3").text
        post_text = self.selenium.find_element(By.ID, "post-text").text
        self.assertEqual(poster, "Marwan")
        self.assertEqual(post_text, "AA")

        