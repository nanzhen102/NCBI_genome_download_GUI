#!/usr/bin/env python
# Aim: Obtain the latest genera and species info of the family Lactobacillaceae from NCBI
# Written by: Nanzhen   nanzhen.qiao@gmail.com

import requests, time, csv
from bs4 import BeautifulSoup
from selenium import webdriver

def fetch_taxonomy_data(url, label):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome("/Users/nanzhen/Documents/GitHub/NCBI_genome_download_GUI/chromedriver", options=chrome_options)
    driver.get(url)
    time.sleep(2)
    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', {'aria-label': label})

    data = []
    for link in links:
        name = link.get('data-ga-label')
        tax_id = link.find('span', {'data-tax-id': True}).get('data-tax-id')
        url = f'https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/tree/?taxon={tax_id}'
        data.append((name, tax_id, url))
    
    return data

def write_csv(data, filename, fieldnames):
    with open(filename, mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # writer.writeheader()
        for item in data:
            writer.writerow({fieldnames[0]: item[0], fieldnames[1]: item[1], fieldnames[2]: item[2]})

# Obtain genera info
family_url = 'https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/tree/?taxon=33958' # Lactobacillaceae, txid 33958
genus_data = fetch_taxonomy_data(family_url, 'genus')

write_csv(genus_data, 'genus_data.csv', ['genus_name', 'tax_id', 'genus_url'])

# Create the species_info.csv file with headers
with open('species_info.csv', mode='w', newline='') as species_csv:
    species_fieldnames = ['species_name', 'tax_id', 'species_url']
    species_writer = csv.DictWriter(species_csv, fieldnames=species_fieldnames)
    species_writer.writeheader()

# Obtain species info for each genus
for genus in genus_data:
    genus_url = genus[2]
    species_data = fetch_taxonomy_data(genus_url, 'species')
    genus_name = genus[0].replace(' ', '_')
    # write_csv(species_data, f'{genus_name}_species_data.csv', ['species_name', 'tax_id', 'species_url'])
    write_csv(species_data, 'species_info.csv', ['species_name', 'tax_id', 'species_url'])