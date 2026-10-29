# Nightly Builds with Spack


## Usage of the nightly builds on CVMFS

For Centos7, the latest nightly build can be set up by running:

```
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
```

Spack can also be configured to use `/cvmfs/sw-nightlies.hsf.org/spackages` as an upstream installation.

## Technical Information

Nightly builds can be a very useful tool, both to test code correctness and to quickly and automatically deploy the latest developments.
In contrast to the release builds, which use the latest stable version of the individual packages, nightly builds typically use the HEAD of the main development branch.

It is not very efficient to completely rebuild the stack every day, as some packages change fairly infrequently.
The key4hep-spack repository includes some scripts in order to use commit hashes as versions.

