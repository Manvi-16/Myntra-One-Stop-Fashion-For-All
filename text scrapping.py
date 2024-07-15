import os
import time
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup


# Set up the WebDriver
driver = webdriver.Chrome()

# Open the H&M website
driver.get("https://www2.hm.com/en_in/index.html")

# Give the page some time to load
time.sleep(5)

# Find all "Trending Now" links on the initial page
initial_trending_links = driver.find_elements(
    By.XPATH, '//a[contains(@href, "trending-now")]'
)

# Extract the href attribute from each link
initial_trending_urls = [link.get_attribute("href") for link in initial_trending_links]

# List to hold all additional trending URLs found on visited pages
additional_trending_urls = []

# Folder to save images
image_folder = "trending_images"
os.makedirs(image_folder, exist_ok=True)

# Loop through each initial "Trending Now" link
for url in initial_trending_urls:
    # Open each link in a new tab
    driver.execute_script("window.open(arguments[0]);", url)
    driver.switch_to.window(driver.window_handles[-1])

    # Give the new page some time to load
    time.sleep(5)

    # Find all "Trending Now" links on the current page
    additional_links = driver.find_elements(
        By.XPATH, '//a[contains(@href, "trending")]'
    )

    # Extract the href attribute from each additional link
    for link in additional_links:
        link_url = link.get_attribute("href")
        if link_url not in additional_trending_urls:
            additional_trending_urls.append(link_url)

    # Close the current tab and switch back to the main tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
print(additional_trending_urls)
i = 1
product_titles = []
# Loop through each additional "Trending Now" link
for url in additional_trending_urls:

    # Open each link in a new tab
    driver.execute_script("window.open(arguments[0]);", url)
    driver.switch_to.window(driver.window_handles[-1])

    # Give the new page some time to load
    time.sleep(5)

    # Navigate to the website

    html = driver.page_source

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")

    # Find all product items
    product_items = soup.find_all("li", class_="product-item")

    # List to store product titles

    # Iterate through each product item
    for item in product_items:
        # Find the title element within each product item
        title_element = item.find("a", class_="link")

        # Extract the text from the title element
        title_text = title_element.get_text(strip=True)

        # Append the title text to the list
        product_titles.append(title_text)

    # Print the list of product titles
print("Product Titles:")
"""for title in product_titles:
        print(title)"""

print(product_titles)

# Quit the WebDriver
driver.quit()
