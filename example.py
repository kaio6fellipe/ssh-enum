import ssh_enumeration

host = "10.0.0.248"

enumeration = ssh_enumeration.iniEnumSSH(host, 22)
enumeration.start()

dict = enumeration.get_dict()
print(dict)