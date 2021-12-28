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