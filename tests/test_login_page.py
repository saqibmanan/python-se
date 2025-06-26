import time
import pytest
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL      = os.getenv("URL")
ALL_DATA_URL = os.getenv("URL_ALL_DATA")

class TestLoginPage:
    def test_home_url(self, driver):
        driver.get(BASE_URL)
        time.sleep(5)
        driver.get(ALL_DATA_URL)
        # # Type username
        # username_input = driver.find_element(By.ID, "user-name")
        # username_input.send_keys("standard_user")
        #
        # # Type password
        # password_input = driver.find_element(By.ID, "password")
        # password_input.send_keys("secret_sauce")
        #
        # # Click on the login button
        # login_btn = driver.find_element(By.ID, "login-button")
        # login_btn.click()

        # URL Validation
        actual_url = driver.current_url
        # assert actual_url == "https://civicdataspace.in/"
        assert actual_url == "https://civicdataspace.in/datasets?size=9&page=1&sort=recent"

        # time.sleep(2)
    # def test_all_data_url(self, driver):
    #     driver.get(ALL_DATA_URL)
    #     time.sleep(5)
    #     actual_url_data = driver.current_url
    #     assert actual_url_data == "https://civicdataspace.in/datasets?size=9&page=1&sort=recent"
    # @pytest.mark.parametrize("username, password, error", [
    #     ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
    #     ("invalidUser", "invalidPass", "Epic sadface: Username and password do not match any user in this service")])
    # def test_invalid_login(self, driver, username, password, error):
    #     driver.get("https://www.saucedemo.com/")
    #     # time.sleep(2)
    #
    #     # Type username
    #     username_input = driver.find_element(By.ID, "user-name")
    #     username_input.send_keys(username)
    #
    #     # Type password
    #     password_input = driver.find_element(By.ID, "password")
    #     password_input.send_keys(password)
    #
    #     # Click on the login button
    #     login_btn = driver.find_element(By.ID, "login-button")
    #     login_btn.click()
    #
    #     # Error message validation
    #     error_msg_h3 = driver.find_element(By.TAG_NAME, "h3")
    #     error_msg_text = error_msg_h3.text
    #     assert error_msg_text == error
    #
    #     # time.sleep(2)
