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
# from pages.about_page import AboutPage
from pages.dataset_page import DatasetPage
# from pages.consumer.publishers_page import PublishersPage
# from pages.consumer.publisher_detail_page import PublisherDetailPage
# from pages.consumer.sectors_page import SectorsPage
# from pages.consumer.usecase_page import UseCasePage

# ────────────────────────────────────────────────────────────────────────────────

# ─── Provider‐flow imports ────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────

# ─── Load environment variables once ───────────────────────────────────────────────
load_dotenv()
# BASE_URL      = os.getenv("BASE_URL")
# TEST_EMAIL    = os.getenv("TEST_EMAIL")
# TEST_PASSWORD = os.getenv("TEST_PASSWORD")
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
    
    # ─── Consumer‐flow navigation methods ───────────────────────────────────────────

    # def go_to_about(self) -> AboutPage:
    #     btn = WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, HomepageLocators.TAB_ABOUT))
    #     )
    #     btn.click()
    #     return AboutPage(self.driver)

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

    # def go_to_publishers(self) -> PublishersPage:
    #     btn = WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, HomepageLocators.TAB_PUBLISHERS))
    #     )
    #     btn.click()
    #     return PublishersPage(self.driver)
    #
    # def go_to_sectors(self) -> SectorsPage:
    #     btn = WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, HomepageLocators.TAB_SECTORS))
    #     )
    #     btn.click()
    #     return SectorsPage(self.driver)
    #
    # def go_to_usecases(self) -> UseCasePage:
    #     btn = WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, HomepageLocators.TAB_USECASES))
    #     )
    #     btn.click()
    #     return UseCasePage(self.driver)
    #
    # def is_icon_visible(self, timeout: int = 10) -> bool:
    #     """TC_HOM_01: Wait for the platform icon (logo) to be visible."""
    #     WebDriverWait(self.driver, timeout).until(
    #         EC.visibility_of_element_located((By.XPATH, HomepageLocators.ICON))
    #     )
    #     return True

    # ────────────────────────────────────────────────────────────────────────────────


    # ─── Provider‐flow login method ──────────────────────────────────────────────────

    # def go_to_login(self, flow: str = "consumer") -> Union[LoginPage, ProviderHomePage]:
    #     """
    #     Click “LOGIN / SIGN UP,” then:
    #
    #     • flow == "consumer":
    #         – Wait for the login form to appear.
    #         – Return a LoginPage so tests can fill in credentials manually.
    #
    #     • flow == "provider":
    #         – If we already detect the ProviderHomePage is visible, return it immediately.
    #         – Otherwise, click “LOGIN / SIGN UP,” wait for the form, submit EMAIL/PASSWORD,
    #           then wait up to 10 s for the dashboard header to appear—finally return ProviderHomePage.
    #
    #     Raises AssertionError if the login form never appears.
    #     """
    #     if flow.lower() == "provider":
    #         # 0) If the dashboard header is already visible, assume “already logged in”
    #         try:
    #             WebDriverWait(self.driver, 5).until(
    #                 EC.visibility_of_element_located((By.XPATH, ProviderHomepageLocators.HEADER))
    #             )
    #             return ProviderHomePage(self.driver)
    #         except TimeoutException:
    #             pass
    #
    #     # 1) Click “LOGIN / SIGN UP”
    #     WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGIN_BUTTON))
    #     ).click()
    #
    #     # 2) Wait up to 10 s for the login‐form container to appear
    #     try:
    #         WebDriverWait(self.driver, 10).until(
    #             EC.visibility_of_element_located((By.XPATH, LoginLocators.FORM))
    #         )
    #     except TimeoutException:
    #         raise AssertionError(
    #             "Tapped LOGIN / SIGN UP, but the login form never appeared."
    #         )
    #
    #     # 3) Wrap that form in a LoginPage POM
    #     login_page = LoginPage(self.driver)
    #
    #     if flow.lower() == "provider":
    #         # 4a) Auto‐login as provider
    #         login_page.login(os.getenv("TEST_EMAIL"), os.getenv("TEST_PASSWORD"))
    #
    #         # 5a) Now wait for the ProviderHomePage header to appear (up to 10 s).
    #         WebDriverWait(self.driver, 10).until(
    #             EC.visibility_of_element_located((By.XPATH, ProviderHomepageLocators.HEADER))
    #         )
    #         return ProviderHomePage(self.driver)
    #
    #     # 4b) flow == "consumer": return the LoginPage so tests can fill it
    #     return login_page
    #
    # # ────────────────────────────────────────────────────────────────────────────────
