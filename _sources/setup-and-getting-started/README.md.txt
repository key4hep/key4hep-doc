# Getting started with Key4hep software

## Setting up the Key4hep Software Stack

### Using a central installation on cvmfs

Two builds with the key4hep stack are distributed on cvmfs. The releases happen
every few months on demand (for example, if there is a new important feature or
a breaking change) and at the moment only CentOS 7 is supported (support for
AlmaLinux 9 and Ubuntu is coming soon). Run the following to set up the stack:

```bash
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```

In addition, nightly builds for CentOS 7, AlmaLinux 9 and Ubuntu 22.04 with the
latest version of most of the packages are available:

```bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
```

The `setup.sh` script always points to the latest build and it will change
without warning. However, after sourcing the script some information will be
displayed with instructions on how to reproduce the current environment. Nightly
builds are intended for development and testing and they will be deleted after
some time from `/cvmfs`.
