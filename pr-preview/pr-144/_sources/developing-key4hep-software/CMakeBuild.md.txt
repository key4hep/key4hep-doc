# Building Key4hep using CMake: For Developers

A common problem when developing is needing to build multiple packages on top of
the stack to test changes in several repositories. One way of doing this is
using Spack but there is an experimental way using cmake.

First, source the releases or the nightlies as usual. Then, run the following
command:

```
/cvmfs/sw-nightlies.hsf.org/key4hep/experimental/setup.py pkg1 pkg2
```

Where `pkg1` and `pkg2` are the packages that will be cloned (can be empty). On
top of that, `setup.py` checks for folders (or symbolic links) in the current
directory that contain `CMakeLists.txt`. This can be useful if we want to use a
local version and don't need to clone some repositories. After running the
command, a CMakeLists.txt file will appear. We may have to edit it manually if
we are using packages that are not recognized or are in a different organization
than the predefined ones. The information that we'll need to edit is most likely
one of the first lines at the top:

```
set(pkgs EDM4hep k4FWCore)
```
that sets the packages that will be built in their right build order.
and the individual `FetchContent_Declare` entries for each package.

After we are happy with the CMakeLists.txt file, it's important that we set the
new environment variables:

``` bash
mkdir install
cd install
export PATH=$PWD/bin:$PATH
export LD_LIBRARY_PATH=$PWD/lib:$PWD/lib64:$LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH=$PWD/include:$ROOT_INCLUDE_PATH
export PYTHONPATH=$PWD/python:$PYTHONPATH
export CMAKE_PREFIX_PATH=$PWD:$CMAKE_PREFIX_PATH
cd ..
```

Then, we can run the usual commands for building:

```
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make -j N install
```

and it will build all the packages at the same time, so it may take some time. Symbolic links are
created in the build directory for each package that allow us to run `ctest` like:

``` bash
cd k4FWCore
ctest -j 2
```

in case we are building k4FWCore.

For the cloned directories, in case we want to clone a different commit or
branch from the master/main branch, this can be done by editing the
CMakeLists.txt


## Possible issues

Not everything has been tested so it's likely some things won't work. For
many packages there are recent changes that enable these builds so using older
versions probably won't work.

## Packages that have been tested

The following packages have been built together successfully so it should be
possible to build any combination of them:
- podio
- EDM4hep
- k4FWCore
- LCIO
- ILCUTIL
- LCCD
- GEAR
- Marlin
- k4EDM4hep2LcioConv
- k4MarlinWrapper

## Changing to a different commit or branch

If we don't want to build the master or main branch of the repositories we are
cloning, we have two options:

- Set the commit or branch we want in the `CMakeLists.txt` in the corresponding
  `FetchContent_Declare` entry by changing `GIT_TAG` to whatever commit or branch
  we want to checkout.
- Go to the source directory, which can be found in the build directory under
  `_deps/<pkg>-src` and checkout manually whatever commit or branch you want.
