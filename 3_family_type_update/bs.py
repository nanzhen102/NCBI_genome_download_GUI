import requests
from bs4 import BeautifulSoup

url = 'https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/tree/?taxon=33958'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

# print(soup.prettify()) # represents the document as a nested data structure


