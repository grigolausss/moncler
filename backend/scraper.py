import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_chromedriver_path_workaround():
    """
    Workaround for webdriver-manager issues. It finds the correct executable
    and ensures it has the correct permissions.
    """
    print("Locating chromedriver with workaround...")
    try:
        incorrect_path = ChromeDriverManager().install()
        driver_dir = os.path.dirname(incorrect_path)
        correct_path = os.path.join(driver_dir, "chromedriver")

        if not os.path.exists(correct_path):
            raise FileNotFoundError(f"Could not find 'chromedriver' at '{correct_path}'")

        # --- FIX: Ensure the driver is executable ---
        if not os.access(correct_path, os.X_OK):
            print(f"'{correct_path}' is not executable. Setting permissions...")
            os.chmod(correct_path, 0o755) # Set rwxr-xr-x permissions

        print(f"Correct and executable chromedriver path found: {correct_path}")
        return correct_path
    except Exception as e:
        print(f"Error during chromedriver path workaround: {e}")
        raise

def scrape_moncler_page(url):
    """
    Scraper that uses a headless browser to access a Moncler page.
    Includes a workaround for a webdriver-manager bug and permission issues.
    """
    print("Setting up headless Chrome browser...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = None
    try:
        driver_path = get_chromedriver_path_workaround()
        service = ChromeService(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print(f"Navigating to {url}...")
        driver.get(url)
        print("Successfully navigated to the page.")
        print(f"Page title: {driver.title}")

        # Wait for a potential cookie banner and accept it
        try:
            print("Looking for cookie consent button...")
            wait = WebDriverWait(driver, 10)
            cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            cookie_button.click()
            print("Clicked the cookie consent button.")
            time.sleep(2) # Wait for banner to disappear
        except Exception:
            print("Cookie consent button not found or not clickable.")

        # Save the page source to a file for inspection
        page_source_path = "/tmp/moncler_page_source.html"
        with open(page_source_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"Saved page source to {page_source_path}")

    except Exception as e:
        print(f"An error occurred during scraping: {e}")
    finally:
        if driver:
            print("Closing the browser.")
            driver.quit()

if __name__ == '__main__':
    test_url = "https://www.moncler.com/en-it/women/outerwear/short-down-jackets"
    scrape_moncler_page(test_url)
