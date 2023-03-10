import subprocess

process = subprocess.Popen("ncbi-genome-download", "--genera", genus, "--formats", format, "--parallel 4", "--dry-run")
