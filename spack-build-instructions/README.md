# Using Spack to build Key4HEP software

The [spack](https://spack.io) package manager can be  used to build the Key4HEP software packages.
This is part of a software R&D program, so some parts are still somewhat experimental

A central installation is provided on cvmfs, and can be used without spack by sourcing:

```bash
source /cvmfs/sw.hsf.org/key4hep/views/key4hep-stack-0.1/linux-centos7-broadwell/gcc-8.3.0/setup.sh
```

Using spack can give a more fine-grained control over loaded packages.

Spack can be installed by simply cloning it with git. The spack repository for key4hep packages is installed the same way:

```bash
git clone https://github.com/spack/spack.git
source spack/share/spack/setup-env.sh
git clone https://github.com/key4hep/k4-spack.git

spack repo add k4-spack

```

The cvmfs installation can now be used as an "upstream installation", by adding the following configuration:

```bash
cat <<EOT >> $HOME/.spack/linux/upstreams.yaml
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

### Using a central buildcache

{% callout "Spack documentation" %}

For more information refer to the [spack documentation](https://spack.readthedocs.io/en/latest/binary_caches.html).

{% endcallout %}

It is possible to relocate and  re-use  binaries with the so-called buildcache. 
Some central buildcaches are on the key4hep `eos` space under:

```
/eos/project/k/key4hep/www/key4hep/spack_build/mirror/spackages
```
`spackages` is intended as the central buildcache for key4hep packages built from scratch,
but there exist other buildcaches for packages built against the LCG releases, and rolling builds that are using the branchname `master` or other moving targets.
All packages versioned `package@master` are treated by spack as the same version, even if master points to different commits, thus they must be installed to separate directories, ideally indicating the date.
A buildcache called `contrib` is intended for build tools such as compilers.
Spack automatically creates subdirectory for different platforms and compiler versions.

For write permissions to this space, subscribe to the egroup `cernbox-project-key4hep-writers`.

The following command can be used to put packages into the buildcache:

```
# key4hep-stack was already installed with 'spack install key4hep-stack'
spack mirror add key4hep /eos/project/k/key4hep/www/key4hep/spack_build/mirror/spackages
spack buildcache create -m key4hep -u -a -f key4hep-stack
```

Since the packages need to be relocated as well as copied, this might take up to an hour.




In order to install packages from the  buildcache, use:

```
spack buildcache install -u -a key4hep-stack

```
Spack will then search all added mirrors for `key4hep-stack`.
For read-only access on machines without `eos`, these files are served also over http:


```
spack mirror add key4hep-web http://key4hep.web.cern.ch/key4hep/spack_build/mirror/spackages/
```
