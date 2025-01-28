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
    output_dir = os.path.expanduser(f"~/tesi/Dati/t2t/annotation_pc/chr_{chromosome}")
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    
    # Build the output file path
    output_file = os.path.join(output_dir, f"chr{chromosome}_genes.txt")
    
    # Build the command
    cmd = f"""gunzip -c {gtf_file} | awk '$1 == "chr{chromosome}" && $3 == "exon"' | grep 'transcript_id "NM_' |sort -k4,4V """ 
    
    # Execute the command
    count = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    
    # Save the result in the chromosome's folder
    with open(output_file, 'w') as f:
        f.write(f"{count}\n")

# Loop through chromosomes
for i in range(1, 23):  # For chromosomes 1 to 22
    process_chromosome(i)

# Optional: Add the X and Y chromosomes
process_chromosome("X")
process_chromosome("Y")
