# Writing Gaudi Algorithms

## Gaudi

Gaudi is an event-processing framework. Algorithms can be defined by users and
Gaudi will take care of running them for each event. In addition, Gaudi has a
set of services and tools like logging and support for running in a
multithreaded environment.

The relationship between Gaudi with key4hep happens through
[k4FWCore](https://github.com/key4hep/k4FWCore). k4FWCore has tools and
utilities needed to be able to use (almost) seamlessly EDM4hep collections in
Gaudi algorithms. We recommend checking out the
[tests](https://github.com/key4hep/k4FWCore/tree/main/test/k4FWCoreTest) in this
repository since they contain examples of algorithms (in particular of
algorithms using `Gaudi::Functional`).

# Gaudi::Functional
Using `Gaudi::Functional` is the recommended way of creating algorithms. The
design is simple and at the same time enforces several constraints at
compile-time, allowing for a quicker development cycle. In particular, we will
see that our algorithms won't have an internal state and we obtain the benefit
of being able to run in a multithreaded environment (almost) trivially[^1].

[^1]: It's possible to find algorithms written based on GaudiAlg which is going to be removed from future versions of Gaudi. GaudiAlg was substituted by Gaudi::Algorithm, although the recommended way is to use Gaudi::Functional.

## Setup
We will need Gaudi, k4FWCore and all their dependencies. Installing these by
ourselves is not easy but there are software stacks on cvmfs, see this
[page](../getting_started/setup.md) to set up the key4hep stack.

The easiest way of having a working repository is to copy the template
repository that we provide in key4hep:

``` bash
git clone https://github.com/key4hep/k4-project-template
```

or ideally with ssh

``` bash
git clone git@github.com:key4hep/k4-project-template
```

This template repository already has the cmake code that will make our
algorithms know where Gaudi and k4FWCore and to properly link to them. In
addition there are a few examples that combined with the tests in k4FWCore
provide an overview of what's possible to do. The `k4-project-template`
repository contains a CMake configuration (as described in more detail in the
previous tutorial) so it can be built with:

```bash
cd k4-project-template
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make -j 4 install
```

To run the algorithms contained in this repository you can use `k4run`, like:

```bash
k4run ../K4TestFWCore/options/createExampleEventData.py 

```

## Walkthrough of Functional Algorithms

Functional algorithms in Gaudi are relatively straightforward to write. For each
algorithm we want, we have to create a class that will inherit from one of the
`Gaudi::Functional` classes. The most important function member will be
`operator()` which is what will run over our events (or over none in case we are
generating). There are several base classes in Gaudi (see a more complete list
in https://lhcb.github.io/DevelopKit/03a-gaudi/):
- Consumer, one or more inputs, no outputs
- Producer, one or more outputs, no inputs
- Transformer (and MultiTransformer), one or more inputs, one or more outputs

The structure of our class (more precisely structs) will then be, in the general
case of the transformer:

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
  including `BaseClass.h` and passing `BaseClass_t` it as one of the template
  arguments to the Gaudi class we are inheriting from.
- `operator()` is const, which means that it can't modify class members. This is
  intended and helps with multithreading by not having an internal state.

Let's start with the first template argument. It's the signature of a function
that returns one or more outputs and takes as input one or more inputs.
One possible example would be to have these two lines before the class definition:

``` cpp
using colltype_in  = edm4hep::MCParticleCollection;
using colltype_out = edm4hep::MCParticleCollection;
```

and then we have a transformer that will take one `MCParticleCollection` as
input and return another one. If we have multiple inputs we keep adding
arguments to the function arguments and if we don't have any we can leave that
empty. For the output this is slightly more complicated because if there are
more than one output we have to return an `std::tuple<OutputClass1,
OutputClass2>`; if there aren't any outputs we can simply return `void`.

Then we reach the constructor. We'll always initialize from the constructor of the
class we're inheriting (in this example a `Transformer`) and then we'll
initialize a set of `KeyValues`. These `KeyValues` will be how we define the
names of our inputs and outputs so they can be found by other algorithms, read
from a file or saved to a file.

``` cpp
  ExampleTransformer(const std::string& name, ISvcLocator* svcLoc)
      : Transformer(name, svcLoc,
                    KeyValue("InputCollection", "MCParticles"),
                    KeyValue("OutputCollection", "NewMCParticles")) {
                    // possibly do something
                    }
```

Here we are defining how we will name our input collection in the steering value
(`InputCollection`) and giving it a default value. We're doing the same with the
output collection. The order is important here: first inputs and then outputs
and they are ordered. When we have more inputs we just add another line, like
the one above for the input collection. For outputs, since they are bundled
together in a `std::tuple` when there are several, we have to enclose the list
of `KeyValue` with brackets, like

``` cpp
  ExampleMultiTransformer(const std::string& name, ISvcLocator* svcLoc)
      : MultiTransformer(name, svcLoc,
                    KeyValue("InputCollection", "MCParticles"),
                    {
                    KeyValue("OutputCollection1", "NewMCParticles"),
                    KeyValue("OutputCollection2", "SimTrackerHits"),
                    KeyValue("OutputCollection3", "UsefulCollection"),
                    }
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

The complete example for reference can be found in the tests of k4FWCore:
https://github.com/key4hep/k4FWCore/blob/main/test/k4FWCoreTest/src/components/ExampleFunctionalTransformer.cpp

## The steering file

The steering file is the file where we define which algorithms will run, what
parameters they will use and how they will do it; what level of logging, if
using multithreading, etc.

We start with some imports

``` python
from Gaudi.Configuration import INFO
from Configurables import ExampleFunctionalTransformer
from Configurables import ApplicationMgr
from Configurables import k4DataSvc
from Configurables import PodioOutput
from Configurables import PodioInput
```

it's also possible to import everything from `Configurables` but it's better not
to so that if we are using IDE or an editor with some kind of analysis it can
tell us if we are using an undefined variable, for example.

Then, the input:

``` python
podioevent = k4DataSvc("EventDataSvc")
podioevent.input = "output_k4test_exampledata_producer.root"

inp = PodioInput()
inp.collections = [
    "MCParticles",
]
```

We select the name of the input file and which collections we'll make available
for the rest of the algorithms.

For the output:

``` python
out = PodioOutput("out")
out.filename = "output_k4test_exampledata_transformer.root"
# The collections that we don't drop will also be present in the output file
out.outputCommands = ["drop MCParticles"]
```

we can select which collections we keep in the output file. By default the
collections in the output file will be the same as in the input file. Check the
[relevant
documentation](https://github.com/key4hep/k4FWCore/blob/main/doc/PodioInputOutput.md)
to learn more about `PodioInput` and `PodioOutput`.

Our algorithm will look like this:

``` python
transformer = ExampleFunctionalTransformer("ExampleFunctionalTransformer",
                                           InputCollection="MCParticles",
                                           OutputCollection="NewMCParticles")
```

If we have defined `Gaudi::Property`s for our algorithm it is also possible to
change them by doing `transformer.property = value`; however with the names of
the collections, if they are provided, they are set when creating the python
object with our algorithm.

Finally we define what to run:

``` python
ApplicationMgr(TopAlg=[inp, transformer, out],
               EvtSel="NONE",
               EvtMax=10,
               ExtSvc=[k4DataSvc("EventDataSvc")],
               OutputLevel=INFO,
               )
```

We pass a list of the algorithms in `TopAlg`. `PodioInput` will be the first one
and `PodioOutput` will be the last one when used. In `EvtMax` we set what is the
maximum number of event that we are processing. Use -1 not to limit it. That
means if we are processing a file, then read all the events in the file. We pass
extra services to `ExtSvc` and set an `OutputLevel` that could be `DEBUG`,
`WARNING` or `INFO` most of the time.

## Initialize and finalize
There are some occasions where we may want to run some code between the
constructor and the `operator()`; that is the place for `initialize()`. There is
also a way of doing something similar after processing with `finalize()`. For that, we
can add to our classes those functions (we can also add only one of these):

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
[LHCb Code Analysis Tools](https://twiki.cern.ch/twiki/bin/view/LHCb/CodeAnalysisTools#Debugging_gaudirun_py_on_Linux_w) (requires a CERN account to view).

## Avoiding const in `operator()`
There is a way of working around `operator()` being const and that is by adding
the keyword `mutable` to our data member. This will allow us to change our data
member inside `operator()` and will cause code that wasn't compiling because of
this to compile. Of course, this is not a good idea because unless the member of
our class is thread-safe, that means that our algorithm is no longer thread-safe
and running with multiple threads can cause different results. Even worse than
that, it's very possible that there are not any errors or crashes but the
results are simply wrong from having several threads changing a member at the
same time, for example.
