ooni-support
============

Support scripts for OONI on M-Lab

```
sudo yum install git svn rpm-build m4
git clone --recursive https://github.com/m-lab-tools/ooni-support.git
cd ooni-support
git checkout <tag>
# Note this command will build the rpm package but delete /home/mlab_ooni/,
# therefore you should have cloned the above repository inside of some
# temporary directory.
./package/slicebuild.sh mlab_ooni
```
