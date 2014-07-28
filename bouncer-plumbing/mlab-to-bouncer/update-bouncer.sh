#!/bin/bash
# Fetch and install the latest bouncer configuration.
python2 makeconfig.py
# Restart the bouncer.
sudo /home/mlab_ooni/init/stop.sh
sudo /home/mlab_ooni/init/start.sh
