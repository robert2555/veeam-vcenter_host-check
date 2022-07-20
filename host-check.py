import hosts_veeam
import hosts_vcenter
import read_config
import sys
from os.path import exists
import getopt


def get_config_path():
    # Get the passed args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:")
    except getopt.GetoptError:
        print("Usage: host-check.py -f <path-to-config>")
        sys.exit(2)

    # Check if args are valid
    if not opts or opts[0][0] != "-f":
        print("Usage: host-check.py -f <path-to-config>")
        sys.exit(2)

    file_path = opts[0][1]

    # Check if the file exists
    if not exists(file_path):
        print("Could not find file: "+file_path)
        sys.exit(2)

    # Return the config path
    return file_path


def compare_hosts(veeam_list, vcenter_list, ignore_hosts):
    # Check with Host Output
    missing_hosts = list(set(veeam_list) - set(vcenter_list)) + list(set(vcenter_list) - set(veeam_list))

    # If ignore list exists, remove hosts from the list
    if ignore_hosts:
        for host in ignore_hosts:
            missing_hosts.remove(host)

    # Check for hosts in the list
    if not missing_hosts:
        return True
    else:
        return missing_hosts


def main():
    config_path = get_config_path()
    config = read_config.ReadConfig(config_path)

    # Get Veeam credentials
    veeam_host = config.get_veeam_host()
    veeam_user = config.get_veeam_user()
    veeam_pass = config.get_veeam_pass()

    # Get vcenter credentials
    vcenter_host = config.get_vcenter_host()
    vcenter_user = config.get_vcenter_user()
    vcenter_pass = config.get_vcenter_pass()

    # Get Additional config
    ignore_hosts = config.get_ignore_hosts()

    # Get Host Lists
    veeam_list = hosts_veeam.get_hosts(veeam_host, veeam_user, veeam_pass)
    vcenter_list = hosts_vcenter.get_hosts(vcenter_host, vcenter_user, vcenter_pass)

    # Compare the lists
    result = compare_hosts(veeam_list, vcenter_list, ignore_hosts)

    if result is True:
        print("All hosts in backup Jobs")
    else:
        print("Hosts not in backup Jobs: " + ', '.join(result))


if __name__ == '__main__':
    main()

