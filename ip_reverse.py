import time
import requests
from bs4 import BeautifulSoup
import re


ip_reverse_result = open("ip_reverse_result.txt", "w")

def search_ip(url):
    pattern = re.compile(r'[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}')
    ip = pattern.findall(url)
    try:
        return ip[0]
    except:
        return ""

def get_ip_reverse():
    f = open("vul_url.txt","r")
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        line_ls = line.split(" ")
        url = line_ls[0]
        ip = search_ip(url)
        if ip != "":
            aizhan_reverse(ip)
    ip_reverse_result.close()

def aizhan_reverse(ip):
    result = ip + " =>"
    url = "https://dns.aizhan.com/" + ip + "/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'
    }
    try:
        # print(url)
        r = requests.get(url=url, headers=headers, timeout=3)
        soup = BeautifulSoup(r.content,"html.parser")
        # print(soup)
        td = soup.find_all(name="td", attrs={"class" :"domain"})
        for i in td[1:len(td)-1]:
            a = i.a
            result += " " + str(a['href'])
        print(result)
        ip_reverse_result.write(result+"\n")
        time.sleep(2)
    except Exception as e:
        print(e)
        print(ip+" 发生错误")


if __name__ == "__main__":
    get_ip_reverse()