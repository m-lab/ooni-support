#!/bin/bash
# Fetch and install the latest bouncer configuration.
python2 makeconfig.py
# Restart the bouncer.
/home/mlab_ooni/init/stop.sh
/home/mlab_ooni/init/start.sh
