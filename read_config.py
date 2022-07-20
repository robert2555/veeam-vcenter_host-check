import configparser


class ReadConfig:
    def __init__(self, config_path):
        # Read from the config
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def get_veeam_host(self):
        return self.config['VeeamSettings']['host']

    def get_veeam_user(self):
        return self.config['VeeamSettings']['user']

    def get_veeam_pass(self):
        return self.config['VeeamSettings']['pass']

    def get_vcenter_host(self):
        return self.config['vCenterSettings']['host']

    def get_vcenter_user(self):
        return self.config['vCenterSettings']['user']

    def get_vcenter_pass(self):
        return self.config['vCenterSettings']['pass']

    def get_ignore_hosts(self):
        return self.config['Additional']['ignore hosts'].split(", ")
