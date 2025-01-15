# Developing a single package

For quick modifications, such as updating a single package, you can source the stack from cvmfs, compile a local version of the selected package, and export specific environment variables to ensure the local package is used instead of the one from cvmfs.

## With `k4_local_repo`

`k4_local_repo` is a helper command to simplify setting up the environment for single package development. This command becomes available immediately after sourcing the environment. To use it, navigate to the root directory of the package you want to develop and execute the command:

```bash
k4_local_repo <install_location>
```

where `<install_location>` refers to the location where the package will be installed. This should match the one specified during cmake configuration with `-DCMAKE_INSTALL_PREFIX=<install_location>`.

Afterwards, the environment will be updated to automatically pick up the installed package.

## Manually

While the `k4_local_repo` is the preferred method, it's also possible to set up the environment variables manually. To do so, execute the following commands:

```bash
export PATH=<install_location>/bin:$PATH
export LD_LIBRARY_PATH=<install_location>/lib:<install_location>/lib64:$LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH=<install_location>/include:$ROOT_INCLUDE_PATH
export PYTHONPATH=<install_location>/python:$PYTHONPATH
```

where `<install_location>` should match the install location specified during cmake configuration with `-DCMAKE_INSTALL_PREFIX=<install_location>`. It's possible some packages may required specifying some extra environmental variables beside these.

## Limitations

While this approach works and any number of packages can be built this way, it is cumbersome to do so for many packages, as one has to repeat the cycle of configuring, building, and installing and then exporting the environment variables as many times as packages are installed. It is possible to miss packages, and then the cvmfs version will be used instead of the local one without notice. It's also cumbersome to reproduce the environment at a later time.
