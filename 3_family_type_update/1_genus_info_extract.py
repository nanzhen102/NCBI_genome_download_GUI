#!/usr/bin/env python
# Aim: obtain the latest genera info of the family Lactobacillaceae from NCBI
# Written by: Nanzhen   nanzhen.qiao@gmail.com

import requests, time, csv
from bs4 import BeautifulSoup
from selenium import webdriver

# Launch a Chrome browser using Selenium
driver = webdriver.Chrome("/Users/nanzhen/Documents/GitHub/NCBI_genome_download_GUI/chromedriver")

# Navigate to the URL with dynamic content
family_url = 'https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/tree/?taxon=33958' # Lactobacillaceae, txid 33958
driver.get(family_url) 

# Wait for the dynamic content to load
time.sleep(10)

# Parse the HTML content using after dynamic content has loaded
html_content = driver.page_source

# Close the browser
driver.quit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
pretty_html = soup.prettify() # make it more readable

# Find all <a> elements with aria-label="genus"
genus_links = soup.find_all('a', {'aria-label': 'genus'})

# Extract the data-ga-label and href attributes of each link
genus_data = []
for genus in genus_links:
    genus_name = genus.get('data-ga-label')
    tax_id = genus.find('span', {'data-tax-id': True}).get('data-tax-id')
    genus_url = f'https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/tree/?taxon={tax_id}'
    # print(genus_name, tax_id)
    genus_data.append((genus_name, tax_id, genus_url))
print(genus_data)

# write the data to a csv file
with open('genus_data.csv', mode='w', newline='') as csv_file:
    fieldnames = ['genus_name', 'tax_id', 'genus_url']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for genus in genus_data:
        writer.writerow({'genus_name': genus[0], 'tax_id': genus[1], 'genus_url': genus[2]})

# Write the HTML content to a text file
# with open('html_2.txt', 'w') as f:
#     f.write(pretty_html)