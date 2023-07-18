# Developing a single package

For quick changes of, for example, a single package, it's possible to compile
the package using cmake (after having sourced the release or nightlies) and then
export some environment variables manually so that our local version will be
picked up instead of the one in cvmfs:

``` bash
export PATH=/path/to/install/bin:$PATH
export LD_LIBRARY_PATH=/path/to/install/lib:/path/to/install/lib64:$LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH=/path/to/install/include:$ROOT_INCLUDE_PATH
export PYTHONPATH=/path/to/install/python:$PYTHONPATH
```

where the path to the installation is the one we gave cmake with
`-DCMAKE_INSTALL_PREFIX` when configuring. It's possible more environment
variables need to be set depending on which package we are installing but the
previous ones are the main ones for many of the packages of the key4hep stack.

While this approach works and any number of packages can be built this way, it
is cumbersome to do so for many packages, as one has to repeat the cycle of
configuring, building and installing and then exporting the environment
variables as many times as packages are installed. It is possible to miss
packages and then the cvmfs version will be used instead of the local one
without notice and it's also cumbersome to reproduce the environment at a later
time.
