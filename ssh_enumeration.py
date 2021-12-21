import os
import re
import importlib
python_nmap = importlib.import_module("nmap-python.python_nmap")

class iniEnumSSH():
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        self.dict = {"host": self.host}
        self.sshaudit()
        self.ssh_keyscan()
        self.ssh_nmap()

    def get_dict(self):
        return self.dict

    def sshaudit(self):
        try:
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            response_ssh_audit = os.popen("ssh-audit " +  self.host + " -p" + str(self.port)).read()

            for lines in response_ssh_audit.splitlines():
                new_lines = ansi_escape.sub('', lines)
                if "(gen)" in new_lines or "(fin)" in new_lines:
                    key_gen = new_lines[:new_lines.find(":")]
                    value_gen = new_lines[new_lines.find(":"):]
                    value_gen_replace = value_gen.replace(": ", "")
                    self.dict[key_gen] = value_gen_replace
                if "(" in new_lines and "#" not in new_lines and "(nfo)" not in new_lines and "(gen)" not in new_lines and "(fin)" not in new_lines:
                    replace_lines = new_lines.replace("  ", "")
                    key = replace_lines[:replace_lines.find("--")]
                    value = new_lines[new_lines.find("--")+3:]
                    self.dict[key] = value
        except Exception as err:
            print('[*] Exception while executing sshaudit: %s' % err)

    def ssh_keyscan(self):
        try:
            response_ssh_keyscan = os.popen("ssh-keyscan -t rsa " + self.host + " -p " + str(self.port)).read()
            for lines in response_ssh_keyscan.splitlines():
                if "ssh-rsa" in lines:
                    key_rsa = "(fin) public ssh-rsa"
                    value_rsa = lines[lines.find("ssh-rsa "):].replace("ssh-rsa ", "")
                    self.dict[key_rsa] = value_rsa
        except Exception as err:
            print('[*] Exception while executing ssh_keyscan: %s' % err)

    def ssh_nmap(self):
        try:
            document1, nmap_result1 = python_nmap.nmapCustomScanProcess(self.host, '-sC -sV', self.port)
            document2, nmap_result2 = python_nmap.nmapCustomScanProcess(self.host, '--script ssh2-enum-algos', self.port)
            document3, nmap_result3 = python_nmap.nmapCustomScanProcess(self.host, '--script ssh-hostkey --script-args ssh_hostkey=full', self.port)
            document4, nmap_result4 = python_nmap.nmapCustomScanProcess(self.host, '--script ssh-auth-methods --script-args="ssh.user=root"', self.port)

            for key1 in nmap_result1.keys():
                self.dict[key1 + '1'] = nmap_result1[key1]
            for key2 in nmap_result2.keys():
                self.dict[key2 + '2'] = nmap_result2[key2]
            for key3 in nmap_result3.keys():
                self.dict[key3 + '3'] = nmap_result3[key3]
            for key4 in nmap_result4.keys():
                self.dict[key4 + '4'] = nmap_result4[key4]
        except Exception as err:
            print('[*] Exception while executing ssh_nmap: %s' % err)