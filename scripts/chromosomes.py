#!/usr/bin/env python3
import os
import subprocess

# Paths to the GTF file and gene list directory
gtf_file = "~/tesi/Dati/t2t/hs1.ncbiRefSeq.gtf.gz"
gene_list_dir = "~/tesi/Dati/t2t/gene_list"
output_base_dir = "~/tesi/Dati/t2t/annotations"

# Expand the ~ to the full path
gtf_file = os.path.expanduser(gtf_file)
gene_list_dir = os.path.expanduser(gene_list_dir)
output_base_dir = os.path.expanduser(output_base_dir)

# Function to process a chromosome and create the structure
def process_chromosome(chromosome):
    # Path to the gene list for the chromosome
    gene_list_file = os.path.join(gene_list_dir, f"chromosome_{chromosome}", f"chr{chromosome}_genes.txt")
    
    # Check if the gene list file exists
    if not os.path.exists(gene_list_file):
        print(f"Gene list for chr{chromosome} not found. Skipping.")
        return
    
    # Read the gene list
    with open(gene_list_file, 'r') as gene_list:
        genes = [gene.strip() for gene in gene_list if gene.strip()]  # Remove empty lines and strip whitespace
    
    # Process each gene
    for gene in genes:
        # Create a folder for the gene
        gene_dir = os.path.join(output_base_dir, f"chr_{chromosome}", gene)
        os.makedirs(gene_dir, exist_ok=True)
        
        # Path to the output file for the gene
        gene_output_file = os.path.join(gene_dir, f"{gene}.gtf")
        
        # Build the command to extract lines for the gene
        cmd = f"""gunzip -c {gtf_file} | awk '$1 == "chr{chromosome}" && $3 == "exon"' | grep "{gene}" """
        
        # Execute the command
        try:
            gene_lines = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        except subprocess.CalledProcessError:
            print(f"No lines found for gene {gene} in chr{chromosome}.")
            continue
        
        # Save the extracted lines to the gene's folder
        with open(gene_output_file, 'w') as f:
            f.write(gene_lines)

# Loop through chromosomes
for i in range(1, 23):  # For chromosomes 1 to 22
    process_chromosome(i)

# Optional: Add the X and Y chromosomes
process_chromosome("X")
process_chromosome("Y")
