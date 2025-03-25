#!/usr/bin/env python3
import os
import re
from collections import defaultdict

# Base directory containing per-chromosome txt files
base_dir = os.path.expanduser("~/tesi/Dati/t2t/annotation_all")

# Function to extract genes from a chromosome's text file
def process_chromosome(chromosome):
    input_file = os.path.join(base_dir, f"chr_{chromosome}", f"chr{chromosome}_genes.txt")

    # Check if the file exists
    if not os.path.exists(input_file):
        print(f"File {input_file} not found. Skipping.")
        return

    # Dictionary to store gene_id → list of corresponding lines
    gene_data = defaultdict(list)

    # Read the chromosome file
    with open(input_file, "r") as file:
        for line in file:
            fields = line.strip().split("\t")
            if len(fields) < 9:
                continue  # Skip malformed lines
            
            attributes = fields[8]
            
            # Extract the gene_id using regex
            match = re.search(r'gene_id "([^"]+)"', attributes)
            if match:
                gene_id = match.group(1)
                gene_data[gene_id].append(line.strip())

    # Save extracted data
    for gene_id, entries in gene_data.items():
        gene_dir = os.path.join(base_dir, f"chr_{chromosome}", gene_id)
        os.makedirs(gene_dir, exist_ok=True)  # Ensure the folder exists
        
        output_file = os.path.join(gene_dir, f"{gene_id}.gtf")
        with open(output_file, "w") as f:
            f.write("\n".join(entries) + "\n")  # Save all lines for this gene

# Process all chromosomes
for i in range(1, 23):  # Chromosomes 1-22
    process_chromosome(i)

# Process sex chromosomes
process_chromosome("X")
process_chromosome("Y")
