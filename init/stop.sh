#!/bin/sh
source /etc/mlab/slice-functions
cd $SLICEHOME
if test -f $SLICEHOME/oonib.pid ; then
    sudo -u $SLICENAME kill `cat $SLICEHOME/oonib.pid`
    rm -f $SLICEHOME/oonib.pid
fi
