#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, csv, re
import urllib.request
from bs4 import BeautifulSoup

# Define main NCBI URL and base URL for nucleotide search
mainurl = "https://www.ncbi.nlm.nih.gov"
baseurl = "https://www.ncbi.nlm.nih.gov/nuccore/"

in_file = "/Users/nanzhen/Documents/GitHub/NCBI_genome_download_GUI/2_ACC_download/ACC.tab"
savePath = '/Users/nanzhen/Documents/GitHub/NCBI_genome_download_GUI/2_ACC_download/ACC_ftp_sites_out.csv'

def main():
    # Read ACC numbers from input file
    ACC_list = readAcc_list(in_file)
    out_lines = []

    # Loop through ACC numbers to retrieve FTP sites
    for ACC in ACC_list:
        print(ACC)
        if ACC == '':
            out_lines.append(['', ''])
        else:
            try:
                ftp_site = get_ftp_site(ACC)
                out_lines.append([ACC, ftp_site])
            except:
                out_lines.append([ACC, ''])
    # Save ACC numbers and FTP sites to a CSV file
    saveData(out_lines, savePath)

    # Download genomic files using the FTP links from the CSV file
    with open(savePath, 'r') as input_file:
        for line in input_file:
            line = line.strip()
            if line == '':
                continue
            ftp = line.split(',')[-1]
            strain_name = line.split(',')[0]
            l = ftp.split('/')[-1]
            ftp_id = ftp + '/' + l + '_genomic.fna.gz'
            os.system('wget %s -O %s.fna.gz' % (ftp_id, strain_name))

# Function to send a request to a URL and return the HTML content
def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:74.0) Gecko/20100101 Firefox/74.0"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

# Function to retrieve the FTP site for a given ACC number
def get_ftp_site(ACC):
    url = baseurl + ACC
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    a = soup.find_all('a', text='Assembly')[0]
    assembly_url = mainurl + a.attrs['href']

    html2 = askURL(assembly_url)
    soup = BeautifulSoup(html2, "html.parser")
    p = soup.find_all('p', class_="title")[0]
    a = p.contents[0]
    assembly_url2 = mainurl + a.attrs['href']

    html3 = askURL(assembly_url2)
    soup = BeautifulSoup(html3, "html.parser")
    a = soup.find_all("a", text='FTP directory for GenBank assembly')[0]
    ftp_site = a.attrs['href']
    return ftp_site

# Function to read ACC numbers from the input file
def readAcc_list(file_name):
    with open(file_name, 'r') as f:
        headline = f.readline()
        Acc_list = [l.strip() for l in f]
    return Acc_list

# Function to save the ACC numbers and FTP sites to a CSV file
def saveData(out_lines, savePath):
    with open(savePath, 'w', newline='') as out:
        out_csv = csv.writer(out)
        out_csv.writerows(out_lines)

if __name__ == '__main__':
    main()
