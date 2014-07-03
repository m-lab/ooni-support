M-Lab Deployment Process
=========================

This document describes the process of deploying Ooni on M-Lab. It assumes the
steps in the [Ooni Deployment Process](http://example.org/) document have been
completed by the Ooni team.

**TODO:** Fix the above URL.

What's Required
----------------

This is a checklist of all the things that are necessary for the deployment.
Ensure that you have them all before starting.

### For RPM Building

- Git: `yum install git`
- SVN: `yum install svn`
- rpm-build: `yum install rpm-build`
- m4: `yum install m4`
- A *recursive* clone of the `ooni-support` repository.
    - `git clone --recursive https://github.com/m-lab-tools/ooni-support.git`

### For Ooni Installation

- The Ooni `.rpm` file.
- A clone of the `ooni-support` repository.
- `/etc/mlab/slice-functions` must exist, containing the M-Lab slice functions.

Building the Ooni RPM
----------------------

With the recursive clone of `ooni-support` in a temporary not inside
`/home/mlab_ooni`, perform the following steps.

1. Change directories into the `ooni-support` clone.
2. Run `git checkout <tag>` where `<tag>` is the tag you want to build.
3. Ensure that it is OK to delete everything in `/home/mlab_ooni`.
4. Run `./package/slicebuild.sh mlab_ooni`.

**WARNING:** The last step will remove all files and subdirectories in
`/home/mlab_ooni`.

**NOTE:** The `ooni-support` clone MUST be outside of `/home/mlab_ooni`,
otherwise, otherwise an `rsync` copy will go into an infinite loop because of
the destination directory being inside the source directory.

This will create an `mlab_ooni-XYZ.rpm` file (where `XYZ` is the version number
and architecture name) inside of `build/slicebase-i386/i686/` in the
`ooni-support` clone.

Installing the RPM
-------------------

With the `mlab_ooni-XYZ.rpm` (where `XYZ` is a placeholder for the version and
architecture of the build) file, run the following commands:

    sudo yum install yum-cron
    sudo rpm -Uvh mlab_ooni-XYZ.rpm

This installs the Ooni backend software on the slice. Next, initialize the Ooni
configuration.

Initializing the Ooni Configuration
------------------------------------

To initialize the Ooni configuration, change directories into the `init`
subdirectory of the `ooni-support` repository, then run the following commands:

    sudo mkdir /etc/mlab
    sudo ./initialize.sh

This will create the Ooni configuration. Ooni is now ready to be started.

Starting and Stopping Ooni
---------------------------

To start and stop the Ooni backend service, change directories into the `init`
subdirectory of the `ooni-support` repository and run `start.sh` and `stop.sh`
respectively.

Testing
--------

After deployment, tests should be performed to ensure Ooni is working properly.
These tests are out of scope of this document.
