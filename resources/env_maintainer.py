#!/bin/python
import os
import argparse
import time
from jinja2 import Environment, FileSystemLoader
from termcolor import colored

from cfme.test_framework.sprout.plugin import (SproutProvisioningRequest,
                                               SproutManager)

SPROUT_ONLY = "env.yaml.sprout.template"
FULL_ENV = "env.yaml.full.template"

class lease_applince():

    @staticmethod
    def get_appliance(stream, timeout=12 * 60, provision_timeout=60, version=None, date=None, desc=None,
                      override_ram=None, override_cpu=None, provider=None):
        # Creating an appliance
        sr = SproutProvisioningRequest(group=stream, count=1, version=version, date=date,
                                       lease_time=timeout, provision_timeout=provision_timeout,
                                       desc=desc, cpu=override_cpu, ram=override_ram, provider=provider)
        print(sr)
        sm = SproutManager()
        appliance_data = sm.request_appliances(sr)
        while not sm.check_fullfilled():
            print("waiting for fullfillment of appliance_data....")
            time.sleep(10)
        sm.reset_timer()
        print("appliance data:")
        for app in appliance_data:
            print("    {}: {}\n".format(app['name'], app['ip_address']))

        return [app['ip_address'] for app in appliance_data].pop()

    @staticmethod
    def destroy_appliances():
        # Destroying the collected appliances
        SproutManager().destroy_pool()

class config_util():

    def __init__(self, selected_population, target_file_path, config_params):
        self.env = Environment(loader=FileSystemLoader('../'), trim_blocks=True, lstrip_blocks=True)
        self.template = self.env.get_template(FULL_ENV if selected_population == "full" else SPROUT_ONLY)
        self.config_data = config_params
        self.conf_path = target_file_path

    def setup_env(self):
        # Render the template with data and print the output
        print(self.template.render(self.config_data))

        with open(os.path.join(self.conf_path, "env.yaml"), "w") as outFile:
            for line in self.template.render(self.config_data):
                outFile.write(line)


def validate_params(args):
    if args.populate_sprout_only and any([args.stream, args.appliance,
                                          args.stream, args.wharf_ip, args.wharf_port, args.lease_appliance]):
        print colored("Warning: ignoring all params\nrunning populate_sprout_only procedure!", 'yellow', attrs=['bold'])
        return True

    if args.action == "setup":
        if all([args.populate_sprout_only, args.sprout_url, args.config_path]) and \
                not all([args.appliance, args.stream, args.lease_appliance, args.wharf_ip, args.wharf_port]):
            return True
        elif all([(args.lease_appliance and bool(args.stream)) ^ args.appliance, args.wharf_ip,
                  args.wharf_port, args.sprout_url, args.config_path]):
            return True

        print colored("Error: Wrong parameter combination used", 'red', attrs=['bold'])
        return False

    if args.action == "destroy" and any([args.stream, args.appliance,
                                         args.stream, args.wharf_ip, args.wharf_port, args.lease_appliance,
                                         args.populate_sprout_only]):
        print colored("Warning: ignoring all params\nrunning destroy procedure!", 'yellow', attrs=['bold'])
        return True

def main():
    parser = argparse.ArgumentParser(description='Configuration management util')

    main_group = parser.add_argument_group('Main action')
    setup_group = parser.add_argument_group('Setup')

    main_group.add_argument('--action', type=str, choices=["setup", "destroy"], required=True,
                        help="Action to do")

    setup_group.add_argument('--lease_appliance', action="store_true", default=False,
                             help="leased an appliance from sprout")
    setup_group.add_argument('--stream', type=str, default=False,help="CFME stream to lease")
    setup_group.add_argument('--appliance', type=str, default=False,help="CFME appliance IP")
    setup_group.add_argument('--wharf_ip', type=str, default=False ,help="wharf's IP address")
    setup_group.add_argument('--wharf_port', type=str, default=False, help="wharf server's port number")
    setup_group.add_argument('--sprout_url', type=str, default=False, help="sprout's URL")
    setup_group.add_argument('--config_path', type=str, default=False, required=True, help="Configuration file path")

    setup_group.add_argument("--populate_sprout_only", action="store_true",
                             help="create only sprout section in env.yaml")

    args = parser.parse_args()
    if not validate_params(args):
        os._exit(1)

    if args.action =="setup":
        config_params = {}
        selected_population = None
        if args.populate_sprout_only:
            config_params = {"sprout_url": args.sprout_url}
            selected_population = "sprout"
        else:
            appliance_ip = lease_applince.get_appliance(args.stream) if args.lease_appliance else args.appliance
            config_params = {"appliance_ip": appliance_ip,
                             "sprout_url": args.sprout_url,
                             "wharf_ip":args.wharf_ip,
                             "wharf_port": args.wharf_port}
            selected_population = "full"

        config_obj = config_util(selected_population=selected_population,
                                 target_file_path=args.config_path,
                                 config_params=config_params)
        config_obj.setup_env()

    else:
        lease_applince.destroy_appliances()

if __name__=="__main__":
    main()

