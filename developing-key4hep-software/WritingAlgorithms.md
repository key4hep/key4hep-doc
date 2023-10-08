# Writing Gaudi Algorithms

# Gaudi

Gaudi is an event-processing framework. Algorithms can be defined by users and
Gaudi will take care of running them for each event. In addition, Gaudi has a
set of services and tools like logging and support for running in a
multithreaded environment.

The relationship with key4hep happens through
[k4FWCore](https://github.com/key4hep/k4FWCore). k4FWCore has tools and
utilities needed to be able to use (almost) seamlessly EDM4hep collections in
Gaudi algorithms. We recommend checking the
[tests](https://github.com/key4hep/k4FWCore/tree/main/test/k4FWCoreTest) in this
repository since they contain examples of algorithms (in particular of
algorithms using `Gaudi::Functional`).

# Gaudi::Functional
Using `Gaudi::Functional` is the recommended way of creating algorithms. The
design is simple and at the same time enforces several constraints at
compile-time, allowing for a quicker development cycle. In particular, we will
see that our algorithms won't have an internal state and we obtain the benefit
of being able to run in a multithreaded environment trivially[^1].

[^1]: It's possible to find algorithms written based on GaudiAlg which is going to be removed from future versions of Gaudi. GaudiAlg was substituted by Gaudi::Algorithm, although the recommended way is to use Gaudi::Functional.

## Setup
We will need Gaudi, k4FWCore and all their dependencies. Installing these by
ourselves is not easy but there are software stacks on cvmfs. For example, to
source the key4hep nightlies:

``` bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
```

The easiest way of having a working repository is to copy the template
repository that we provide in key4hep:

``` bash
git clone https://github.com/key4hep/k4-project-template
```

or ideally with ssh

``` bash
git@github.com:key4hep/k4-project-template.git
```

This template repository already has the cmake code that will make our
algorithms know where Gaudi and k4FWCore and to properly link to them.
Our development cycle will be based on cmake

##

Algorithms in Gaudi are relatively straightforward to write. For each algorithm
we want, we have to create a class that will inherit from one of the
Gaudi::Functional classes. The most important function member will be
`operator()` which is what will run over our events. There are several base
classes in Gaudi (see a complete list in
https://lhcb.github.io/DevelopKit/03a-gaudi/:
- Consumer, one or more inputs, no outputs
- Producer, one or more outputs, no inputs
- Transformer (and MultiTransformer), one or more inputs, one or more outputs

The structure of our class will then be, in the general case of the transformer:
``` cpp

#include "GaudiAlg/Transformer.h"
// Define BaseClass_t
#include "k4FWCore/BaseClass.h"

struct ExampleTransformer final
    : Gaudi::Functional::Transformer<colltype_out(const colltype_in&), BaseClass_t> {

  ExampleTransformer(const std::string& name, ISvcLocator* svcLoc);
  colltype_out operator()(const colltype_in& input) const override;
};
```
Some key points:
- The magic to make our algorithm work with EDM4hep collections happens by
  including `BaseClass.h` and passing it as one of the template arguments to 
- `operator()` is const, which means that it can't modify class members. This is
  intended and helps with multithreading by not having an internal state.

Let's start with the first template argument. It's the signature of a function
that returns one or more outputs and takes as input one or more inputs.
One possible example would be to have these two lines before the class definition:

``` cpp
using colltype_in  = edm4hep::MCParticleCollection;
using colltype_out = edm4hep::MCParticleCollection;
```

and then we have a transformer that will take one MCParticleCollection as input
and return another one. If we have multiple inputs we keep adding arguments to
the signature and if we don't have any we can leave that empty. For the output
this is slightly more complicated because if there are more than one output we
have to return an `std::tuple<OutputClass1, OutputClass2>`; if there aren't any
outputs we can simple return `void`.

Then the constructor. We'll always inherit from the constructor of the class
we're inheriting (in this example a `Transformer`) and then we'll initialize a
set of `KeyValues`. These `KeyValues` will be how we define the names of our
inputs and outputs so they can be found by other algorithms, read from a file or
saved to a file.

``` cpp
  ExampleTransformer(const std::string& name, ISvcLocator* svcLoc)
      : Transformer(name, svcLoc,
                    KeyValue("InputCollection", "MCParticles"),
                    KeyValue("OutputCollection", "NewMCParticles")) {
                    // possibly do something
                    }
```

Here we are defining how we will name our input collection in the steering value
("InputCollection") and giving it a default value. We're doing the same with the
output collection. The order is important here, first inputs then outputs and
they are ordered. When we have more inputs we just add another line. For
outputs, since they are bundled together in a `std::tuple` when there are
several, we have to enclose the list of `KeyValue` with brackets, like

``` cpp
  ExampleMultiTransformer(const std::string& name, ISvcLocator* svcLoc)
      : MultiTransformer(name, svcLoc,
                    KeyValue("InputCollection", "MCParticles"),
                    {
                    KeyValue("OutputCollection1", "NewMCParticles"),
                    KeyValue("OutputCollection2", "SimTrackerHits"),
                    KeyValue("OutputCollection3", "UsefulCollection"),
                    ) {
                    // possibly do something
                    }
```

Then in the `operator()` we can do whatever we want to do with our collections
``` cpp
  colltype_out operator()(const colltype_in& input) const override {
    auto coll_out = edm4hep::MCParticleCollection();
    for (const auto& particle : input) {
      auto new_particle = edm4hep::MutableMCParticle();
      new_particle.setPDG(particle.getPDG() + 10);
      new_particle.setGeneratorStatus(particle.getGeneratorStatus() + 10);
      new_particle.setSimulatorStatus(particle.getSimulatorStatus() + 10);
      new_particle.setCharge(particle.getCharge() + 10);
      new_particle.setTime(particle.getTime() + 10);
      new_particle.setMass(particle.getMass() + 10);
      coll_out->push_back(new_particle);
    }
    return coll_out;
```

When we return several collections we can bundle them in an `std::tuple` like this:

``` cpp
    return std::make_tuple(std::move(collection1), std::move(collection2));
```

The complete example for reference
``` cpp
```

The steering file

``` python

# This is an example reading from a file and using a consumer with several inputs
# to check that the contents of the file are the expected ones

from Gaudi.Configuration import INFO
from Configurables import ExampleFunctionalTransformer
from Configurables import ApplicationMgr
from Configurables import k4DataSvc
from Configurables import PodioOutput
from Configurables import PodioInput

podioevent = k4DataSvc("EventDataSvc")
podioevent.input = "output_k4test_exampledata_producer.root"

inp = PodioInput()
inp.collections = [
    "MCParticles",
]

out = PodioOutput("out")
out.filename = "output_k4test_exampledata_transformer.root"
# The collections that we don't drop will also be present in the output file
out.outputCommands = ["drop MCParticles"]

transformer = ExampleFunctionalTransformer("ExampleFunctionalTransformer",
                                           InputCollection="MCParticles",
                                           OutputCollection="NewMCParticles")

ApplicationMgr(TopAlg=[inp, transformer, out],
               EvtSel="NONE",
               EvtMax=10,
               ExtSvc=[k4DataSvc("EventDataSvc")],
               OutputLevel=INFO,
               )
```


## Initialize and finalize
There are some occasions where we may want to run some code between the
constructor and the `operator()`, that is the place for `initialize()`. There is
also a way of doing something after processing with `finalize()`. For that, we
can add to our classes those functions:
``` cpp
  StatusCode initialize() override;
  StatusCode finalize() override;
```
and then we can implement them.

Make sure to remember to return the corresponding status code, otherwise
Gaudi will crash. For example:
``` cpp
StatusCode MyAlgorithm::initialize() {
  // do something
  return StatusCode::SUCCESS;
}
```

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
