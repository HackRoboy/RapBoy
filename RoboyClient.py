import os
import paramiko

class RoboyClient:

    def __init__(self, server, username, password):

        self.ssh = paramiko.SSHClient()
        self.ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        self.ssh.connect(server, username=username, password=password)

    def close(self):

        self.ssh.close()

    def send_file(self, localpath, remotepath):

        sftp = self.ssh.open_sftp()
        sftp.put(localpath, remotepath)
        sftp.close()
    
    def run_command(self, command):

        return self.ssh.exec_command(command)
    
    def remove_remote(self, filepath):

        sftp = self.ssh.open_sftp()
        sftp.remove(filepath)
        sftp.close()
    
