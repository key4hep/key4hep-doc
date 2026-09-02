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

## Required system packages

The key4hep stack requires some system libraries to be present before sourcing
the setup script. On a minimal installation install them with:

```bash
apt install -y libgl1-mesa-glx libgl1-mesa-dev libglu1-mesa libglu1-mesa-dev   # Ubuntu
dnf install -y mesa-libGL mesa-libGL-devel mesa-libGLU mesa-libGLU-devel       # AlmaLinux 9
```

For building software from source you additionally need the compilers and
development tools:

```bash
apt install -y build-essential gfortran                             # Ubuntu
dnf groupinstall -y "Development Tools" && dnf install -y gfortran  # AlmaLinux 9
```

Alternatively, installing [HEP_OSlibs](https://gitlab.cern.ch/linuxsupport/rpms/HEP_OSlibs)
provides the typical set of system libraries needed at CERN.
