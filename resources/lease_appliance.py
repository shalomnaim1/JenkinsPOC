import time
import os
import argparse

from cfme.test_framework.sprout.plugin import (SproutProvisioningRequest,
                                               SproutManager)


def get_appliance(stream, timeout=12*60, provision_timeout=60, version=None, date=None, desc=None,
                  override_ram=None, override_cpu=None, populate_yaml=False, provider=None):
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
    
    os.environ["APPLINCE_IP"] = [app['ip_address'] for app in appliance_data].pop()
    return os.environ["APPLINCE_IP"]


def destroy_appliances():
    # Destroying the collected appliances
    SproutManager().destroy_pool()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Lease appliance script', add_help=True)
    parser.add_argument('--action', choices=['lease', 'destroy'] ,required=True, help="Action to do [lease or destroy]")
    parser.add_argument('--stream', type=str ,help="Vesrion of CFME to lease")
    
    args = parser.parse_args()
    
    actions = {"lease": get_appliance, "destroy":destroy_appliances}
    actions_args = {"lease": {args.stream}, "destroy": {}}
    
    actions[args.action](**actions_args[args.action])

