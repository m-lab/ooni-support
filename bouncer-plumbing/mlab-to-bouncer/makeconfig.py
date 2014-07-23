#!/usr/bin/env python

import sys
import yaml

def read_parts_from_stdin():
    data = sys.stdin.read()
    parts_string = data.split("----")
    parts_parsed = []
    for part in parts_string:
        part_parsed = yaml.safe_load(part)
        parts_parsed.append(part_parsed)
    return parts_parsed

def assemble_bouncer_config(parts):
    merged_parts = { }
    for part in parts:
        merged_parts.update(part)
    bouncer_config = { 'collector': merged_parts }
    return yaml.dump(bouncer_config)

def write_bouncer_config(path, bouncer_config_contents):
    try:
        f = open(path, 'w')
        f.write(bouncer_config_contents)
        f.close()
    except IOError:
        print "Couldn't write to bouncer config file."
        exit(1)


bouncer_config_path = '/home/mlab/data/bouncer.yaml'
if len(sys.argv) >= 2:
    bouncer_config_path = sys.argv[1]

# FIXME: Read from the mlab-ns simulator.
parts = read_parts_from_stdin()
bouncer_config = assemble_bouncer_config(parts)
write_bouncer_config(bouncer_config_path, bouncer_config)
