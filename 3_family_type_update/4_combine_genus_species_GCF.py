#!/usr/bin/env python
# Aim: obtain the latest genera, species, and reference genome info of the family Lactobacillaceae from NCBI
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

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

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
# print(genus_data)

# write the genus data to a csv file
with open('genus_data.csv', mode='w', newline='') as csv_file:
    fieldnames = ['genus_name', 'tax_id', 'genus_url']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for genus in genus_data:
        writer.writerow({'genus_name': genus[0], 'tax_id': genus[1], 'genus_url': genus[2]})

for genus in genus_data:
    genus_name = genus[0]
    genus_url = genus[2]

    driver.get(genus_url) 

    # Wait for the dynamic content to load
    time.sleep(1)

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
    species_file_name = f'{genus_name}_species_data.csv'
    with open(species_file_name, mode='w', newline='') as csv_file:
        fieldnames = ['species_name', 'tax_id', 'species_url']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for species in species_data:
            writer.writerow({'species_name': species[0], 'tax_id': species[1], 'species_url': species[2]})
    