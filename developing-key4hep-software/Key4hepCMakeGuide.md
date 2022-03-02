# CMake guide for Key4hep software

## Overview

CMake is a tool for building software, which has become the de-facto
standard outside HEP. In HEP, it is for example used by the ILC/CLIC
communities and by the LHCb collaboration. For CMS people, CMake is the
equivalent of scram.

## Quick start into building Key4hep Software

### Set up the environment

The first step is adding all dependencies to the bash environment. 
In case you are unsure, it is best to use the default init script, provided on CVMFS for Centos7:

```
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```

Note that mixing setup scripts (from another package, for example) may or may not work as intended - more likely not.
For any requests to changes in the environment, feel free to contact the software team on the mailing list or any other channels.
Developers may also look into `spack` to have more fine-grained control over the build dependencies.


### Running CMake

* Create a build directory: `mkdir build; cd build`
* Run CMake in the build directory: `cmake .. `
* Change any cmake options by rerunning cmake.\
  For example: `cmake .. -DCMAKE_INSTALL_PREFIX=../install -DCMAKE_BUILD_TYPE=Debug`.\
  Tools like ccmake may also be useful: `ccmake ..`
* Compile the software, using all the cpus available:    ```make -j `getconf _NPROCESSORS_ONLN` ```  
* Install by running `make install`
* In case any dependency is changed, most likely you need to remove all the contents of the build folder and rerun cmake and the compilation.

### Using your local installation

In order to run the code you just installed, there are a few environment variables to set up (assuming the installation directory is the working directory):

```
mkdir build; cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../InstallArea
make install
cd ../InstallArea
```

* `export CMAKE_PREFIX_PATH=$PWD/:$CMAKE_PREFIX_PATH`
  - in order to use this installation as a dependency for other packages
* `export PATH=$PWD/bin/:$PATH`
  - in order to make any executables available on the command line
* `export LD_LIBRARY_PATH=$PWD/lib:$PWD/lib64:$LD_LIBRARY_PATH`
  - in order to make libraries available for linking and as for the plugin systems in Gaudi/DD4hep
* `export PYTHONPATH=$PWD/python:$PYTHONPATH`
  - in order to make libraries available for linking and as for the plugin systems in Gaudi/DD4hep
* `export ROOT_INCLUDE_PATH=$PWD/include:$ROOT_INCLUDE_PATH`
  - in case the package builds ROOT dictionaries
* `export <PACKAGENAME>=$PWD/share/<PackageName>`
  - some packages distribute data files that are found with a special environment variable, usually this is the package name in all caps.
  - e.g. `export K4SIMDELPHES=$PWD/share/k4SimDelphes/`

## CMake example packages

Colin provides [a few simple CMake
examples](https://github.com/cbernet/cmake-examples). They are helpful to understand the basics of
CMake.

Get these packages:

    git clone https://github.com/cbernet/cmake-examples.git
    cd cmake-examples

Follow the instructions in
[README.md](https://github.com/cbernet/cmake-examples/blob/master/README.md).

## Changing the CMake Configuration


When adding new source files to a package, the CMake build system needs
to be made aware of them. Usually `CMakeLists.txt` contains a wildcard
expression that adds all implementation files in a subfolder, e.g.
`src/*.cpp` , so there is no need to explicitly add the names of the
new files. To update the list of files, it is fastest to run
`make configure` .

Note that when changing the name of a property of an algorithm or a
tool, `make` (and not only `make packagename` ) needs to be run for
Gaudi to be aware of the change.


### Runtime Environment

Key4hep packages, in particular the gaudi framework components, consist of executables, headers, scripts, dynamic libraries, xmls  and special files describing gaudi components.
In order to use these, some environment variables need to be set.

Gaudi also offers the possibility to set up the environment via the `xenv` command. This is done by simply prefixing the command you want to run with the `run` script in the top level directory of FCCSW, or directly in the build directory.

```bash
./build/run key4run Examples/options/pythia.py
```

Sometimes it is convenient to run FCCSW directly from the binaries in the build directory without installing them.
This can be done by using the `run` script in the build directory, or setting the environment variables as in `setup.sh` for the build folder.
Note that the directories in the  build folder differ a bit. Mostly it is important the the LD_LIBRARY_PATH is pre-fixed with the library directories. The fccrun command should pick up the components from the build folder then.



## CTest in Key4hep

Key4hep also uses CMake for integration tests.
They are added with `add_test()` and can be run with `make test` in the build folder. For Gaudi packages, the environment should be set so they can be run also in a build environments, see https://github.com/HEP-FCC/k4Gen/blob/main/k4Gen/CMakeLists.txt 



### Customizing how CMake is run

An environment variable is used to forward command line arguments to the cmake command, for example to run cmake with the `trace` option:

```
CMAKEFLAGS='--trace' make
```

{% callout "How do I check compilation flags?" %}

Instead of running `  make` , run:

 ```bash
 make VERBOSE=1 
 ```

{% endcallout %}
