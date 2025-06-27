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
