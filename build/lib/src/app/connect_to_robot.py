# scp command: scp -i ot2_ssh_key -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ./your_file.csv root@169.254.235.94:/data/your_folder
import os
from paramiko import SSHClient, client

from scp import SCPClient


# Other wired IP: 169.254.199.133  169.254.236.41


class OT2Connect:
    def __init__(self, local_path, file_name, expr_type):
        # host info
        self.host = '169.254.140.23'
        self.robot_usr = "root"
        self.key_path = self.find_key(name='ot2_ssh_key', path=os.path.join(os.path.expanduser('~'), '.ssh'))
        self.key_passphrase = "pass"
        self.connection = self._establish_connection()
        self.file_name = file_name
        self.local_path = local_path
        self.data_root = os.path.join(os.path.sep, "data", "platemaps")
        self.remote_expr_dir = expr_type

    def find_key(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)

    def _establish_connection(self):
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(client.AutoAddPolicy)
        try:
            ssh.connect(hostname=self.host, username=self.robot_usr, passphrase=self.key_passphrase,
                        key_filename=self.key_path, timeout=1)
            return ssh
        except Exception as e:
            return None

    def save_file_to_robot(self):
        with SCPClient(self.connection.get_transport()) as scp:
            scp.put(os.path.join(self.local_path), os.path.join(self.data_root, self.remote_expr_dir))
