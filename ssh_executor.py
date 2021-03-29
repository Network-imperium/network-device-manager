from paramiko import SSHClient, AutoAddPolicy

class Client:
    def __init__ (self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def _connect (self):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(
            self.host, 
            username=self.username,
            password=self.password
        )
        return self.client

    def disconnect (self):
        if self.client:
            self.client.close()

    def execute (self, command):
        self.conn = self._connect()
        stdin, stdout, stderr = self.client.exec_command(command)
        res = stdout.readlines()
        return res