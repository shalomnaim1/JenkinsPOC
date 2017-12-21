#!/bin/python

#Import necessary functions from Jinja2 module
from jinja2 import Environment, FileSystemLoader

#Import YAML module
import yaml
import os

def get_varible(var_name, defualt=None):
    if os.environ.has_key(var_name):
        return os.environ[var_name]
    print "\033[01;31mEnvironment valiable {var_name} was not exist on system, setting value to dufualt ({defualt})\033[00m".format(var_name=var_name, defualt=defualt)
    return defualt

config_data = {"appliance_ip":get_varible("APPLIANCE_IP"),"wharf_ip":get_varible("WHARF_IP"),"worf_port":get_varible("WORF_PORT")}

#Load Jinja2 template
env = Environment(loader = FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template('env.yaml.template')

#Render the template with data and print the output
print(template.render(config_data))

with open(os.path.join(os.getenv("CONF_PATH","/tmp"),"env.yaml"), "w") as outFile:
    for line in template.render(config_data):
        outFile.write(line)
