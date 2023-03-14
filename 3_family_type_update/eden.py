import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the URL of the page to be scraped
url = 'https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/tree/?taxon=33958'

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Set up the webdriver
# driver = webdriver.Chrome()
driver = webdriver.Chrome(ChromeDriverManager().install(),)
driver.get(url)

# Wait for the page to load
wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'data-tree')))

# Find the Lactobacillaceae node and open its dropdown
lacto_node = driver.find_element_by_xpath('//div[@class="taxon-name"][text()="Lactobacillaceae"]')
lacto_dropdown_button = lacto_node.find_element_by_xpath('./following-sibling::div/button')
lacto_dropdown_button.click()
time.sleep(1) # Wait for the dropdown to fully open before moving on

# Find all the dropdown buttons below the Lactobacillaceae node and click them
lacto_node_div = lacto_node.find_element_by_xpath('./following-sibling::div[@class="taxon-children"]')
dropdown_buttons = lacto_node_div.find_elements_by_xpath('.//button[@data-toggle="dropdown"]')
for button in dropdown_buttons:
    button.click()
    time.sleep(1) # Wait for the dropdown to fully open before moving on

# Get the HTML source of the page after all dropdowns have been opened
html = driver.page_source

# Close the webdriver
driver.quit()

# Parse the HTML source using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the div containing the tree structure
tree_div = soup.find('div', {'class': 'data-tree'})

# Find all the links within the tree div
links = tree_div.find_all('a')

# Create an empty list to store the links to Lactobacillaceae species/subspecies/strains
lacto_links = []

# Loop through all the links and check if they belong to the Lactobacillaceae family
for link in links:
    # Get the URL of the link
    link_url = link.get('href')

    # Check if the link belongs to the Lactobacillaceae family
    if 'taxonomy/' in link_url and '33958' in link_url:
        # Add the link to the list of Lactobacillaceae links
        lacto_links.append(link_url)

# Create a dataframe to store the links
df = pd.DataFrame({'Lactobacillaceae links': lacto_links})

# Dump the dataframe to a csv file
df.to_csv('lactobacillaceae_links.csv', index=False)