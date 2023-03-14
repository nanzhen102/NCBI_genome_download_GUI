from Bio import Entrez

# Set the email address associated with your NCBI account
Entrez.email = "nanzhen.qiao@gmail.com"

# Search for all genera under the family Lactobacillaceae
# search_term = '"Lactobacillaceae"[Family] AND "genus"[Rank]'
search_term = '"Periweissella"[Genus] AND "species"[Rank]'

handle = Entrez.esearch(db="taxonomy", term=search_term, retmax=10000)
record = Entrez.read(handle)

try: 
    # Extract the tax_ids from the search results
    tax_ids = record["IdList"]

    # Print the tax_ids for each genus
    for tax_id in tax_ids:
        handle = Entrez.efetch(db="taxonomy", id=tax_id)
        record = Entrez.read(handle)
        genus_name = record[0]["ScientificName"]
        print(f"{genus_name}: {tax_id}")
        print(f"Search term: {search_term}")
        print(f"Number of tax_ids: {len(tax_ids)}")

except Exception as e:
    print(f"An error occurred: {str(e)}")