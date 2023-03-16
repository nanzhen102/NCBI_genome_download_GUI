import requests, time, csv, re
from bs4 import BeautifulSoup
from selenium import webdriver

def get_gcf_id(species_url):
    # Launch a Chrome browser using Selenium
    driver = webdriver.Chrome("/Users/nanzhen/Documents/GitHub/NCBI_genome_download_GUI/chromedriver")

    # Navigate to the URL with dynamic content
    driver.get(species_url)

    # Wait for the dynamic content to load
    time.sleep(1)

    # Parse the HTML content using after dynamic content has loaded
    html_content = driver.page_source

    # Close the browser
    driver.quit()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find if there is a Reference genome. If so, extract GCF
    GCF_id = soup.find('a', {'class': 'MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineHover css-41ei74', 'href': True})

    # GCF_id['data-ga-label'] is reference genome.
    if GCF_id: 
        href = GCF_id['href']
        match = re.search(r'/genome/(.*?)/', href)
        if match:
            genome_id = match.group(1)
            return genome_id
        else:
            return "GCF_id not found"
    else:
        return "Reference genome not found"

# Read genus_data.csv and extract species_url
with open('species_info_exp.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        species_url = row['species_url']
        # the url need to be edited here !!!!
        species_url_edited = species_url.replace("taxonomy/tree/?taxon=", "taxonomy/")
        gcf_id = get_gcf_id(species_url_edited)
        print(f"Species URL: {species_url} | GCF_id: {gcf_id}")
