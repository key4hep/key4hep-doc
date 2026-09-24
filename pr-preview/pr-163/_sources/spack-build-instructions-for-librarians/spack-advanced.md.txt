
# Spack Usage and Further Technical Topics

This page collects a few known workarounds for issues and areas of development in spack. 
Check also the issues in [key4hep-spack](https://github.com/key4hep/key4hep-spack/issues) for up-to-date information. 
Additionally, we also provide a few more advanced invocations of `spack` commands that allow a certain degree of debugging of the decisions spack has made when installing a given package and its dependencies.

## Checking which packages will be newly installed

When installing a package it might be interesting to estimate how long it will take to do so.
An important proxy for this is how many and which dependencies spack will install in order to build a package.
This can be done with the `spack solve` command, which invokes the concretizer and then spits out the solution that would be installed if the same arguments were passed to `spack install`, e.g.

```bash
spack solve -I
```
```console
==> Best of 12 considered solutions.
==> Optimization Criteria:
  Priority  Criterion                                            Installed  ToBuild
  1         number of input specs not concretized                        -        0
  2         number of packages to build (vs. reuse)                      -        4
  3         requirement weight                                           0        0
  4         deprecated versions used                                     1        0
  5         version weight                                               0        0
  6         number of non-default variants (roots)                       0        0
  7         preferred providers for roots                                0        0
  8         default values of variants not being used (roots)            0        0
  9         number of non-default variants (non-roots)                   3        0
  10        preferred providers (non-roots)                              0        0
  11        compiler mismatches                                          0        0
  12        OS mismatches                                                0        0
  13        non-preferred OS's                                           0        0
  14        version badness                                            156        0
  15        default values of variants not being used (non-roots)        1        0
  16        non-preferred compilers                                      0        0
  17        target mismatches                                            0        0
  18        non-preferred targets                                      165       44

 -   whizard@3.0.3%gcc@10.3.0~fastjet~latex~lcio~lhapdf~openloops~openmp+pythia8 hepmc=3 arch=linux-ubuntu20.04-x86_64
[+]      ^hepmc3@3.2.4%gcc@10.3.0~interfaces~ipo~python~rootio build_type=RelWithDebInfo arch=linux-ubuntu20.04-x86_64
[+]          ^cmake@3.16.3%gcc@10.3.0~doc+ncurses+ownlibs~qt build_type=RelWithDebInfo patches=1c54004,bf695e3 arch=linux-ubuntu20.04-x86_64
 -       ^libtirpc@1.2.6%gcc@10.3.0 arch=linux-ubuntu20.04-x86_64
 -           ^krb5@1.19.3%gcc@10.3.0+shared arch=linux-ubuntu20.04-x86_64
[+]              ^bison@3.8.2%gcc@10.3.0 arch=linux-ubuntu20.04-x86_64
[+]                  ^diffutils@3.8%gcc@10.3.0 arch=linux-ubuntu20.04-x86_64
[+]                      ^libiconv@1.16%gcc@10.3.0 libs=shared,static arch=linux-ubuntu20.04-x86_64
[+]                  ^m4@1.4.18%gcc@10.3.0+sigsegv patches=3877ab5,fc9b616 arch=linux-ubuntu20.04-x86_64
[+]                  ^perl@5.30.0%gcc@10.3.0~cpanm+shared+threads arch=linux-ubuntu20.04-x86_64
[+]              ^gettext@0.21%gcc@10.3.0+bzip2+curses+git~libunistring+libxml2+tar+xz arch=linux-ubuntu20.04-x86_64
[+]                  ^bzip2@1.0.8%gcc@10.3.0~debug~pic+shared arch=linux-ubuntu20.04-x86_64
[+]                  ^libxml2@2.9.13%gcc@10.3.0~python arch=linux-ubuntu20.04-x86_64
[+]                      ^pkgconf@1.8.0%gcc@10.3.0 arch=linux-ubuntu20.04-x86_64
[+]                      ^xz@5.2.5%gcc@10.3.0~pic libs=shared,static arch=linux-ubuntu20.04-x86_64
[+]                      ^zlib@1.2.12%gcc@10.3.0+optimize+pic+shared patches=0d38234 arch=linux-ubuntu20.04-x86_64
[+]                  ^ncurses@6.2%gcc@10.3.0~symlinks+termlib abi=none arch=linux-ubuntu20.04-x86_64
[+]                  ^tar@1.30%gcc@10.3.0 zip=pigz arch=linux-ubuntu20.04-x86_64
[+]              ^openssl@1.1.1f%gcc@10.3.0~docs~shared certs=mozilla arch=linux-ubuntu20.04-x86_64
 -       ^ocaml@4.13.1%gcc@10.3.0+force-safe-string arch=linux-ubuntu20.04-x86_64
[+]      ^pythia8@8.306%gcc@10.3.0~evtgen~fastjet~hdf5+hepmc+hepmc3~lhapdf~madgraph5amc~mpich~openmpi~python~rivet~root+shared arch=linux-ubuntu20.04-x86_64
[+]          ^hepmc@2.06.11%gcc@10.3.0~ipo build_type=RelWithDebInfo length=MM momentum=GEV arch=linux-ubuntu20.04-x86_64
[+]          ^rsync@3.1.3%gcc@10.3.0 arch=linux-ubuntu20.04-x86_64
```

The `-I` flag shows which packages are alrady installed.
`spack solve` also shows some information about all the things that were considered during concretization. It can also be used to dump more information on the concretization process.
Unfortunately, this information is rather hard to parse, and still a work in progress from the spack developers.


## Requiring certain variants globally

spack can be configured using some [configuration
files](https://spack.readthedocs.io/en/latest/configuration.html). Specifically
using `packages.yaml` which is read from the user directory, i.e. `~/.spack` (or
`/.spack/linux`) can be used to enforce the value of certain default variants
globally. To solve the above problem it is enough to put the following into
`packages.yaml`:

```yaml
packages:
  all:
  variants: cxxstd=17
  ```

It is still possible to override this for certain packages either by
individually configuring them in `packages.yaml` or via the command line which
take precedence over all configuration files.

In the Key4hep software stack build recipes for releases, we use the same mechanism, as this configuration is also available from spack environments.


## System Dependencies

Some spack packages have *external find* support. For these packages it is possible to let spack detect the variants and versions for system (or otherwise) installed packages.
For such cases use the `spack external find` command. It has to be noted that detecting external packages and using them does not always work perfectly.


## Target Architectures

Since HEP software is usually deployed on a variety of machines via cvmfs, installations need to pick a target architecture. `broadwell` is for now the default choice, and can be set with:

```
packages:
  all:
    target: [broadwell]
```

in `$HOME/.spack/linux/packages.yaml`




## Bundle Packages and Environments

Right now, key4hep is installed via a `BundlePackage`, that depends on all other relevant packages.
An alternative would be to use [spack environments](https://spack-tutorial.readthedocs.io/en/latest/tutorial_environments.html). This alternative is still under investigation.


## Setting Up Runtime Environments 

The simplest way to set the environment to use spack installed packages is to use the `spack load` command.
In order for users not to have to set up spack when it is not needed, the `key4hep-stack` bundle package includes a script that will automatically generate a bash setup script and install it into its prefix.

Spack can also create "filesystem views" of several packages, resulting in a directory structure similar what you would find in `/usr/local`.
This simplifies library and include paths, but the setup generation for views still has to be developed.

## Compiler Dependencies and Data Packages

Some HEP packages (like `geant4-data`) consist only of data files, and can thus be used on any platform.
Spack cannot yet handle this gracefully, but an ongoing development tries to treat compilers as dependencies, which would help with re-using data packages.


## Duplicating Recipes in Downstream Repositories

Although it is possible to "patch" spack build recipes by overriding them in another repository (key4hep-spack, for example), this is discouraged.
The central repo is one of the strenghts of spack, with many contributors ensuring that packages build smoothly.
Also, packages are installed in different namespaces, so it is not possible to deprecate changed recipes and use the upstream ones without re-installing the packages.


## CVMFS Installation Workflow

The distribution on cvmfs is an exact copy of the spack installation on the build machine, just copied with this rsync command on the publisher:

```
rsync -axv --inplace --delete    --verbose -e "ssh -T  -o Compression=no -o StrictHostKeyChecking=no -o GSSAPIAuthentication=yes -o GSSAPITrustDNS=yes" user@build-machine:/cvmfs/sw.hsf.org/spackages/ /cvmfs/sw.hsf.org/spackages/
```

The `--delete` option can be omitted in order to preserve already installed packages, regardless of the state of the build machine.



## Compiler Wrappers

Spack uses compiler wrappers instead of exposing the actual compilers during the build.
For packages like whizard, which register the compiler path to use during runtime, this will not work, as the wrappers are not available at runtime.
For these packages, the current workaround is to force spack to use the actual compilers during build (see the build recipe of `whizard`).


## Spack-Installed LCG releases

A spack installation that contains all packages in the LCG releases is work in progress, see https://gitlab.cern.ch/sft/sft-spack-repo.

## Using Spack-installed GCC

When installing gcc with spack, it is necessary to add a `cc` symlink to `$PATH`, in order to avoid errors with cling, see https://github.com/spack/spack/issues/17488.



