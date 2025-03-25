#!/usr/bin/env python3
import os
import subprocess

# Path to the GTF file
gtf_file = "~/tesi/Dati/t2t/hs1.ncbiRefSeq.gtf.gz"

# Expand the ~ to the full path
gtf_file = os.path.expanduser(gtf_file)

# Function to process a chromosome and save the results in a separate folder
def process_chromosome(chromosome):
    # Create a folder for the chromosome
    output_dir = os.path.expanduser(f"~/tesi/Dati/t2t/gene_list/chromosome_{chromosome}")
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    
    # Build the output file path
    output_file = os.path.join(output_dir, f"chr{chromosome}_genes.txt")
    
    # Build the command
    cmd = rf"""gunzip -c {gtf_file} | awk '$1 == "chr{chromosome}" && $3 == "exon"' | cut -f 9 | sed 's/; /\t/g; s/;$//' | cut -f 1 | sed 's/gene_id "\(.*\)"/\1/' | uniq | awk 'NF' """
    
    # Execute the command
    count = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    
    # Save the result in the chromosome's folder
    with open(output_file, 'w') as f:
        f.write(count)  # Write the gene list without any prefix or additional formatting

    # Sort the output file
    cmd = f"sort {output_file} -o {output_file}"
    subprocess.run(cmd, shell=True)

# Loop through chromosomes
for i in range(1, 23):  # For chromosomes 1 to 22
    process_chromosome(i)

# Optional: Add the X and Y chromosomes
process_chromosome("X")
process_chromosome("Y")

# Check the number of unique gene_ids found
print(f"Total unique gene_ids found: {len(gene_data)}")

# Check if any gene_id is missing compared to the expected list
expected_genes = set()  # Store expected gene IDs from chr1_genes.txt
chr1_genes_file = os.path.join(base_dir, "chr_1", "chr1_genes.txt")

if os.path.exists(chr1_genes_file):
    with open(chr1_genes_file, "r") as file:
        for line in file:
            match = re.search(r'gene_id "([^"]+)"', line)
            if match:
                expected_genes.add(match.group(1))

missing_genes = expected_genes - set(gene_data.keys())
print(f"Genes expected but not found: {len(missing_genes)}")
print(missing_genes)  # Print missing gene names
