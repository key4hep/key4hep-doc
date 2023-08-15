# Writing Gaudi Algorithms


{% objectives "Learning Objectives" %}

This tutorial will teach you how to:

* write an algorithm for Key4hep
* interact with the cmake based build system 
* use other Gaudi components in the algorithms 

{% endobjectives %}


## Getting Started

Writing Gaudi components requires a bit of boilerplate code.
Often it is easiest to start from existing files and modify them as needed.
For this tutorial, there is a dedicated repository that contains an example.
Start by cloning it locally:

```bash
git clone https://github.com/key4hep/k4-project-template
```

It contains a CMake configuration (as described in more detail in the previous tutorial) so it can be built with:

```bash
cd k4-project-template
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make -j 4
```

To run the algorithms contained in this repository, it is not necesary to run

```
make install
```

you can use the `run` script in the `build` directory, like:

```bash
./run k4run ../K4TestFWCore/options/createExampleEventData.py 

```


## Exercise: Adding an Algorithm

The repository contains an `EmptyAlg` in `K4TestFWCore/src/components`.


* As a first exercise, copy and modify this algorithm to print out the current event number.

* Second step: If you used `std::cout` in the first step, try to use the gaudi logging service instead.

* Third Step: Print out a string before the event number that should be configurable at runtime.

* Finally: use the Gaudi Random Number Generator Service to approximate pi with a [Monte Carlo Integration](https://en.wikipedia.org/wiki/Monte_Carlo_integration)


## Debugging: How to use GDB

[The GNU Project Debugger](https://www.sourceware.org/gdb/) is supported by
Gaudi and can be invoked by passing additional `--gdb` parameter to the `k4run`.
For example:
```bash
k4run ../K4TestFWCore/options/createExampleEventData.py --gdb
```
This will start the GDB and attaches it to the Gaudi steering. After initial
loading, user can start running of the steering by typing `continue` into the
GDB console. To interrupt running of the Gaudi steering use `CTRL+C`.

More details how to run GDB with Gaudi can be found in
[LHCb Code Analysis Tools](https://twiki.cern.ch/twiki/bin/view/LHCb/CodeAnalysisTools#Debugging_gaudirun_py_on_Linux_w).
