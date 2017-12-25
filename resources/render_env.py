#!/bin/python
import os

from jinja2 import Environment, FileSystemLoader
from termcolor import colored
import argparse

def get_varible(var_name, default=None, skip_warning=False):
    if var_name in os.environ:
        return os.environ[var_name]

    if not skip_warning:
        print(colored('Environment variable {var_name} was not exist on system, '
            'setting value to default ({default})', 'red', attrs=['bold']).format(
                var_name=var_name, default=default))

    return default

def main(args):

    config_data = {
        "appliance_ip": get_varible("APPLIANCE_IP", skip_warning=args.skip_warnings),
        "wharf_ip": get_varible("WHARF_IP", skip_warning=args.skip_warnings),
        "wharf_port": get_varible("WHARF_PORT", skip_warning=args.skip_warnings),
        "sprout_url": get_varible("SPROUT_URL", skip_warning=args.skip_warnings)
    }

    # Load Jinja2 template
    env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('env.yaml.template')

    # Render the template with data and print the output
    print(template.render(config_data))

    with open(os.path.join(os.getenv("CONF_PATH", "/tmp"), "env.yaml"), "w") as outFile:
        for line in template.render(config_data):
            outFile.write(line)

if __name__=="__main__":
    
    parser = argparse.ArgumentParser(description='Reandering env.yaml util')
    parser.add_argument('--skip_warnings', dest='skip_warnings', action='store_true', default=False, help="Skip warning messages")

    main(parser.parse_args())

