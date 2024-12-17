
# Setting up Spack


## Downloading a spack instance 

Spack is easy to set up: simply clone the key4hep fork, and use one of the provided spack "environments", that is spack configuration that is created automatically from the current key4hep/key4hep-spack repository.

```bash
git clone https://github.com/spack/spack
git clone https://github.com/key4hep/key4hep-spack
source spack/share/spack/setup-env.sh
source key4hep-spack/environments/key4hep-release-user/setup_clingo_centos7.sh # NOTE: only needed on centos7
spack env activate key4hep-spack/environments/key4hep-release-user # or other environment, see below
```

These instructions assume that a Centos7 machine with a running CVMFS client is used (for other OSs see below). Since Spack cannot bootstrap with the system compiler on Centos7, a setup script for Clingo ( a spack dependency ) is provided.

## Using Spack Environments

The  [spack environments](https://spack.readthedocs.io/en/latest/environments.html) available in `key4hep-spack/environments` bundle the spack configuration, setting up a suitable compiler from cvmfs, the key4hep package recipes, whether to create a view, etc. It is recommended to always use spack in an environment. New environments can be easily created by copying and modifying existing ones, but some use relative links to common configuration files in `key4hep-spack/environments/key4hep-common`, so they should be kept in the `key4hep/environments` directory.

The basic environment is `key4hep-release`, which is used for the central installations and therefore uses `/cvmfs` as install area. `key4hep-debug` is a variation for debug builds. The default compiler is gcc, but an environment that uses clang is provided under `key4hep-release-clang`.
 For local builds that use cvmfs read-only, `key4hep-release-user` can be used.

## Using the key4hep-release-user environment

The key4hep user environment has the `key4hep-stack` bundle package in its spec list. By concretizing it, spack selects the latest compatible versions, re-using installations from cvmfs

```bash
spack concretize -f
spack find # lists the available concretized packages
```

The environment can be installed as is, although this will just install the bundle packages. However, this will create a setup script that can be used to load the software.

```
spack install
```

Custom builds can now be realized, by adding specs to the environment and concretizing together. For example, to build the stack with a local version of EDM4hep:

```
spack add edm4hep@master
git clone https://github.com/key4hep/edm4hep
# make some local changes to edm4hep
spack develop -p $PWD/edm4hep edm4hep@master
spack concretize -f
spack install

```


## Configuring Spack

Alternatively, and for other platforms, spack can be configured in a few steps. These steps are essentially what is used to create the pre-configured spack instance in this script: https://github.com/key4hep/key4hep-spack/blob/master/scripts/ci_setup_spack.sh

While this still puts the configuration files in the global scope of spack, it is recommended to use them in an environment, as provided by key4hep-spack.

### Installing Spack
Spack itself is very easy to install -  simply clone the repository with git.

```bash
git clone https://github.com/spack/spack.git
source spack/share/spack/setup-env.sh
```

### Installing the key4hep package recipes

 The spack repository for key4hep packages is installed the same way:

```
git clone https://github.com/key4hep/key4hep-spack.git
spack repo add key4hep-spack
```

## Configuring `packages.yaml`

In order to choose the right package versions and build options, spack sometimes needs a few [hints and nudges](https://spack.readthedocs.io/en/latest/build_settings.html). With the new concretizer (default as of spack version 0.17) this should be mostly obsolete.
key4hep-spack ships a spack config file that should give a good build customization out of the box, but can also be customized further. It just needs to be copied to the configuration where spack searches for configurations:

```
cp key4hep-spack/environments/key4hep-common/packages.yaml spack/etc/spack/
```



### Configuring `upstreams.yaml`

The cvmfs installation can be used as an "upstream installation", by adding the following configuration:

```bash
cat <<EOT >> spack/etc/spack/upstreams.yaml
upstreams:
  spack-instance-1:
      install_tree: /cvmfs/sw.hsf.org/spackages6/
EOT
```


### Setting up additional compilers

Often it is practical to use a compiler already installed upstream. Spack provides the `spack compiler find` command for this, but the compiler needs to be loaded into the PATH:

```bash
# loading the compiler from upstream
source /cvmfs/sft.cern.ch/lcg/contrib/gcc/11.2.0/x86_64-centos7/setup.sh
spack compiler find --scope site
```

