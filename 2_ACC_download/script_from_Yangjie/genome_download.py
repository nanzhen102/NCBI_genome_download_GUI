import os
import re

input_file=open('ACC_ftp_sites_out.csv','r')
for line in input_file:
        line=line.strip()
        if line =='':
                continue
        ftp = line.split(',')[-1]
        strain_name = line.split(',')[0]
        l=ftp.split('/')[-1]
        ftp_id=ftp+'/'+l+'_genomic.fna.gz'
        os.system('wget %s -O %s.fna.gz'%(ftp_id,strain_name))

