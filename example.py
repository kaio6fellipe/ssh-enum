import ssh_enumeration

host = "10.0.0.248"
port = 22

enumeration = ssh_enumeration.iniEnumSSH(host, port)
enumeration.start()

dict = enumeration.get_dict()
print(dict)