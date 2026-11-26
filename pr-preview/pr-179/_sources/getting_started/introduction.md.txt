# Introduction


## Notable stack components

The Key4hep software stack includes a variety of components, featuring both
general-purpose solutions and elements specific to High Energy Physics (HEP). It
integrates well-established HEP libraries like ROOT, Geant4, DD4hep, and Gaudi,
along with components developed specifically to support the stack.

### Event Data Model

The Event Data Model (EDM) defines the structures needed to represent and store
event information. The Key4hep software stack uses a common EDM called
[EDM4hep](https://edm4hep.web.cern.ch), which is used by various stack
components. EDM4hep is implemented with the
[PODIO](https://key4hep.web.cern.ch/podio) data model generator.

### Event Processing Framework

An event processing framework, sometimes also just referred to as *framework*,
allows for defining and orchestrating the execution of complex workflows, such
as event reconstruction, including handling data transformations and their
interdependencies. For its framework, Key4hep adopted Gaudi, a widely used
framework established in experiments like LHCb and ATLAS. To support Gaudi's
integration within the stack, Key4hep provides
[k4FWCore](https://github.com/key4hep/k4FWCore), which enables the use of
EDM4hep in Gaudi based applications.

### Detector description

Key4hep uses the toolkit for detector description.
[DD4hep](https://dd4hep.web.cern.ch) is a well-established tool in the HEP
community, providing a unified approach to describing a detector's geometry,
materials, readout, and calibration.

### Interoperability with iLCSoft

Key4hep draws significant inspiration from iLCSoft, a common software stack
widely used by the linear collider community. To support interoperability and
simplify the transition between the two stacks, several tools have been
developed. Among them,
[k4EDM4hep2LcioConv](https://github.com/key4hep/k4EDM4hep2LcioConv) facilitates
the conversion between EDM4hep and the LCIO data model used in iLCSoft, while
k4MarlinWrapper enables the integration of processors from the iLCSoft framework
with Gaudi-based frameworks.

### Infrastructure

Key4hep uses the [Spack package manager](https://spack.io/) to manage the
compilation and deployment of its packages. Spack allows experiments to share
build recipes, enabling any experiment to build the stack independently or
extend it for their own needs. In addition, the Key4hep stack is also built
centrally and deployed to the CVMFS, from where it can be [easily
accessed](setup.md).


```{note}
We are currently switching the way we build and deploy the Key4hep software
stack. For users this switch will be mostly transparent and for a transition
period the spack basded setup and installation will remain available in
parallel.
```
