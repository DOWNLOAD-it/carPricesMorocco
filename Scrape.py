import csv
import time
import numpy as np
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)


# Configure Edge WebDriver (headless mode)
service = Service(log_path="NUL")  # Windows
options = Options()
options.add_argument("--headless=new")  # Faster headless mode
options.add_argument("--log-level=3")  # Suppress logs
driver = webdriver.Edge(service=service, options=options)

# Headers for requests
HEADERS = {"User-Agent": "Mozilla/5.0"}


# Helper function to extract text safely
def extract_text(soup, selector, index=0):
    elements = soup.select(selector)
    return elements[index].text.strip() if elements and len(elements) > index else "NaN"


# Function to get listing links using Selenium
def get_listing_links():
    """Retrieve all listing links on a results page."""
    links = []
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-1jge648-0.jZXrfL"))
        )
        elements = driver.find_elements(By.CLASS_NAME, "sc-1jge648-0.jZXrfL")
        links = [
            el.get_attribute("href") for el in elements if el.get_attribute("href")
        ]
    except (NoSuchElementException, TimeoutException):
        print("No links found on this page.")
    return links


def scrape_page(url):
    """Scrape data from an individual listing page with NaN fallback for all fields."""
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"⚠️ Skipping {url}, status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Updated version of safe_extract to return NaN when an element is not found
    def safe_extract(soup, selector, index=0):
        elements = soup.select(selector)
        return (
            elements[index].text.strip()
            if elements and len(elements) > index
            else np.nan
        )

    # Extract data from the soup, replacing missing values with NaN if not found
    data = [
        safe_extract(soup, "h1"),  # Title
        safe_extract(soup, ".sc-1x0vz2r-0.kQHNss", 0),  # Year
        safe_extract(soup, ".sc-1x0vz2r-0.kQHNss", 1),  # Transmission
        safe_extract(soup, ".sc-1x0vz2r-0.kQHNss", 2),  # Fuel
        safe_extract(soup, ".sc-1x0vz2r-0.gSLYtF", 0),  # Car Type
        safe_extract(soup, ".sc-1x0vz2r-0.gSLYtF", 1),  # Secteur
        safe_extract(soup, ".sc-1x0vz2r-0.gSLYtF", 2),  # Kilometrage
        safe_extract(soup, ".sc-1x0vz2r-0.gSLYtF", 3),  # Marque
        safe_extract(soup, ".sc-1x0vz2r-0.gSLYtF", 4),  # Model
        safe_extract(soup, ".sc-1x0vz2r-0.gSLYtF", 5),  # Nombre de Portes
        safe_extract(soup, ".sc-1x0vz2r-0.gSLYtF", 6),  # Origine
        safe_extract(soup, ".sc-1x0vz2r-0.gSLYtF", 7),  # Premiere Main
        safe_extract(soup, ".sc-1x0vz2r-0.gSLYtF", 8),  # Puissance Fiscale
        safe_extract(soup, ".sc-1x0vz2r-0.gSLYtF", 9),  # État
    ]

    # Special handling for price (cleanup + NaN fallback)
    try:
        price = safe_extract(soup, ".sc-1x0vz2r-0.lnEFFR")
        price = (
            price.replace(" ", "").replace(" ", "").replace("DH", "")
            if price != "NaN"
            else "NaN"
        )
        data.append(price)
    except Exception:
        data.append("NaN")

    print(f"Scraped: {data[0]} -----> done")
    return data


# Start scraping process
driver.get("https://www.avito.ma/fr/maroc/voitures_d_occasion-%C3%A0_vendre")
all_data = []

for page in range(2):  # Change range to scrape multiple pages
    try:
        links = get_listing_links()

        # Scrape each link using BeautifulSoup
        for link in links:
            data = scrape_page(link)
            if data:
                all_data.append(data)

        # 🛑 Hide the ad (iframe)
        try:
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.execute_script("arguments[0].style.display = 'none';", iframe)
            print("✅ Publicité masquée")
        except NoSuchElementException:
            print("✅ Aucune publicité détectée")

        # ✅ Click the "Next" button normally
        try:
            # Locate the last "Next" button by selecting the last occurrence of the "Next" button with your classes
            next_button = driver.find_element(
                By.XPATH,
                "(//a[contains(@class, 'sc-2y0ggl-1') and contains(@class, 'yRCEb')])[last()]",
            )

            # Click it
            next_button.click()
            print("✅ Clicked Next Page")
        except (NoSuchElementException, TimeoutException):
            print("❌ Next button not found or not clickable")

        time.sleep(1)  # Small delay before next iteration

        print(f"Page {page + 1} completed")

    except (NoSuchElementException, TimeoutException):
        print("End of pagination or error encountered.")
        break

# Save results to CSV
with open("avito_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "Title",
            "Year",
            "Transmission",
            "Fuel",
            "Type",
            "Secteur",
            "Kilometrage",
            "Marque",
            "Model",
            "Nombre de Portes",
            "Origine",
            "Première Main",
            "Puissance Fiscale",
            "État",
            "Price",
        ]
    )
    writer.writerows(all_data)

print(f"✅ Scraped {len(all_data)} listings. Data saved to avito_data.csv")
driver.quit()
