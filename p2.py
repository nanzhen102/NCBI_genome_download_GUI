import subprocess

# process = subprocess.Popen("ncbi-genome-download", "--genera Fructilactobacillus" "--formats fasta", "--parallel 4", "--dry-run")

output_folder = "/Users/nanzhen"

cmd = ["ncbi-genome-download", "--genera", "Fructilactobacillus", "--formats", "fasta", "--parallel", "4", "--output-folder", output_folder, "bacteria"]

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

stdout, stderr = process.communicate()

if process.returncode != 0:
    print(f"An error occurred: {stderr.decode()}")
else:
    print(f"Command executed successfully. Output: {stdout.decode()}")
