#!/usr/bin/env python
# Aim: obtain the latest info of the reference genome of each species of the family Lactobacillaceae from NCBI
# Written by: Nanzhen   nanzhen.qiao@gmail.com

#!/usr/bin/env python
# Aim: obtain the latest species info of the family Lactobacillaceae from NCBI
# Written by: Nanzhen   nanzhen.qiao@gmail.com

import requests, time, csv, re
from bs4 import BeautifulSoup
from selenium import webdriver

# Launch a Chrome browser using Selenium
driver = webdriver.Chrome("/Users/nanzhen/Documents/GitHub/NCBI_genome_download_GUI/chromedriver")

# Navigate to the URL with dynamic content
species_url = 'https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/287844' 
driver.get(species_url) 

# Wait for the dynamic content to load
time.sleep(1)

# Parse the HTML content using after dynamic content has loaded
html_content = driver.page_source

# Close the browser
driver.quit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find if there is a Refrence genome. If so, extract GCF
GCF_id = soup.find('a', {'class': 'MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineHover css-41ei74', 'href': True})

# GCF_id['data-ga-label'] is reference genome.
if GCF_id: 
    href = GCF_id['href']
    match = re.search(r'/genome/(.*?)/', href)
    if match:
        genome_id = match.group(1)
        # ask Eden how to extract strain_info
        # strain_info = GCF_id.find_next_sibling('p').text.strip()
       #  print(genome_id, strain_info)
        print(genome_id)
    else:
        print("GCF_id not found")
else:
    print("Reference genome not found")

