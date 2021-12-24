<a href="https://kaio6fellipe.github.io/"><img src="./images/back-home.png" alt="Home Page" width="50" height="58" style="filter: grayscale(100%)"></a> 

# Information
> How about performing the inicial enumeration process of an ssh service using only 2 lines and receiving a dictionary with lots of information?
>
> Every time that I had to enumerate an ssh service in [Hack The Box](https://www.hackthebox.com/), I aways had to follow a certain sequence of steps. After a while, laziness won and I decided to use Python to automate this process.
>
> In this repository I use my [another repository](https://kaio6fellipe.github.io/nmap-python/) to make some custom scans with nmap, so, if you wanna use it, remember to configure my [nmap-python](https://kaio6fellipe.github.io/nmap-python/) functions too, I will explain it later.

# Configuration

Install [ssh-audit](https://github.com/jtesta/ssh-audit):
```shell
pip install ssh-audit
```

By default, Windows and Linux ahve ssh-keyscan preinstalled, to make sure, execute this line:
```shell
ssh-keyscan
```
Expected output:
```console
C:\Users\KAIO>ssh-keyscan                                                                                               usage: ssh-keyscan [-46cDHv] [-f file] [-p port] [-T timeout] [-t type]                                                                    [host | addrlist namelist] 
```

At the end, configure my [nmap-python repository](https://kaio6fellipe.github.io/nmap-python/), put the nmap folder inside the ssh-enum folder, if everything goes right, your folders will be organized that way:

![folders](./images/folders.png)

# Details

The ssh_enumeration.py file contains one class:
- iniEnumSSH

    This class contains the methods:
    - ssh_audit
      - This method will open a subprocess to execute this line: ```ssh-audit (host) -p(port)```
      - After that, the generated output will be validated and formated to be included in a dict
    - ssh_keyscan
      - This method will open a subprocess to execute this line : ```ssh-keyscan -t rsa (host) -p (port)```
      - After that, the generated output will be validated and formated to be included in a dict
    - ssh_nmap
      - This method will execute the function nmapCustomScanProcess present in the nmap-python module using the following parameters:
        - ```-sC -sV```
        - ```--script ssh2-enum-algos```
        - ```--script ssh-hostkey --script-args ssh_hostkey=full```
        - ```--script ssh-auth-methods --script-args="ssh.user=root```
    - start
      - This method will execute all the other methods
    - get_dict
      - Return of the result dict

# Example (In progress)

I usually use this class like that:

```python
import ssh_enumeration

# Setting the target and the port
host = '10.0.0.248'
port = 22

# Instantiating the object
enumeration = ssh_enumeration.iniEnumSSH(host, port)
# Executing the start() method
enumeration.start()

# Getting the result dict
dict = enumeration.get_dict()
print(dict)
```
This example will generete the following output after the scan that I did on the metasploitable machine:
```json
{
    "a-beautiful-dict" : "right here"
}
```