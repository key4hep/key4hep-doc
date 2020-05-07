
# Building Key4hep Software on Arch Linux with spack

[Arch](archlinux.org) is a Linux distribution that provides cutting-edge versions for many packages, including many HEP-software projects.
To build the Key4HEP software stack, it is advised to use the following system packages:

```
gcc gcc-fortran cmake clang make hdf4 root xrootd delphes hepmc pythia8 python cern-vdt boost libpng xz intel-tbb python-pythia8 python-yaml range-v3
```

Other system packages that may be useful for extending key4hep:

```
meson doxygen gnuplot lhapdf valgrind libmng gl2ps
```

This results in the following `packages.yaml` file for spack:



```
packages:
  cmake:
    buildable: False
    paths: 
      cmake: /usr
      cmake@3.14.3: /usr
  root:
    buildable: False
    paths: {root@6.20.04 cxxstd=17 +vdt +python +root7 +ssl +tbb +threads: /usr}
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
    paths:
      python@3.8.2: /usr
  boost:
    paths: {boost@1.72 +python +numpy ^python@3.8.2: /usr}
  expat:
    buildable: False
    paths: {expat: /usr}
  xerces-c:
    buildable: True
    paths: {xerces-c@3.2.3 cxxstd=11: /usr}
  libuuid:
    buildable: False
    paths: {libuuid: /usr}
  range-v3:
    buildable: False
    paths: {range-v3: /usr}
  intel-tbb:
    buildable: False
    paths: {intel-tbb: /usr}
  meson:
    buildable: False
    paths: {meson: /usr}
  tar:
    buildable: False
    paths: {tar: /usr}
  gnuplot:
    buildable: False
    paths: {gnuplot@5.2.7: /usr}
  gl2ps:
    buildable: False
    paths: {gl2ps: /usr}
  hdf5:
    buildable: False
    paths: {hdf5@1.10.5 +hl: /usr}
  doxygen:
    buildable: False
    paths: {doxygen +graphviz: /usr}
  valgrind:
    buildable: False
    paths: {valgrind: /usr}
  libmng:
    buildable: False
    paths: {libmng: /usr}




```

