#!/usr/bin/env python
# Aim: print html
# Written by: Nanzhen   nanzhen.qiao@gmail.com

import requests, time, csv
from bs4 import BeautifulSoup
from selenium import webdriver

# Launch a Chrome browser using Selenium
driver = webdriver.Chrome("/Users/nanzhen/Documents/GitHub/NCBI_genome_download_GUI/chromedriver")

# Navigate to the URL with dynamic content
url = 'https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/287844' 
driver.get(url) 

# Wait for the dynamic content to load
time.sleep(1)

# Parse the HTML content using after dynamic content has loaded
html_content = driver.page_source

# Close the browser
driver.quit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
pretty_html = soup.prettify() # make it more readable

# Write the HTML content to a text file
with open('html.txt', 'w') as f:
    f.write(pretty_html)