#!/bin/sh

source /etc/mlab/slice-functions
cd $SLICEHOME
$SLICEHOME/bin/oonib -c $SLICEHOME/oonib.conf &
