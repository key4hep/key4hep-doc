
## Setting up Spack


### Downloading a pre-configured instance (lxplus)

On centos7 machines with cvmfs, the easiest way to set up spack is to download a pre-configured instance that is created automatically from the current key4hep/key4hep-spack repository.

```bash
# download spack artifact created by ci --
# pre-configured for key4hep use on lxplus/centos7

curl -L -o spack.tar.gz https://gitlab.cern.ch/key4hep/k4-deploy/-/jobs/artifacts/release/raw/key4hep-spack_centos7-cvmfs.tar.gz?job=setup_spack_push
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

Alternatively, and for other platforms, spack can be configured in a few steps. These steps are essentially what is used to create the pre-configured spack instance in this script: https://github.com/key4hep/key4hep-spack/blob/master/scripts/ci_setup_spack.sh

While this still puts the configuration files in the global scope of spack, it is recommended to use them in an environment, as provided by key4hep-spack.

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

In order to choose the right package versions and build options, spack sometimes needs a few [hints and nudges](https://spack.readthedocs.io/en/latest/build_settings.html). With the new concretizer (default as of spack version 0.17) this should be mostly obsolete.
key4hep-spack ships a spack config file that should give a good build customization out of the box, but can also be customized further. It just needs to be copied to the configuration where spack searches for configurations:

```
cp key4hep-spack/environments/key4hep-common/packages.yaml spack/etc/spack/
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


#### Setting up an upstream compiler

Often it is practical to use a compiler already installed upstream. Spack provides the `spack compiler find` command for this, but the compiler needs to be loaded into the PATH:

```bash
# loading the compiler from upstream
spack load gcc
spack compiler find --scope site
```

Now, the full stack can be installed locally by simply doing:

```bash
# install the meta-package for the key4hep-stack
spack install key4hep-stack
```

