# Introduction

## About

Key4hep is a turnkey software stack for detector optimisation and performance studies for future collider experiments. It provides common libraries and solutions for the generation, simulation, reconstruction, and analysis of events at future colliders, with a strong focus on coherence and re-usability in order to reduce duplication of effort and foster collaboration. Key4hep serves as a common software base for future experiments, allowing project-specific adaptations to be made to accommodate their specific requirements.

Key4hep is a community-driven project, with contributions and adaptations from different
future collider projects: CEPC, CLIC, EIC, FCC, ILC, Muon Collider.

## Notable stack components

The Key4hep software stack includes a variety of components, featuring both general-purpose solutions and elements specific to High Energy Physics (HEP). It integrates well-established HEP libraries like ROOT, Geant4, DD4hep, and Gaudi, along with components developed specifically to support the stack.

### Data-model

A data model defines the structures needed to represent and store event information in a persistent store. The key4hep software stack uses a common event data model called EDM4hep, which is used by various stack components. EDM4hep is implemented with the PODIO data model generator.

### Framework

An event-processing application framework allows for defining and orchestrating the execution of complex workflows, such as event reconstruction, including handling data transformations and their interdependencies. For its processing framework, Key4hep adopted Gaudi, a widely used framework established in experiments like LHCb and ATLAS. To support Gaudi's integration within the stack, Key4hep provides k4FWCore, which enables the use of EDM4hep in Gaudi-based applications.

### Detector description

Key4hep uses the DD4hep toolkit for detector description. DD4hep is a well-established tool in the HEP community, providing a unified approach to describing a detector's geometry, materials, readout, and calibration. 

### Interoperability with iLCSoft

Key4hep draws significant inspiration from iLCSoft, a common software stack widely used by the linear collider community. To support interoperability and simplify the transition between the two stacks, several tools have been developed. Among them, k4EDM4hep2LcioConv facilitates the conversion between EDM4hep and the LCIO data model used in iLCSoft, while k4MarlinWrapper enables the integration of processors from the iLCSoft framework with Gaudi-based frameworks.

### Infrastructure

Key4hep uses the Spack package manager to manage the compilation and deployment of its packages. Spack allows experiments to share build recipes, enabling any experiment to build the stack independently or extend it for their own needs. In addition, the Key4hep stack is also built centrally and deployed to the CVMFS, from where it can be [easily accessed](setup.md).

## License

Except where otherwise noted, the example programs and other software provided
by Key4hep are made available under the [OSI](https://opensource.org)-approved [Apache
2.0](https://opensource.org/license/apache-2-0/).

## Acknowledgements
Strategic R&D Programme on Technologies for Future Experiments ([CERN-OPEN-2018-006](https://cds.cern.ch/record/2649646/)) https://ep-rnd.web.cern.ch/   

European Union’s Horizon 2020 Research and Innovation programme under Grant
Agreement no. 101004761.