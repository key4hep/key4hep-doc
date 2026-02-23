# Getting key4hep

## With CVMFS

Two builds with the key4hep stack are distributed on cvmfs. The releases happen
every few months on demand (for example, if there is a new important feature or
a breaking change) and at the moment AlmaLinux 9 (EL9, Rocky Linux 9), Ubuntu
22.04 are supported. Some older releases also were built for CentOS7. For
sourcing the releases, run:

```bash
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```

In addition, nightly builds for AlmaLinux 9, Ubuntu 22.04 and Ubuntu 24.04 with
the latest version of most of the packages are available:

```bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
```

The `setup.sh` script always points to the latest build and it will change
without warning. However, after sourcing the script some information will be
displayed with instructions on how to reproduce the current environment.
**Nightly builds are intended for development and testing and they will be
deleted after some time from `/cvmfs`. They will also introduce new features
unannounced, so don't use these for anything else than development!**
