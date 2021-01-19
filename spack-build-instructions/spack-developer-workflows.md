# Spack workflows for developing Key4HEP software

Using spack to develop software is somewhat pushing its intended usage to its limits.
However, it is not impossible and this is an area of spack that is currently under active development.
Unfortunately, this also means that the spack documentation might not be fully up-to-date on these topics.
Hence, this page tries to collect some of the experiences the Key4HEP developers have made.

## Developing a single package

When only developing on a single package it is possible to use the [`dev-build`](https://spack.readthedocs.io/en/latest/command_index.html#spack-dev-build) command of spack.
A brief tutorial can be found in [the spack documentation](https://spack-tutorial.readthedocs.io/en/lanl19/tutorial_developer_workflows.html).
There is also a dedicated channel on slack (https://spackpm.herokuapp.com/) where questions regarding the development workflow can be discussed. 
It allows to build a given package directly from local sources in the same way as spack does it, and even makes this package available to other packages in the same way it does packages that have been installed by spack directly.
Here we will use [LCIO](https://github.com/iLCSoft/LCIO) as an example since it can be installed without (or with only one) dependency.

As a first step let's have a look at what installing `lcio` with spack would entail. 
Note that we explicitly disable the ROOT dictionaries in order to limit the number of dependencies
```bash
spack spec -Il lcio ~rootdict
```
```
Input spec
--------------------------------
 -   lcio~rootdict

Concretized
--------------------------------

 -   vdwx2aq  lcio@2.16%gcc@9.3.0~examples~ipo~jar~rootdict build_type=RelWithDebInfo cxxstd=17 arch=linux-ubuntu20.04-skylake
[+]  utzbuq7      ^cmake@3.16.3%gcc@9.3.0~doc+ncurses+openssl+ownlibs~qt patches=1c540040c7e203dd8e27aa20345ecb07fe06570d56410a24a266ae570b1c4c39,bf695e3febb222da2ed94b3beea600650e4318975da90e4a71d6f31a6d5d8c3d arch=linux-ubuntu20.04-skylake
[+]  pljbs5a      ^sio@0.0.4%gcc@9.3.0+builtin_zlib~ipo build_type=RelWithDebInfo cxxstd=17 arch=linux-ubuntu20.04-skylake

```

In this configuration `lcio` has only two dependencies, `sio` and `cmake`, which are both already installed in this case.
If these dependencies are not yet installed, spack will automatically install them for you when using the `dev-build` command.

### Installing a local version with `dev-build`

In order to install a local version of LCIO with spack, first we have to clone it into a local directory
```bash
git clone https://github.com/iLCSoft/LCIO
```

Now we can install this local version via
```bash
cd LCIO
spack dev-build lcio@master ~rootdict
```
This should install `lcio` and all dependencies that are not yet fulfilled, giving you the full output of all the build stages ending on something like the following
```
...
==> lcio: Successfully installed lcio-master-7dovpqn3kscbg672ham5wcqro7lg45gh
  Fetch: 0.00s.  Build: 1.62s.  Total: 1.62s.
[+] /home/tmadlener/work/spack/opt/spack/linux-ubuntu20.04-skylake/gcc-9.3.0/lcio-master-7dovpqn3kscbg672ham5wcqro7lg45gh
```

Note, that it is necessary to specify a single concrete version here for `lcio`. We use `@master`.
This version has to be one that is already available for the package (use `spack info` to find out which ones are available) and cannot be an arbitrary version.
It also does not necessarily have to correspond to the actual version of the source code you are currently installing. 
However, it is of course encouraged to use a meaningful version specifier, since this package should also be useable as desired by dependent packages.

### Using the local version as dependency

Now that the local version has been installed, it would of course be nice to be able to use it in downstream packages as well.
Spack doesn't pick package versions installed from local sources by default, but as with any other package it is possible to require a specific version of a dependency.
This is described in a bit more detail [here](https://key4hep.github.io/key4hep-doc/spack-build-instructions/spack-advanced.html#concretizing-before-installation).

Let's first find out how the version that we have just installed looks like
```bash
spack find -lv lcio
```
which will yield something similar to
```
==> 1 installed package
-- linux-ubuntu20.04-skylake / gcc@9.3.0 ------------------------
7dovpqn lcio@master~examples~ipo~jar~rootdict build_type=RelWithDebInfo cxxstd=17 dev_path=/home/tmadlener/work/ILCSoft/LCIO
```
As you can see the local path from which this version was installed has become part of the spec for the installed package (the `dev_path=...` part of the spec above).
Hence, also the hash is affected by the fact that it has been built from a local source.

### More advanced usage
Note: If you have installed lcio following the description above you might have to uninstall it again first to follow these instructions, because spack will not overwrite an already installed package.

The above instructions only dealt with installing a package from a local source, but not how to easily get a development environment allowing for a quick edit, compile cycle.
This can be achieved by using the `--drop-in` and the `--before`/`--until` arguments of the `dev-build` command:

```bash
spack dev-build --drop-in bash --until cmake lcio@master ~rootdict
```

This command will first install all necessary dependencies, then run the install process for `lcio` until **after** the `cmake` stage and then drop you into a new bash shell with the proper build environment setup.
It will also setup a build folder, which follows the naming scheme `spack-build-${hash}`, in this case: `spack-build-7dovpqn`.
To compile `lcio` simply go into this directory and run `make` in there
```bash
cd spack-build-7dovpqn
make -j4
```
You are now in an environment where you can easily edit the local source code and re-compile afterwards.

Once all the development is done, it is still necessary to install everything to the appropriate location.
This installation has to be registered in the spack database as well. Hence, simply calling `make install` in the build directory will not do the trick.
Another call to `dev-build` is necessary.
```bash
cd .. # go back to the source directory where you started
spack dev-build lcio@master ~rootdict
```
This will run the whole chain again, but it will not overwrite the build directory.
Hence, it will not recompile everything again, but simply install all the build artifacts to the appropriate location.
`spack find -lv lcio` can be used to check if the installation was successful.

**NOTE: You are probably still in the build environment at this stage. To return back to you original shell simply type `exit`.**

## Developing multiple packages or dependencies of other packages

Developing on many packages simultaneously using the `dev-build` command can become cumbersome and doesn't really scale.

### Using an environment to setup all dependencies
One way to develop on multiple packages simultaneously can be to setup an [environment](https://spack.readthedocs.io/en/latest/environments.html) that contains the dependencies of all packages.

As an example the following definition of an environment has been used to develop on
[`podio`](https://github.com/AIDASoft/podio), [`EDM4HEP`](https://github.com/key4hep/EDM4HEP) and some other packages.
```yaml
spack:
  specs:
    - python
    - root@6.20.04 +davix+gsl+math~memstat+minuit+mlp~mysql+opengl~postgres~pythia6+pythia8+python~qt4+r+root7+rootfit+rpath~shadow+sqlite+ssl~table+tbb+threads+tmva+unuran+vc+vdt+vmc+x+xml+xrootd build_type=RelWithDebInfo cxxstd=17 patches=22af3471f3fd87c0fe8917bf9c811c6d806de6c8b9867d30a1e3d383a1b929d7
    - dd4hep +geant4
    - geant4
    - heppdt
    - hepmc@2.06.10
    - tricktrack
    - py-pyyaml
    - py-jinja2
    - cmake
    - pythia8
    - evtgen
  concretization: together
  view: true
  packages:
    all:
      compiler: [gcc@9.3.0]
      variants: cxxstd=17
```

Assuming this is the content of `edm4hep_devel.yaml` an environment can be created, activated, concretized and installed with the following commands:
```bash
spack env create edm4hep-devel edm4hep_devel.yaml
spack env activate -p edm4hep-devel
spack concretize
spack install
```

After an environment has been installed, it can easily be activated via
```bash
spack env activate -p edm4hep-devel
```
which immediately drops you in an environment with all the packages stated in the environment file above available and properly set up. 
Developing packages that depend on these should then be straight forward, especially for properly setup CMake based projects that can automatically find and configure their dependencies.

The disadvantage of this approach is that the packages you want to develop on have to be on the top of the stack and if they depend on each other, you still have to properly handle these dependencies on your own.

### Environments and a development workflow

Recently spack gained the ability to setup environments and specify multiple packages that you would like to develop on (See [spack/spack#256](https://github.com/spack/spack/pull/15256)).
It is not yet really documented and it is not yet fully optimized, but it allows for a decent development experience if your package is not too deep down in the stack.
It is not impossible to develop on packages deep down the software stack, but this can imply frequently recompiling large parts of the software stack, since spack does not yet handle this in the best way, but instead builds all packages that you are not developing on from scratch. Hence, even if a simple relinking would have done the trick, spack will still build a lot of packages again.
Nevertheless, the feature is in a usable state and this section briefly describes how to use it.
Especially if you mainly develop on one package but sometimes want to check whether the rest of the stack, that depends on this package still compiles with the latest version, this can be a very useful workflow.

As an example we will be using the `k4simdelphes` package that depends on `edm4hep`, which in turn depens again on `podio`. 
Suppose we want to change `podio` and `edm4hep` and see if `k4simdelphes` still compiles and works.
We would then use an environment definition file similar to the usual environments. For this example it has the following content
```yaml
spack:
  spec: 
    - k4simdelphes
  concretization: together
  view: false
  packages:
     all:
       compiler: [gcc@9.3.0]
       variants: cxxstd=17
  develop:
    podio:
      spec: podio@master +sio
      path: ../../../../../podio
    edm4hep:
      spec: edm4hep@master
      path: ../../../../../EDM4hep
```

The first part is the same as previously, but a new `develop` section containing information about the packages that should be developed on has been added.
For each package there is a `spec` and a `path` field. The `spec` field tells spack which spec to build, while the `path` field tells spack where the source files are located. 
**The path is relative to the `$(prefix)/var/spack/environments/${environment-name}` directory or an absolute path.**

Assuming that you are currently in the directory that contains local `spack` installation, the following steps are necessary to create the development environment
```bash
git clone https://github.com/AIDASoft/podio
git clone https://github.com/key4hep/EDM4hep
spack env create my-development-env development_env_packages.yaml
```
where `development_env_packages.yaml` is the yaml file with the contents just described above.

It is now possible to activate this environment via
```bash
spack env activate -p my-development-env
```

To install all the packages, including the local versions of `podio` and `edm4hep` it is now enough to simply do `spack install`**in the activated environment**.
This will build your local copies of `podio` and `edm4hep` and use these versions as dependencies for the `k4simdelphes` package.
Changes can also be made to either of the two packages.
To compile only one package without installing it yet, it is easiest to simply go to the directory where the sources are.
There should now be a few spack related files and a spack build folder among the other source files
```
[...]
spack-configure-args.txt
spack-build-env.txt
spack-build-out.txt
spack-build-${hash}
```
Here `${hash}` is the same that you get from `spack find -l package`.
After you have done all the necessary changes you can simply change into this build directory and run `make` to compile the package again.
Once all your development is done and you want to install the package `spack install` will run the whole build chain again.
This means that all the (local) development packages in your environment will only be recompiled as far as necessary, while all other packages that depend on the development packages will be re-built from scratch.

Once you are done developing, this environment can be used like any other environment simply by running `spack env activate my-development-env` to activate it.

#### Adding another package to develop
If you now realize that your changes to `podio` or `edm4hep` broke `k4simdelphes` and you need to also implement some changes there, you do not have to define a new environment.
Instead it is possible to add `k4simdelphes` to the `develop` section via `spack develop` (assuming you are still in the activated environment and in the same directory where also the `podio` and `edm4hep` sources live)
```bash
git clone https://github.com/key4hep/k4SimDelphes
spack develop --no-clone --path ../../../../../k4SimDelphes k4simdelphes@main
```
Here, the `--path` is again either relative to the environment directory inside spack. It could also be an absolute path.
You now have to concretize the environment again before you can install the packages.
```bash
spack concretize -f
spack install
```

Now you can work on `k4simdelphes` in the same way as you can for `podio` or `edm4hep`.
You can also check that the environment now indeed uses your local version of `k4simdelphes` via
```
spack find -lv k4simdelphes
```
which should now yield something along the lines of
```
==> In environment my-development-env
==> Root specs
------- k4simdelphes@main 

==> 1 installed package
-- linux-ubuntu20.04-broadwell / gcc@9.3.0 ----------------------
m5khm2w k4simdelphes@main~ipo build_type=RelWithDebInfo dev_path=/home/tmadlener/work/spack/var/spack/environments/test-devel-env/../../../../../k4SimDelphes
```
where the path to the local source files has now again become part of the spec as can be seen by the `dev_path=...` part of the spec.
