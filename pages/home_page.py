# pages/home_page.py

import os
from dotenv import load_dotenv
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage

# ─── Consumer‐flow imports (PLACE YOUR ORIGINAL IMPORTS HERE) ─────────────────────
#
from locators.homepage_locators import HomepageLocators
from pages.dataset_page import DatasetPage


# ────────────────────────────────────────────────────────────────────────────────

# ─── Provider‐flow imports ────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────

# ─── Load environment variables once ───────────────────────────────────────────────
load_dotenv()

# ────────────────────────────────────────────────────────────────────────────────


class HomePage(BasePage):
    """


    Contains:
      1) Consumer‐flow navigation methods (e.g. go_to_about, go_to_all_data_page, etc.)
      2) A unified go_to_login(...) for consumer vs provider login
    """

    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = base_url.rstrip("/") + "/"
        
    def load(self) -> None:
        """Navigate to the site root once."""
        self.driver.get(os.getenv("URL"))

    def is_loaded(self, timeout: int = 5) -> bool:
        """
        Returns True once the login‐form container is visible.
        We wait on the FORM locator.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, HomepageLocators.ICON))
            )
            return True
        except TimeoutException:
            return False


    def go_to_all_data_page(self) -> DatasetPage:
        """Navigate to the Datasets tab, falling back to direct navigation."""

        # Dismiss the cookie consent banner if it appears.  We keep the wait
        # short so a missing banner doesn't delay page navigation.
        try:
            bann = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.ID, "cookieConsentAccept"))
            )
            bann.click()
        except TimeoutException:
            pass

        try:
            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, HomepageLocators.TAB_DATASETS))
            )
            btn.click()
        except TimeoutException:
            # If the datasets tab is not clickable (e.g. due to dynamic layout),
            # navigate directly to the datasets URL instead.
            target = os.getenv("URL_ALL_DATA") or f"{self.url.rstrip('/')}/datasets"
            self.driver.get(target)

        # Return a DatasetPage instance for further interactions
        return DatasetPage(self.driver)
