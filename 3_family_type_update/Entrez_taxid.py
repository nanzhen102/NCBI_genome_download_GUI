# Aim: Retrieve the taxonomy information for Apilactobacillus

from Bio import Entrez

# Provide your email address to NCBI
Entrez.email = "nanzhen.qiao@gmail.com"

# Retrieve the taxonomy information for Apilactobacillus
tax_id = "33958" # Apilactobacillus 2767877; Lactobacillaceae 33958
handle = Entrez.efetch(db="taxonomy", id=tax_id, retmode="xml")
record = Entrez.read(handle)[0]

# Print the taxonomy information
print(f"Taxonomy information for {record['ScientificName']}:")
for line in record["LineageEx"]:
    print(f"{line['Rank']}: {line['ScientificName']} [{line['TaxId']}]")
