#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#通过爬取NCBI，提交基因组Accession number获取基因组的ftp site，便于后续批量下载基因组
"""
Created on Mon Apr 20 10:28:25 2020
@author: 李阳杰
"""
# 这个文件是针对Michael给的excel文件的，里面提供了AC Num，手动到成tab文件，然后执行此脚本。然后再for循环，下载

import os # 师兄个人习惯，但是这里并没有用到此模块
import urllib.request # 这里就是我和师兄电脑不一样的地方，我需要 .request
from bs4 import BeautifulSoup
import csv

mainurl ="https://www.ncbi.nlm.nih.gov"
baseurl = "https://www.ncbi.nlm.nih.gov/nuccore/"  #到nucleotide搜索界面。统一定义基本的网页，方便后面解析和保存对基本网页进行修改

in_file="ACC.tab"  #输入文件
savePath = 'ACC_ftp_sites_out.csv' #输出文件名
def main(): #主函数
    ACC_list=readAcc_list(in_file)
    out_lines = []
    for ACC in ACC_list:
        print(ACC)
        if ACC=='':
            out_lines.append(['',''])
        else:
            try:
                ftp_site = get_ftp_site(ACC)
                out_lines.append([ACC,ftp_site])
            except:
                # print('not ok')
                out_lines.append([ACC,''])
    
    saveData(out_lines,savePath)

def askURL(url):
    head = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:74.0) Gecko/20100101 Firefox/74.0"
        }
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        reponse = urllib.request.urlopen(request)
        html= reponse.read().decode("utf-8")
        #print(html) #测试
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

def get_ftp_site(ACC):
    url = baseurl+ACC # baseurl = "https://www.ncbi.nlm.nih.gov/nuccore/，到达Nucleotide的特定ACC number搜索界面
    html=askURL(url)
    soup= BeautifulSoup(html,"html.parser")
    a = soup.find_all('a',text='Assembly')[0] #点击右侧工具栏中的assembly，跳转
    assembly_url=mainurl+a.attrs['href']
       
    ###
    html2 =askURL(assembly_url)
    soup = BeautifulSoup(html2,"html.parser")
    p = soup.find_all('p',class_="title")[0] #在跳转的assembly界面，点击title，跳转
    a = p.contents[0]
    assembly_url2 = mainurl+a.attrs['href']
    
    ### 所以这里也还是下载了assembly的数据
    html3 = askURL(assembly_url2)
    soup = BeautifulSoup(html3,"html.parser") #已经跳转到Assembly的有GCA编号的界面，开始下载文件
    a = soup.find_all("a",text='FTP directory for GenBank assembly')[0] 
    #这里是师兄手动，在NCBI上一个一个链接点击进去，最后发现是这一个链接里下载genome最方便，属于个人经验。（使用网页，右键，检查）
    ftp_site = a.attrs['href']
    return ftp_site

def readAcc_list(file_name):
    f = open(file_name,'r')
    headline = f.readline() 
    #这里貌似，是不读取tab文件的首行，因此，需要自己加一个空行，或者把这个删除
    Acc_list = [l.strip() for l in f]
    return Acc_list

def saveData(out_lines,savePath):
    out = open(savePath,'w',newline='')
    out_csv = csv.writer(out)
    out_csv.writerows(out_lines)
    out.close()    
    
if __name__ == '__main__':
	main()