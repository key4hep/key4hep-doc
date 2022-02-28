# Building Key4hep: For Librarians

Key4hep comprises a fairly large number of software and depends on even more externals, so some tooling is needed to efficiently build the whole software stack. The [spack](https://spack.io) package manager can be used to build scientific software at scale, and is part of the Key4hep software R&D program.


A spack install of Key4hep is regularly deployed to `/cvmfs/sw.hsf.org/`, and can be used on lxplus/centos7 just by sourcing the following setup script:

```bash
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```

In this page, the workflow to create this installation is documented.

```eval_rst
.. toctree::
    :caption: Contents:

    spack-setup.md
```


