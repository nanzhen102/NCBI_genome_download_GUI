#!/usr/bin/env python
# Aim: obtain the latest info about Lactobacillaceae from NCBI
# Written by: Nanzhen   nanzhen.qiao@gmail.com

import requests
from bs4 import BeautifulSoup

url = 'https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/tree/?taxon=33958'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

# inspect the HTML straucture of the web, find the HTML tags to search for
# a `<a>' tag with 'class="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineHover css-1g2ra9k"'
genus_name = soup.find('a', {'class': 'MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineHover css-1g2ra9k'})

print(genus_name)