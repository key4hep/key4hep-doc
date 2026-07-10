# Developing a single package

For quick modifications, such as updating a single package, you can source the stack from cvmfs, compile a local version of the selected package, and export specific environment variables to ensure the local package is used instead of the one from cvmfs.

## Building a local version

All Key4hep software packages can be built using `cmake`. The minimal way to do this at the top level of the package directory:

```sh
cmake -B build -S . -DCMAKE_INSTALL_PREFIX=./install
cmake --build build --target install
```

This assumes that you don't need to pass any additional configuration arguments to `cmake`. It will also install the results into `./install`, which is the conventional place in Key4hep.

If you want to check whether your local version of the package still passes all tests, you can run:

```sh
ctest --test-dir build
```

Building with multiple processes can either be done simply by passing `-G Ninja` to the first `cmake` command, or via passing `-- -j<N>` to the `cmake --build` command at the very end (replace `<N>` by the number of processes you want).

## Adapt the environment with `k4_local_repo`

`k4_local_repo` is a helper command to simplify setting up the environment for single package development. This command becomes available immediately after sourcing the environment. To use it, navigate to the root directory of the package you want to develop and execute the command:

```bash
k4_local_repo [<install_location>]
```
where, `<install_location>` refers to the directory where the package will be installed. If not specified, the default `./install/` directory is assumed. This should match the location specified during cmake configuration with `-DCMAKE_INSTALL_PREFIX=<install_location>`.

Afterwards, the environment will be updated to automatically pick up the installed package.

When working with multiple local packages it might be beneficial to write a helper script to execute `k4_local_repo` for each locally developed package.

## Adapt the environment manually

While the `k4_local_repo` is the preferred method, it's also possible to set up the environment variables manually. To do so, execute the following commands:

```bash
export PATH=<install_location>/bin:$PATH
export LD_LIBRARY_PATH=<install_location>/lib:<install_location>/lib64:$LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH=<install_location>/include:$ROOT_INCLUDE_PATH
export PYTHONPATH=<install_location>/python:$PYTHONPATH
```

where `<install_location>` should match the install location specified during cmake configuration with `-DCMAKE_INSTALL_PREFIX=<install_location>`. It's possible some packages may require specifying some extra environmental variables beside these, for example replacing some libraries with local libraries in `MARLIN_DLL` if needed.

While this approach works and any number of packages can be built this way, it is cumbersome and error-prone to do so for many packages. In such cases using `k4_local_repo` is strongly recommended.

