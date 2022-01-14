import paramiko

class SshClient:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self, ip_addr, username, password, port):
        try:
            self.ssh.connect(ip_addr, username=username, password=password, port=port, timeout=10)
        #Throw exception
        except Exception as e:
            raise e


    def exec_cmd(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            stdin.flush()
            return stdout.read()
        except Exception as e:
            raise e

    def disconnect(self):
        try:
            self.ssh.close()
            return True
        except Exception as e:
            raise e
