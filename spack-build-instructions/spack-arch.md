
# Building Key4hep Software on Arch Linux with spack

[Arch](archlinux.org) is a Linux distribution that provides cutting-edge versions for many packages, including many HEP-software projects.
To build the Key4HEP software stack, it is advised to use the following system packages:

```
gcc cmake make root xrootd delphes hepmc pythia8 python cern-vdt boost libpng xz intel-tbb
```

This results in the following `packages.yaml` file for spack:



```
packages:
  cmake:
    buildable: False
    paths: {cmake: /usr}
  root:
    buildable: False
    paths: {root@6.20.04 cxxstd=17 +tbb +vdt: /usr}
  xrootd:
    buildable: False
    paths: {xrootd: /usr}
  hepmc:
    buildable: False
    paths: {hepmc: /usr}
  delphes:
    buildable: False
    paths: {delphes: /usr}
  pythia8:
    buildable: False
    paths: {pythia8: /usr}
  py-pyyaml:
    buildable: False
    paths: {py-pyyaml: /usr}
  xz:
    buildable: False
    paths: {xz: /usr}
  libpng:
    buildable: False
    paths: {libpng: /usr}
  python:
    buildable: False
    paths: {python: /usr}
  boost:
    buildable: False
    paths: {boost: /usr}

```

