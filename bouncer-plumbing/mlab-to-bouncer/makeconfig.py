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

def write_bouncer_config(bouncer_config, path):
    print bouncer_config


parts = read_parts_from_stdin()
bouncer_config = assemble_bouncer_config(parts)
write_bouncer_config(bouncer_config, '/home/mlab/data/bouncer.yaml')
