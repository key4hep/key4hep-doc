# Using Spack to build Key4HEP software

The [spack](https://spack.io) package manager can be used to build the Key4HEP software stack. It is recommended to build on top of the LCG releases, as otherwise the compilation will be very time-consuming.

Spack can be installed by simply cloning it with git. The spack repository for key4hep packages is installed the same way:

```bash
git clone https://github.com/spack/spack.git
git clone https://github.com/key4hep/k4-spack.git
alias spack='python $PWD/spack/bin/spack'

spack repo add k4-spack

# install the meta-package for the key4hep-stack
spack install key4hep-stack

```
