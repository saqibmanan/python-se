# pages/home_page.py

import os
from dotenv import load_dotenv
from typing import Union
from selenium.common.exceptions import ElementClickInterceptedException
import json
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

    from selenium.common.exceptions import ElementClickInterceptedException
    import json

    def go_to_all_data_page(self):
        # … all your waits/scrolling/maximize as before …

        elem = self.driver.find_element(By.XPATH, HomepageLocators.TAB_DATASETS)
        try:
            elem.click()
        except ElementClickInterceptedException as e:
            # 1) Log the exception message
            print("⚠️ Click intercepted:", e.msg)

            # 2) Dump a screenshot so you can visually inspect
            path = "debug_blocker.png"
            self.driver.save_screenshot(path)
            print(f"📸 Saved screenshot to {path}")

            # 3) Dump page source to a file
            html = self.driver.page_source
            with open("debug_blocker.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("📄 Written page source snapshot to debug_blocker.html")

            # 4) Find exactly which element is on top at the click point
            box = elem.location
            size = elem.size
            center_x = box["x"] + size["width"] / 2
            center_y = box["y"] + size["height"] / 2
            blocker = self.driver.execute_script(
                "return document.elementFromPoint(arguments[0], arguments[1]).outerHTML;",
                center_x,
                center_y
            )
            print("🚧 Blocking element HTML:", blocker)

            # re-raise so your test still fails if you want—but now with diagnostics
            raise

        return DatasetPage(self.driver)

