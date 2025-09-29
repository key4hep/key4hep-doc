# Key4hep

Key4hep is a turnkey software stack for detector optimisation and performance studies for future collider experiments. It provides common libraries and solutions for the generation, simulation, reconstruction, and analysis of events at future colliders, with a strong focus on coherence and re-usability in order to reduce duplication of effort and foster collaboration.

## Key Goals
Key4hep aims to:
- **Unify software development** across future collider experiments by providing a common foundation
- **Reduce duplication of effort** through shared libraries and standardized interfaces
- **Enable detector optimization** with comprehensive simulation and reconstruction tools
- **Foster collaboration** between different experimental communities
- **Provide turnkey solutions** that work out-of-the-box for common physics tasks
- **Maintain coherence** across the software stack while allowing experiment-specific customizations
- **Prefer reusing existing solutions** where possible and avoid re-inventing the wheel

## Community and Contributors
Key4hep is a community-driven project that brings together software developers and physicists from multiple future collider experiments. The project benefits from active contributions and adaptations from:
- **FCC** (Future Circular Collider)
- **ILC** (International Linear Collider)
- **CLIC** (Compact Linear Collider)
- **CEPC** (Circular Electron Positron Collider)
- **EIC** (Electron-Ion Collider)
- **Muon Collider**

## Quick Start
New to Key4hep? Start here:
- **[Introduction](getting_started/introduction.md)** - Learn about Key4hep's goals and architecture
- **[Getting Key4hep](getting_started/setup.md)** - Learn how and where Key4hep is available
- **[Getting Help](getting_started/help.md)** - Find support and community resources

Want to contribute? Look at our **[Contribution Guide](getting_started/CONTRIBUTING.md)**.

## Main Documentation Sections
- **[How-to Guides](how-tos/README.md)** - Step-by-step instructions for common tasks
- **[Tutorials](tutorials/README.md)** - Learn Key4hep through hands-on examples
- **[Developer Documentation](developing-key4hep-software/README.md)** - Contribute to and extend Key4hep
- **[Build Instructions](spack-build-instructions-for-librarians/README.md)** - Advanced build and deployment guides

## License
Except where otherwise noted, the example programs and other software provided
by Key4hep are made available under the [OSI](https://opensource.org)-approved [Apache
2.0](https://opensource.org/license/apache-2-0/).

## Acknowledgements

Strategic R&D Programme on Technologies for Future Experiments ([CERN-OPEN-2018-006](https://cds.cern.ch/record/2649646/)) [https://ep-rnd.web.cern.ch/](https://ep-rnd.web.cern.ch/)

European Union's Horizon 2020 Research and Innovation programme under Grant Agreement no. 101004761.

```{eval-rst}
.. toctree::
    :maxdepth: 2
    :caption: Getting Started
    :hidden:

    getting_started/introduction.md
    getting_started/setup.md
    getting_started/help.md
    getting_started/CONTRIBUTING.md

.. toctree::
    :maxdepth: 3
    :caption: User Guides
    :titlesonly:
    :hidden:

    how-tos/README.md
    tutorials/README.md

.. toctree::
    :maxdepth: 3
    :caption: Developer Resources
    :titlesonly:
    :hidden:

    developing-key4hep-software/README.md
    spack-build-instructions-for-librarians/README.md

.. toctree::
    :maxdepth: 2
    :caption: More Information
    :titlesonly:
    :hidden:

    talks-and-presentations/README.md
    call-for-logos/README.md

.. toctree::
    :maxdepth: 2
    :caption: Community Resources
    :titlesonly:
    :hidden:

    FCC software  <https://cern.ch/fccsw>
    CLIC software <https://twiki.cern.ch/twiki/bin/view/CLIC/CLICSoftwareComputing>
    ILC software <https://ilcsoft.desy.de/portal>
    CEPC software <http://cepcsoft.ihep.ac.cn/>
    Muon Collider software <https://mcd-wiki.web.cern.ch/software/>

.. toctree::
   :maxdepth: 1
   :caption: External Resources
   :titlesonly:
   :hidden:
   EDM4hep <https://edm4hep.web.cern.ch>
   podio <https://key4hep.web.cern.ch/podio>
   Gaudi (doxygen) <https://gaudi.web.cern.ch/doxygen/v40r0/index.html>
   Acts <https://acts.readthedocs.io>
```
