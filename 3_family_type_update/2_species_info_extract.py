#!/usr/bin/env python
# Aim: obtain the latest species info of the family Lactobacillaceae from NCBI
# Written by: Nanzhen   nanzhen.qiao@gmail.com

import requests, time, csv
from bs4 import BeautifulSoup
from selenium import webdriver

# Launch a Chrome browser using Selenium
driver = webdriver.Chrome("/Users/nanzhen/Documents/GitHub/NCBI_genome_download_GUI/chromedriver")

# Navigate to the URL with dynamic content
genus_url = 'https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/tree/?taxon=2767884' 
driver.get(genus_url) 

# Wait for the dynamic content to load
time.sleep(10)

# Parse the HTML content using after dynamic content has loaded
html_content = driver.page_source

# Close the browser
driver.quit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all <a> elements with aria-label="genus"
species_links = soup.find_all('a', {'aria-label': 'species'})

# Extract the data-ga-label and href attributes of each link
species_data = []
for species in species_links:
    species_name = species.get('data-ga-label')
    tax_id = species.find('span', {'data-tax-id': True}).get('data-tax-id')
    species_url = f'https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/{tax_id}'
    # print(genus_name, tax_id)
    species_data.append((species_name, tax_id, species_url))
print(species_data)

# write the data to a csv file
with open('species_data.csv', mode='w', newline='') as csv_file:
    fieldnames = ['species_name', 'tax_id', 'species_url']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for species in species_data:
        writer.writerow({'species_name': species[0], 'tax_id': species[1], 'species_url': species[2]})

# Count the number 