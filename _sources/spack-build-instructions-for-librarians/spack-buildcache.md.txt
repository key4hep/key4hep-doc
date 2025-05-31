
# Spack Buildcaches

{% callout "Spack documentation" %}

Buildcaches were investigated, but are no longer supported for Key4hep software, due to the difficulty of relocating some packages.

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

```bash
# key4hep-stack was already installed with 'spack install key4hep-stack'
spack mirror add key4hep /eos/project/k/key4hep/www/key4hep/spack_build/mirror/spackages
spack buildcache create -m key4hep -u -a -f key4hep-stack
```

Since the packages need to be relocated as well as copied, this might take up to an hour.


In order to install packages from the  buildcache, use:

```bash
spack buildcache install -u -a key4hep-stack
```

Spack will then search all added mirrors for `key4hep-stack`.
For read-only access on machines without `eos`, these files are served also over http:


```bash
spack mirror add key4hep-web http://key4hep.web.cern.ch/key4hep/spack_build/mirror/spackages/
```
