# Using Spack to build Key4HEP software

Key4HEP comprises a fairly large number of software and depends on even more externals, so some tooling is needed to efficiently build the whole software stack. The [spack](https://spack.io) package manager can be used to build scientific software at scale, and is part of the Key4HEP software R&D program.


A spack install of Key4HEP is regularly deployed to `/cvmfs/sw.hsf.org/`, and can be used on lxplus/centos7 just by sourcing the following setup script:

```bash
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```

Using the spack commands can give a more fine-grained control over loaded packages.

## Setting up Spack


### Downloading a pre-configured instance (lxplus)

On centos7 machines with cvmfs, the easiest way to set up spack is to download a pre-configured instance that is created automatically from the current key4hep/key4hep-spack repository.

```bash
curl -L -o spack.tar.gz https://gitlab.cern.ch/key4hep/k4-deploy/-/jobs/artifacts/master/raw/key4hep-spack_centos7-cvmfs.tar.gz?job=build-spack-nightlies
tar xfz spack.tar.gz && rm spack.tar.gz
source spack/share/spack/setup-env.sh
```

This sets up spack with a suitable compiler from cvmfs, the key4hep package recipes and the location of the upstream installation on cvmfs so packages can be installed on top:

```
# list already installed ("upstream") packages
spack find -p
# install a package locally, using suitable upstream packages as dependencies
spack install edm4hep@master
# load individual packages in the environment
spack load cmake
spack load gcc
# load the whole software 
spack load key4hep-stack

```


### Configuring Spack

Alternatively, and for other platforms, spack can be configured in a few steps.

#### Installing Spack
Spack itself is very easy to install -  simply clone the repository with git.

```bash
git clone https://github.com/key4hep/spack.git
source spack/share/spack/setup-env.sh
```

#### Installing the key4hep package recipes

 The spack repository for key4hep packages is installed the same way:

```
git clone https://github.com/key4hep/key4hep-spack.git
spack repo add key4hep-spack
```

### Configuring `packages.yaml`

In order to choose the right package versions and build options, spack sometimes needs a few [hints and nudges](https://spack.readthedocs.io/en/latest/build_settings.html).
key4hep-spack ships a spack config file that should give a good build customization out of the box, but can also be customized further. It just needs to be copied to the configuration where spack searches for configurations:

```
cp key4hep-spack/config/packages.yaml spack/etc/spack/
```


#### Configuring `upstreams.yaml`

The cvmfs installation can be used as an "upstream installation", by adding the following configuration:

```bash
cat <<EOT >> spack/etc/spack/upstreams.yaml
upstreams:
  spack-instance-1:
      install_tree: /cvmfs/sw.hsf.org/spackages/
EOT

```

Alternatively, the full stack can be installed locally by simply doing:

```bash
# install the meta-package for the key4hep-stack
spack install key4hep-stack
```

