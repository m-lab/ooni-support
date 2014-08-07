#!/bin/bash
#
# This script overwrites the Ooni bouncer configuration file on this
# host based on information gathered from mlab-ns (or a simulator).
# It then stops and starts the bouncer.
#
# If ENABLED is not 'true' it will skip this, so if you want to disable
# mlab-ns integration for the Ooni bouncer, set this to 'false':

ENABLED=true

if [ "$ENABLED" = 'true' ]; then
    # Note: This runs from cron which has a pristine environment, so
    # use absolute paths.

    # Fetch and install the latest bouncer configuration.
    su mlab_ooni -c "/home/mlab_ooni/bin/makeconfig.py"

    # Restart the bouncer.
    sudo /home/mlab_ooni/init/stop.sh
    sudo /home/mlab_ooni/init/start.sh
fi
