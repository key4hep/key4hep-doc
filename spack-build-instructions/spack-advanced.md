
# Spack Usage and Further Technical Topics

This page collects a few known workarounds for issues and areas of development in spack.
Check also the issues in [k4-spack](https://github.com/key4hep/k4-spack/issues) for up-to-date information.





## Concretizing before Installation

Spack often needs to be forced to use existing packages as dependencies when installing a new package.
The best way to make sure that spack does not unnecessarily re-install is to 'preview' what will be installed with the command:

```bash
spack spec -I whizard
```

```bash

Input spec
--------------------------------
 -   whizard

Concretized
--------------------------------
 -   whizard@3.0.0_alpha%gcc@9.3.0~fastjet+hepmc~latex~lcio~lhapdf~openmp+pythia8 arch=linux-ubuntu20.04-broadwell
[+]      ^hepmc@2.06.10%gcc@9.3.0 build_type=RelWithDebInfo arch=linux-ubuntu20.04-broadwell
[+]          ^cmake@3.16.3%gcc@9.3.0~doc+ncurses+openssl+ownlibs~qt patches=1c540040c7e203dd8e27aa20345ecb07fe06570d56410a24a266ae570b1c4c39 arch=linux-ubuntu20.04-broadwell
 -       ^ocaml@4.10.0%gcc@9.3.0+force-safe-string arch=linux-ubuntu20.04-broadwell
[+]          ^ncurses@6.2%gcc@9.3.0~symlinks+termlib arch=linux-ubuntu20.04-broadwell
[+]              ^pkgconf@1.7.3%gcc@9.3.0 arch=linux-ubuntu20.04-broadwell
[+]      ^pythia8@8244%gcc@9.3.0~evtgen~fastjet+hepmc~root+shared arch=linux-ubuntu20.04-broadwell
[+]          ^rsync@3.1.3%gcc@9.3.0 arch=linux-ubuntu20.04-broadwell
[+]              ^popt@1.16%gcc@9.3.0 arch=linux-ubuntu20.04-broadwell
[+]              ^zlib@1.2.11%gcc@9.3.0+optimize+pic+shared arch=linux-ubuntu20.04-broadwell


```
In this example, you could check for an existing `ocaml` installation and use it via its hash:

```bash

spack find -l ocaml
```

```bash

==> 2 installed packages
-- linux-centos7-broadwell / gcc@8.3.0 --------------------------
2aolgjw ocaml@4.08.1  ycqhz3l ocaml@4.10.0
```

```bash

spack spec -I whizard ^/ycqhz3l

--------------------------------
 -   whizard@3.0.0_alpha%gcc@9.3.0~fastjet+hepmc~latex~lcio~lhapdf~openmp+pythia8 arch=linux-ubuntu20.04-broadwell
[+]      ^hepmc@2.06.10%gcc@9.3.0 build_type=RelWithDebInfo arch=linux-ubuntu20.04-broadwell
[+]          ^cmake@3.16.3%gcc@9.3.0~doc+ncurses+openssl+ownlibs~qt patches=1c540040c7e203dd8e27aa20345ecb07fe06570d56410a24a266ae570b1c4c39 arch=linux-ubuntu20.04-broadwell
[+]       ^ocaml@4.10.0%gcc@9.3.0+force-safe-string arch=linux-ubuntu20.04-broadwell
[+]          ^ncurses@6.2%gcc@9.3.0~symlinks+termlib arch=linux-ubuntu20.04-broadwell
[+]              ^pkgconf@1.7.3%gcc@9.3.0 arch=linux-ubuntu20.04-broadwell
[+]      ^pythia8@8244%gcc@9.3.0~evtgen~fastjet+hepmc~root+shared arch=linux-ubuntu20.04-broadwell
[+]          ^rsync@3.1.3%gcc@9.3.0 arch=linux-ubuntu20.04-broadwell
[+]              ^popt@1.16%gcc@9.3.0 arch=linux-ubuntu20.04-broadwell
[+]              ^zlib@1.2.11%gcc@9.3.0+optimize+pic+shared arch=linux-ubuntu20.04-broadwell

```

This 'concretizer' is one of the areas of development in spack, so the commands might frequently change or the behaviour differ from what is described here.



### Working around spack concretizer problems

Currently the default settings for some of the packages here do not work due to
known [short comings of the spack
concretizer](https://spack.readthedocs.io/en/latest/known_issues.html#variants-are-not-properly-forwarded-to-dependencies).
For example `spack install K4FWCore` will most probably fail with the following error

```
1. "cxxstd=11" conflicts with "root+root7" [root7 requires at least C++14]
```

Instead of fixing all the packages to deal with these issues, one of the
following workarounds can be used. The issues in spack are planned to be fixed
with the next spack release which would hopefully make these obsolete.

#### Requiring a specific package version

The simplest solution to the above problem is to simply require a `root` version
with the appropriate requirements, e.g.

```bash
spack install K4FWCore ^root cxxstd=17
```

will tell spack to use `cxxstd=17` also for building `root` and get rid of the
conflict above. If using this, make sure to use the same value for `cxxstd` for
`K4FWCore` and `root`.

#### Requiring certain variants globally

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





## System Dependencies

Although spack can use externally installed packages (and even automatically find them), this is strongly discouraged.
This is because the dependency resolution may not work as intended, and changes to the external packages can break the installation


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
An alternative would be to use [spack environments](https://spack-tutorial.readthedocs.io/en/latest/tutorial_environments.html#creating-and-activating-environments). This alternative is still under investigation.


## Setting Up Runtime Environments 

Spack can create "filesystem views" of several packages, resulting in a directory structure similar what you would find in `/usr/local`.
However, there is no good way to set up the runtime environments for the packages installed there -- an issue that should be adressed in spack.

The setup scripts on cvmfs are created by manually editing `spack load --sh gcc > setup.sh; spack load --sh key4hep-stack >> setup.sh` so that the user environment is left intact.

## Compiler Dependencies and Data Packages

Some HEP packages (like `geant4-data`) consist only of data files, and can thus be used on any platform.
Spack cannot yet handle this gracefully, but an ongoing development tries to treat compilers as dependencies, which would help with re-using data packages.


## Duplicating Recipes in Downstream Repositories

Although it is possible to "patch" spack build recipes by overriding them in another repository (k4-spack, for example), this is discouraged.
The central repo is one of the strenghts of spack, with many contributors ensuring that packages build smoothly.
Also, packages are installed in different namespaces, so it is not possible to deprecate changed recipes and use the upstream ones without re-installing the packages.


## CVMFS Installation Workflow

The distribution on cvmfs is an exact copy of the spack installation on the build machine, just copied with this rsync command on the publisher:

```
rsync -axv --inplace --delete    --verbose -e "ssh -T  -o Compression=no -o StrictHostKeyChecking=no -o GSSAPIAuthentication=yes -o GSSAPITrustDNS=yes" user@build-machine:/cvmfs/sw.hsf.org/spackages/ /cvmfs/sw.hsf.org/spackages/
```



## Compiler Wrappers

Spack uses compiler wrappers instead of exposing the actual compilers during the build.
For packages like whizard, which register the compiler path to use during runtime, this will not work, as the wrappers are not available at runtime.
For these packages, the current workaround is to force spack to use the actual compilers during build (see the build recipe of `whizard`).


## Nightly Builds and Using Git Commits as Versions

Spack can build specific git commits and branches, but only if they are mentioned explicitly in the recipe.
Branches like "master" do not point to the latest commit, so `package@master` will not be re-installed if master changes.
Nightly builds can still be done with spack


## Spack-Installed LCG releases

A spack  install of the whole lcg release is work in progress, see https://gitlab.cern.ch/sft/sft-spack-repo.



