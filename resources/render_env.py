#!/bin/python
import os

from jinja2 import Environment, FileSystemLoader
from termcolor import colored

from DokerFiles.lease_appliance import get_appliance


def get_varible(var_name, defualt=None):
    if var_name in os.environ:
        return os.environ[var_name]
    print(colored('Environment variable {var_name} was not exist on system,'
                  ' setting value to default ({default})', 'red', attrs=['bold'])
          .format(var_name=var_name, defualt=defualt))
    return defualt

if 'APPLIANCE_IP' not in os.environ:
    os.environ['APPLIANCE_IP'] = get_appliance()

config_data = {
    "appliance_ip": get_varible("APPLIANCE_IP"),
    "wharf_ip": get_varible("WHARF_IP"),
    "worf_port": get_varible("WHARF_PORT")
}

# Load Jinja2 template
env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template('env.yaml.template')

# Render the template with data and print the output
print(template.render(config_data))

with open(os.path.join(os.getenv("CONF_PATH", "/tmp"), "env.yaml"), "w") as outFile:
    for line in template.render(config_data):
        outFile.write(line)
