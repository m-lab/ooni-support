#!/usr/bin/env python

# This script builds the portion of the bouncer.yaml config file for the Ooni
# collector and test helpers running on an M-Lab slice. To use it, run `python
# getconfig.py`, and if all goes well, the YAML portion will be printed to
# stdout. If something goes wrong, an error message will be printed to stdout,
# and the exit status will be non-zero. The script assumes the oonib.conf file
# is in /home/mlab_ooni/oonib.conf. If not, pass the path as the first command
# line option.

import sys
import os
import yaml
import subprocess

def get_yaml_config_string(oonib_conf):
    try:
        # Open this slice's oonib.conf
        f = open(oonib_conf, "r")
        oonib_conf_contents = f.read()
        f.close()
        oonib_conf_parsed = yaml.safe_load(oonib_conf_contents)
    except IOError:
        return_failure("Couldn't read oonib.conf")

    try:
        # Read this slice's (collector) .onion address.
        tor_datadir = oonib_conf_parsed['main']['tor_datadir']
        tor_hostname_path = os.path.join(tor_datadir, 'collector', 'hostname')
        f = open(tor_hostname_path, "r")
        tor_onion_address = f.read().strip()
        f.close()
    except IOError:
        return_failure("Couldn't read Tor hostname file")
    except KeyError:
        return_failure("Oonib.conf is not valid or is missing information.")

    # Find this slice's IP address.
    slice_ipv4_address = get_ipv4_address()

    # List the running test helpers and their addresses.
    test_helpers = {}
    # FIXME: This should be a dynamically-generated list of all the test helpers
    # that are actually running. However, I have no idea how to infer which ones
    # are running and which ones aren't from the oonib.conf, since it seems to
    # be the same regardless of whether they're running or not (is there some
    # other source of information?)
    try:
        tcp_helpers_port = oonib_conf_parsed['helpers']['tcp-echo']['port']
        test_helpers['tcp-echo'] = slice_ipv4_address + ':' + str(tcp_helpers_port)
        http_return_headers_port = oonib_conf_parsed['helpers']['http-return-json-headers']['port']
        test_helpers['http-return-json-headers'] = 'http://' + slice_ipv4_address + ':' + str(http_return_headers_port)
    except KeyError:
        return_failure("Oonib.conf is not valid or is missing information.")

    config_part = {
        tor_onion_address: {
            'test-helpers': test_helpers
        }
    }

    return yaml.dump(config_part)

def get_ipv4_address():
    output = subprocess.Popen(["./get_ipv4.sh"], stdout=subprocess.PIPE).communicate()[0]
    return output.strip()

def return_failure(msg):
    print "ERROR: " + msg
    exit(1)

def printconfig(oonib_conf):
    print get_yaml_config_string(oonib_conf)

oonib_conf = '/home/mlab_ooni/oonib.conf'
if len(sys.argv) >= 2:
    oonib_conf = sys.argv[1]

# FIXME: Push to the mlab-ns simulator instead of printing.
printconfig(oonib_conf)

