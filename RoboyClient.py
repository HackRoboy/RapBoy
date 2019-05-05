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
        # https://www.unixtutorial.org/atime-ctime-mtime-in-unix-filesystems
        # mtime - used for tracking the actual changes to data of the file itself.
        mtime = 0
        try:
            # returns http://docs.paramiko.org/en/2.4/api/sftp.html#paramiko.sftp_attr.SFTPAttributes
            stat = sftp.stat(remotepath)
            mtime = stat.st_mtime
        except FileNotFoundError:
            print('There is no such file on remote yet ' + remotepath)
        # also returns http://docs.paramiko.org/en/2.4/api/sftp.html#paramiko.sftp_attr.SFTPAttributes
        stat = sftp.put(localpath, remotepath)
        new_mtime = stat.st_mtime
        sftp.close()
        return new_mtime > mtime
        # sftp = self.ssh.open_sftp()
        # sftp.put(localpath, remotepath)
        # sftp.close()
    
    def run_command(self, command):

        return self.ssh.exec_command(command)
    
    def remove_remote(self, filepath):

        sftp = self.ssh.open_sftp()
        sftp.remove(filepath)
        sftp.close()
    
