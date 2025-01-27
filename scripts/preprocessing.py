#!/usr/bin/env python3
import os
import subprocess

# Path to the GTF file
gtf_file = "~/tesi/Dati/t2t/hs1.ncbiRefSeq.gtf.gz"
output_file = "~/tesi/Dati/t2t/genes_lines.txt"

# Expand the ~ to the full path
gtf_file = os.path.expanduser(gtf_file)
output_file = os.path.expanduser(output_file)

# Function to process a chromosome and append the count to the output file
def process_chromosome(chromosome):
    # Build the command 
    cmd = f"""gunzip -c {gtf_file} |awk '$1 == "chr{chromosome}" && $3 == "transcript"' | cut -f 9 | sed 's/; /\t/g; s/;$//' | cut -f 3 | sed 's/gene_name "\(.*\)"/\\1/' | uniq | wc -l"""
    
    # Execute the command
    count = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    
    # Append the result to the output file
    with open(output_file, 'a') as f:
        f.write(f"chr{chromosome} {count}\n")

# Clear the output file before writing
with open(output_file, 'w') as f:
    f.write("")

# Loop through chromosomes
for i in range(1, 23):  # For chromosomes 1 to 22
    process_chromosome(i)

# Optional: Add the X and Y chromosomes
process_chromosome("X")
process_chromosome("Y")