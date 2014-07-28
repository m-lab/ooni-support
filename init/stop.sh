#!/bin/sh
source /etc/mlab/slice-functions
cd $SLICEHOME
if test -f $SLICEHOME/oonib.pid ; then
    kill `cat $SLICEHOME/oonib.pid`
fi

if test -f $SLICEHOME/mlabsim.pid ; then
    kill `cat $SLICEHOME/mlabsim.pid`
    rm "$SLICEHOME/mlabsim.pid"
fi
