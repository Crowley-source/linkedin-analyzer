"""
scraper.py — Optional LinkedIn Profile Scraper
================================================
This module is intentionally separated from the main analysis pipeline.

⚠️  IMPORTANT DISCLAIMER
LinkedIn's Terms of Service prohibit automated scraping of their platform.
This code is provided for EDUCATIONAL PURPOSES ONLY to demonstrate
Selenium-based data collection techniques.

For production recruiting use, consider:
  - LinkedIn Talent Solutions API (official)
  - LinkedIn Recruiter (official product)
  - Authorized third-party data providers

Usage (if you choose to use it):
    from scraper import LinkedInScraper
    scraper = LinkedInScraper(email="your@email.com", password="yourpass")
    scraper.login()
    df = scraper.scrape_profiles(["username1", "username2"])
    df.to_csv("data/profiles_raw.csv", index=False)
"""

import time
import random
import pandas as pd

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class LinkedInScraper:
    """
    Scrapes public LinkedIn profile data using Selenium.
    See module docstring for important usage notes.
    """

    LOGIN_URL    = "https://www.linkedin.com/login"
    PROFILE_BASE = "https://www.linkedin.com/in/"

    def __init__(self, email: str, password: str, headless: bool = True):
        if not SELENIUM_AVAILABLE:
            raise ImportError(
                "Selenium not installed. Run: pip install selenium webdriver-manager"
            )
        self.email    = email
        self.password = password
        self.driver   = self._init_driver(headless)

    def _init_driver(self, headless: bool):
        opts = Options()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        return webdriver.Chrome(options=opts)

    def login(self):
        self.driver.get(self.LOGIN_URL)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(self.email)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)
        print("✓ Logged in")

    def scrape_profile(self, username: str) -> dict:
        url = f"{self.PROFILE_BASE}{username}/"
        self.driver.get(url)
        time.sleep(random.uniform(2.5, 4.5))  # polite delay

        profile = {"username": username, "url": url}

        try:
            profile["name"] = self.driver.find_element(
                By.CSS_SELECTOR, "h1.text-heading-xlarge"
            ).text.strip()
        except Exception:
            profile["name"] = username

        try:
            profile["headline"] = self.driver.find_element(
                By.CSS_SELECTOR, "div.text-body-medium"
            ).text.strip()
        except Exception:
            profile["headline"] = ""

        try:
            profile["about"] = self.driver.find_element(
                By.CSS_SELECTOR, "div#about ~ div .visually-hidden"
            ).text.strip()
        except Exception:
            profile["about"] = ""

        try:
            skills_els      = self.driver.find_elements(
                By.CSS_SELECTOR, "span.mr1.t-bold span[aria-hidden='true']"
            )
            profile["skills"] = ", ".join(s.text for s in skills_els[:20])
        except Exception:
            profile["skills"] = ""

        try:
            exp_els             = self.driver.find_elements(
                By.CSS_SELECTOR, "span.mr1.t-bold span[aria-hidden='true']"
            )
            profile["experience"] = " ".join(e.text for e in exp_els[:10])
        except Exception:
            profile["experience"] = ""

        return profile

    def scrape_profiles(self, usernames: list) -> pd.DataFrame:
        profiles = []
        for i, username in enumerate(usernames, 1):
            print(f"  Scraping {i}/{len(usernames)}: {username}")
            try:
                profiles.append(self.scrape_profile(username))
            except Exception as e:
                print(f"  ✗ Failed {username}: {e}")
        self.driver.quit()
        return pd.DataFrame(profiles)
