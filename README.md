<a href="https://kaio6fellipe.github.io/"><img src="./images/back-home.png" alt="Home Page" width="50" height="58" style="filter: grayscale(100%)"></a> 

# Information
> How about performing the inicial enumeration process of an ssh service using only 2 lines and receiving a dictionary with lots of information?
>
> Every time that I had to enumerate an ssh service in [Hack The Box](https://www.hackthebox.com/), I aways had to follow a certain sequence of steps. After a while, laziness won and I decided to use Python to automate this process.
>
> In this repository I use my [another repository](https://kaio6fellipe.github.io/nmap-python/) to make some custom scans with nmap, so, if you wanna use it, remember to configure my [nmap-python](https://kaio6fellipe.github.io/nmap-python/) functions too, I will explain it later.

# Configuration

Make sure to clone this repo with the following command, this command will clone the [nmap-python submodule](https://kaio6fellipe.github.io/nmap-python/) too:
```shell
git clone --recurse-submodules -j8 https://github.com/kaio6fellipe/ssh-enum.git
```

Install [ssh-audit](https://github.com/jtesta/ssh-audit):
```shell
pip install ssh-audit
```

By default, Windows and Linux have ssh-keyscan preinstalled, to make sure, execute this line:
```shell
ssh-keyscan
```
Expected output:
```console
❯ ssh-keyscan
usage: ssh-keyscan [-46cDHv] [-f file] [-p port] [-T timeout] [-t type]
                   [host | addrlist namelist]
```

At the end, install the dependencies of my [nmap-python repository](https://kaio6fellipe.github.io/nmap-python/), if everything goes right, your folders will be organized that way:

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

# Example

I usually use this class like that:

```python
import ssh_enumeration

# Setting the target and the port
host = '192.168.0.120'
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
   "host":"192.168.0.120",
   "(gen) banner":"SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1",
   "(gen) software":"OpenSSH 4.7p1",
   "(gen) compatibility":"OpenSSH 4.7-6.6, Dropbear SSH 0.53+ (some functionality from 0.52)",
   "(gen) compression":"enabled (zlib@openssh.com)",
   "(cve) CVE-2018-15473":"(CVSSv2: 5.3) enumerate usernames due to timing discrepencies",
   "(cve) CVE-2016-3115 ":"(CVSSv2: 5.5) bypass command restrictions via crafted X11 forwarding data",
   "(cve) CVE-2014-1692 ":"(CVSSv2: 7.5) cause DoS via triggering error condition (memory corruption)",
   "(cve) CVE-2012-0814 ":"(CVSSv2: 3.5) leak data via debug messages",
   "(cve) CVE-2011-5000 ":"(CVSSv2: 3.5) cause DoS via large value in certain length field (memory consumption)",
   "(cve) CVE-2010-5107 ":"(CVSSv2: 5.0) cause DoS via large number of connections (slot exhaustion)",
   "(cve) CVE-2010-4755 ":"(CVSSv2: 4.0) cause DoS via crafted glob expression (CPU and memory consumption)",
   "(cve) CVE-2010-4478 ":"(CVSSv2: 7.5) bypass authentication check via crafted values",
   "(cve) CVE-2009-2904 ":"(CVSSv2: 6.9) privilege escalation via hard links to setuid programs",
   "(cve) CVE-2008-5161 ":"(CVSSv2: 2.6) recover plaintext data from ciphertext",
   "(cve) CVE-2008-1657 ":"(CVSSv2: 6.5) bypass command restrictions via modifying session file",
   "(cve) CVE-2008-1483 ":"(CVSSv2: 6.9) hijack forwarded X11 connections",
   "(kex) diffie-hellman-group-exchange-sha256 (1024-bit) ":"[fail] using small 1024-bit modulus",
   "(kex) diffie-hellman-group-exchange-sha1 (1024-bit) ":"[fail] using small 1024-bit modulus",
   "(kex) diffie-hellman-group14-sha1 ":"[warn] using weak hashing algorithm",
   "(kex) diffie-hellman-group1-sha1":"[fail] using small 1024-bit modulus",
   "`- [fail] removed (in server) since OpenSSH 6.7, unsafe algorith":"                                          `- [fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "`- [fail] disabled (in client) since OpenSSH 7.0, logjam attac":"                                          `- [fail] disabled (in client) since OpenSSH 7.0, logjam attack",
   "(key) ssh-rsa (2048-bit)":"[fail] using weak hashing algorithm",
   "(key) ssh-dss ":"[fail] using small 1024-bit modulus",
   "`- [fail] removed (in server) and disabled (in client) since OpenSSH 7.0, weak algorith":"                                          `- [fail] removed (in server) and disabled (in client) since OpenSSH 7.0, weak algorithm",
   "(enc) aes128-cbc":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "(enc) 3des-cbc":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "`- [warn] disabled (in client) since OpenSSH 7.4, unsafe algorith":"                                          `- [warn] disabled (in client) since OpenSSH 7.4, unsafe algorithm",
   "(enc) blowfish-cbc":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "`- [warn] disabled (in client) since OpenSSH 7.2, legacy algorith":"                                          `- [warn] disabled (in client) since OpenSSH 7.2, legacy algorithm",
   "(enc) cast128-cbc ":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "(enc) arcfour128":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "(enc) arcfour256":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "(enc) arcfour ":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "(enc) aes192-cbc":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "(enc) aes256-cbc":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "(enc) rijndael-cbc@lysator.liu.se ":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "(enc) aes128-ctr":"[info] available since OpenSSH 3.7, Dropbear SSH 0.52",
   "(enc) aes192-ctr":"[info] available since OpenSSH 3.7",
   "(enc) aes256-ctr":"[info] available since OpenSSH 3.7, Dropbear SSH 0.52",
   "(mac) hmac-md5":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "(mac) hmac-sha1 ":"[warn] using encrypt-and-MAC mode",
   "(mac) umac-64@openssh.com ":"[warn] using encrypt-and-MAC mode",
   "(mac) hmac-ripemd160":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "(mac) hmac-ripemd160@openssh.com":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "(mac) hmac-sha1-96":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "(mac) hmac-md5-96 ":"[fail] removed (in server) since OpenSSH 6.7, unsafe algorithm",
   "(fin) ssh-rsa":"SHA256:BQHm5EoHX9GCiOLuVscegPXLQOsuPs+E9d/rrJB84rk",
   "(rec) !diffie-hellman-group-exchange-sha256 ":"kex algorithm to change (increase modulus size to 2048 bits or larger) ",
   "(rec) -3des-cbc ":"enc algorithm to remove ",
   "(rec) -aes128-cbc ":"enc algorithm to remove ",
   "(rec) -aes192-cbc ":"enc algorithm to remove ",
   "(rec) -aes256-cbc ":"enc algorithm to remove ",
   "(rec) -arcfour":"enc algorithm to remove ",
   "(rec) -arcfour128 ":"enc algorithm to remove ",
   "(rec) -arcfour256 ":"enc algorithm to remove ",
   "(rec) -blowfish-cbc ":"enc algorithm to remove ",
   "(rec) -cast128-cbc":"enc algorithm to remove ",
   "(rec) -diffie-hellman-group-exchange-sha1 ":"kex algorithm to remove ",
   "(rec) -diffie-hellman-group1-sha1 ":"kex algorithm to remove ",
   "(rec) -hmac-md5 ":"mac algorithm to remove ",
   "(rec) -hmac-md5-96":"mac algorithm to remove ",
   "(rec) -hmac-ripemd160 ":"mac algorithm to remove ",
   "(rec) -hmac-ripemd160@openssh.com ":"mac algorithm to remove ",
   "(rec) -hmac-sha1-96 ":"mac algorithm to remove ",
   "(rec) -rijndael-cbc@lysator.liu.se":"enc algorithm to remove ",
   "(rec) -ssh-dss":"key algorithm to remove ",
   "(rec) -ssh-rsa":"key algorithm to remove ",
   "(rec) -diffie-hellman-group14-sha1":"kex algorithm to remove ",
   "(rec) -hmac-sha1":"mac algorithm to remove ",
   "(rec) -umac-64@openssh.com":"mac algorithm to remove ",
   "(fin) public ssh-rsa":"AAAAB3NzaC1yc2EAAAABIwAAAQEAstqnuFMBOZvO3WTEjP4TUdjgWkIVNdTq6kboEDjteOfc65TlI7sRvQBwqAhQjeeyyIk8T55gMDkOD0akSlSXvLDcmcdYfxeIF0ZSuT+nkRhij7XSSA/Oc5QSk3sJ/SInfb78e3anbRHpmkJcVgETJ5WhKObUNf1AKZW++4Xlc63M4KI5cjvMMIPEVOyR3AKmI78Fo3HJjYucg87JjLeC66I7+dlEYX6zT8i1XYwa/L1vZ3qSJISGVu8kRPikMv/cNSvki4j+qDYyZ2E5497W87+Ed46/8P42LNGoOV8OcX/ro6pAcbEPUdUEfkJrqi2YXbhvwIJ0gFMb6wfe5cnQew==",
   "nmap1":"-p22 -sC -sV",
   "info1":{
      "port":22,
      "state":"open",
      "reason":"syn-ack",
      "name":"ssh",
      "product":"OpenSSH",
      "version":"4.7p1 Debian 8ubuntu1",
      "extrainfo":"protocol 2.0",
      "conf":"10",
      "cpe":"cpe:/o:linux:linux_kernel",
      "script":{
         "ssh-hostkey":"\n  1024 60:0f:cf:e1:c0:5f:6a:74:d6:90:24:fa:c4:d5:6c:cd (DSA)\n  2048 56:56:24:0f:21:1d:de:a7:2b:ae:61:b1:24:3d:e8:f3 (RSA)"
      }
   },
   "nmap2":"-p22 --script ssh2-enum-algos",
   "info2":{
      "port":22,
      "state":"open",
      "reason":"syn-ack",
      "name":"ssh",
      "product":"",
      "version":"",
      "extrainfo":"",
      "conf":"3",
      "cpe":"",
      "script":{
         "ssh2-enum-algos":"\n  kex_algorithms: (4)\n      diffie-hellman-group-exchange-sha256\n      diffie-hellman-group-exchange-sha1\n      diffie-hellman-group14-sha1\n      diffie-hellman-group1-sha1\n  server_host_key_algorithms: (2)\n      ssh-rsa\n      ssh-dss\n  encryption_algorithms: (13)\n      aes128-cbc\n      3des-cbc\n      blowfish-cbc\n      cast128-cbc\n      arcfour128\n      arcfour256\n      arcfour\n      aes192-cbc\n      aes256-cbc\n      rijndael-cbc@lysator.liu.se\n      aes128-ctr\n      aes192-ctr\n      aes256-ctr\n  mac_algorithms: (7)\n      hmac-md5\n      hmac-sha1\n      umac-64@openssh.com\n      hmac-ripemd160\n      hmac-ripemd160@openssh.com\n      hmac-sha1-96\n      hmac-md5-96\n  compression_algorithms: (2)\n      none\n      zlib@openssh.com"
      }
   },
   "nmap3":"-p22 --script ssh-hostkey --script-args ssh_hostkey=full",
   "info3":{
      "port":22,
      "state":"open",
      "reason":"syn-ack",
      "name":"ssh",
      "product":"",
      "version":"",
      "extrainfo":"",
      "conf":"3",
      "cpe":"",
      "script":{
         "ssh-hostkey":"\n  ssh-dss AAAAB3NzaC1kc3MAAACBALz4hsc8a2Srq4nlW960qV8xwBG0JC+jI7fWxm5METIJH4tKr/xUTwsTYEYnaZLzcOiy21D3ZvOwYb6AA3765zdgCd2Tgand7F0YD5UtXG7b7fbz99chReivL0SIWEG/E96Ai+pqYMP2WD5KaOJwSIXSUajnU5oWmY5x85sBw+XDAAAAFQDFkMpmdFQTF+oRqaoSNVU7Z+hjSwAAAIBCQxNKzi1TyP+QJIFa3M0oLqCVWI0We/ARtXrzpBOJ/dt0hTJXCeYisKqcdwdtyIn8OUCOyrIjqNuA2QW217oQ6wXpbFh+5AQm8Hl3b6C6o8lX3Ptw+Y4dp0lzfWHwZ/jzHwtuaDQaok7u1f971lEazeJLqfiWrAzoklqSWyDQJAAAAIA1lAD3xWYkeIeHv/R3P9i+XaoI7imFkMuYXCDTq843YU6Td+0mWpllCqAWUV/CQamGgQLtYy5S0ueoks01MoKdOMMhKVwqdr08nvCBdNKjIEd3gH6oBk/YRnjzxlEAYBsvCmM4a0jmhz0oNiRWlc/F+bkUeFKrBx/D2fdfZmhrGg==\n  ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAstqnuFMBOZvO3WTEjP4TUdjgWkIVNdTq6kboEDjteOfc65TlI7sRvQBwqAhQjeeyyIk8T55gMDkOD0akSlSXvLDcmcdYfxeIF0ZSuT+nkRhij7XSSA/Oc5QSk3sJ/SInfb78e3anbRHpmkJcVgETJ5WhKObUNf1AKZW++4Xlc63M4KI5cjvMMIPEVOyR3AKmI78Fo3HJjYucg87JjLeC66I7+dlEYX6zT8i1XYwa/L1vZ3qSJISGVu8kRPikMv/cNSvki4j+qDYyZ2E5497W87+Ed46/8P42LNGoOV8OcX/ro6pAcbEPUdUEfkJrqi2YXbhvwIJ0gFMb6wfe5cnQew=="
      }
   },
   "nmap4":"-p22 --script ssh-auth-methods --script-args=\"ssh.user=root\"",
   "info4":{
      "port":22,
      "state":"open",
      "reason":"syn-ack",
      "name":"ssh",
      "product":"",
      "version":"",
      "extrainfo":"",
      "conf":"3",
      "cpe":"",
      "script":{
         "ssh-auth-methods":"\n  Supported authentication methods: \n    publickey\n    password"
      }
   }
}
```