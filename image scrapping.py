import os
import time
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains


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
# Loop through each additional "Trending Now" link
for url in additional_trending_urls:

    # Open each link in a new tab
    driver.execute_script("window.open(arguments[0]);", url)
    driver.switch_to.window(driver.window_handles[-1])

    # Give the new page some time to load
    time.sleep(5)

    # Find all image elements on the page
    image_elements = driver.find_elements(By.XPATH, "//img[@src]")

    # Folder to save images
    image_folder = "hm_images" + "/" + str(i)
    os.makedirs(image_folder, exist_ok=True)

    # Download each image
    for index, img in enumerate(image_elements):
        # Check if image is fully loaded
        if img.size["height"] > 0:
            img_url = img.get_attribute("src")
            if img_url:
                # Download image using requests
                response = requests.get(img_url)
                if response.status_code == 200:
                    # Save image to the folder
                    img_name = f"{image_folder}/image_{index}.jpg"
                    with open(img_name, "wb") as f:
                        f.write(response.content)
                    print(f"Image {index} downloaded successfully to {image_folder}")
                else:
                    print(
                        f"Failed to download image {index}. Status code: {response.status_code}"
                    )

    i = i + 1


print(f"All images have been downloaded to the folder")


# Close the WebDriver
driver.quit()
