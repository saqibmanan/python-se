# General imports
import tempfile
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
import pytest
from selenium import webdriver

# Imports to get chrome driver working
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Imports to get firefox driver working
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Import options for headless mode
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Send 'chrome' or 'firefox' as parameter for execution"
    )

@pytest.fixture(scope="session")
def driver(request):
    """
    Launch a headless Chrome on GitHub Actions (Ubuntu). We force Chrome to use
    a brand-new, empty user-data directory (in /tmp) on each session so that
    “user data directory already in use” errors never occur.
    """
    browser = request.config.getoption("--browser")
    drv = ""
    # 1) Build ChromeOptions
    opts = Options()

    # Use the new headless mode; on GH runners this avoids some legacy issues.
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-extensions")

    # 2) Create a fresh, empty directory for Chrome's user-data
    tmp_dir = tempfile.mkdtemp(prefix="chrome-user-data-")
    opts.add_argument(f"--user-data-dir={tmp_dir}")

    # 3) Install the matching chromedriver, then start Chrome
    if browser == "chrome":
        drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    elif browser == "firefox":
        drv = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    # Implicit wait setup for our framework
    drv.implicitly_wait(10)
    yield drv

    # 4) Teardown: quit Chrome and remove the temp folder
    try:
        drv.quit()
    except Exception:
        pass
    # Clean up the temp profile directory
    try:
        # shutil.rmtree would remove it recursively
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)
    except Exception:
        pass

@pytest.fixture(scope="session")
def base_url():
    """
    This fixture should return the URL that your HomePage.load() does:
       driver.get(base_url)
    """
    url = os.getenv("URL")  # ← local .env probably sets this
    if not url:
        pytest.skip("BASE_URL is not set")
    return url