import time
import pytest
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
from pages.home_page import HomePage

load_dotenv()
BASE_URL      = os.getenv("URL")
ALL_DATA_URL = os.getenv("URL_ALL_DATA")


def test_home_url(driver, base_url):
    home = HomePage(driver, base_url)
    try:
        if not home.is_loaded():
            home.load()
            assert home.is_loaded(), "Homepage did not load successfully"
    except Exception as e:
        print(f"Error loading homepage: {e}")
    ds_page = home.go_to_all_data_page()
    assert ds_page.is_loaded(), "Con_002: Datasets page failed to load"
    actual_url = driver.current_url
    assert actual_url == "https://civicdataspace.in/datasets"
    # assert actual_url == "https://civicdataspace.in/datasets?size=9&page=1&sort=recent"

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
