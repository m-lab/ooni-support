#!/usr/bin/env python

import os
import yaml

# TODO: Accept the oonib.conf path on the command line.
def get_yaml_config_string(oonib_conf='/home/mlab_ooni/oonib.conf'):
    # Open this slice's oonib.conf
    # FIXME: Make sure errors are handled correctly, and file is closed.
    with open(oonib_conf, "r") as f
        oonib_conf_contents = f.read()
    oonib_conf_parsed = yaml.safe_load(oonib_conf_contents)

    # Read this slice's (collector) .onion address.
    tor_datadir = oonib_configuration['main']['tor_datadir']
    tor_hostname_path = os.path.join(tor_datadir, 'collector', 'hostname')
    # FIXME: Make sure errors are handled correctly, and file is closed.
    with open(tor_hostname_path, "r") as f
        tor_onion_address = f.read().strip()

    # Find this slice's IP address.
    slice_ipv4_address = get_ip_address()

    # TESTING: Print what we have so far:
    print slice_ipv4_address
    print tor_onion_address

def get_ip_address():
    output = Popen(["./get_ipv4.sh"], stdout=PIPE).communicate()[0]
    return output.strip()

def printconfig():
    print get_yaml_config_string()

printconfig()
