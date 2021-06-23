

# Getting started with Key4hep software

## Setting up the Key4hep Software Stack

### Using central installations on cvmfs

The following command will set up the pre-installed software on lxplus (or any centos7 machine with cvmfs):

```bash

source /cvmfs/sw.hsf.org/key4hep/setup.sh
```



### Using Virtual Machines or Docker containers

The instructions above should work in any CentOS7 virtual machine or Docker container with `cvmfs` available. We give in the following one example for each of the two cases.

#### CernVM Virtual Appliance

The CernVM project provides a convenient tool to start VMs, [cernvm-launch](https://cernvm.cern.ch/portal/launch), and a [public repository](https://github.com/cernvm/public-contexts) of contexts to be used with `cernvm-launch` to configure the VM at your needs. A context dedicated to Key4hep is available in the repository. The [cernvm-launch](https://cernvm.cern.ch/portal/launch) works with [VirtualBox](https://www.virtualbox.org/), virtualization manager available for free for all platforms.

To create and use a CernVM virtual machine for Key4hep please follow the following steps:

   * Make sure [VirtualBox](https://www.virtualbox.org/) is installed (details installing instructions from the product web page).
   * Download the `cernvm-launch` binary for your platform either from the [dedicated download page](https://ecsft.cern.ch/dist/cernvm/launch/bin/) or from the following links:
      * [Linux](https://fccsw.web.cern.ch/fccsw/utils/vm/cernvm/launch/linux/cernvm-launch)
      * [Mac](https://fccsw.web.cern.ch/fccsw/utils/vm/cernvm/launch/mac/cernvm-launch)

     Make sure is visible in your $PATH.
   * Get the [k4h-dev.context](https://raw.githubusercontent.com/cernvm/public-contexts/master/k4h-dev.context) (use wget or curl)

Once you have all this you can create the VM with this command:
```
$ cernvm-launch create --name k4h-dev --cpus 4 --memory 8000 --disk 20000 k4h-dev.context
```
You an choose how many CPU cores to use, the memory and the disk space. Good rules of thumb are to use half the cores of your machine, at least 2 GB memory per core, and enough disk for your job. The above command should oepn a window with VirtualBox and produce on the screen an output like this
```
Using user data file: k4h-dev.context
Parameters used for the machine creation:
	name: k4h-dev
	cpus: 4
	memory: 8000
	disk: 20000
	cernvmVersion: 2019.06-1
	sharedFolder: /mnt/shared/k4h-dev-vs
```
You see in partcular that your `$HOME` area is shared with the VM, so you can exchange files between the VM and the host machine very conveniently.
From now on you can either work in the VirtualBox window or ssh to the machine with
```
cernvm-launch ssh k4h-dev
```
In either case you need a user name and password, which by default are `k4huser` and `pass`; these can be changed in the `k4h-dev.context` file.

To enable graphics you need to find out the port on which the VM responds and use `ssh -Y -P <port> fccuser@localhost`. For example
```
$ cernvm-launch list
k4h-dev`:	CVM: 2019.06-1	port: 36998
...
$ ssh -Y -P 36998 k4huser@localhost
The authenticity of host '[localhost]:36998 ([127.0.0.1]:36998)' can't be established.
ECDSA key fingerprint is SHA256:JXjpOzSu7vIwgEDxc8s/fdDJv4gQs2SUjnbMnEZsaYI.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[localhost]:36998' (ECDSA) to the list of known hosts.
k4huser@localhost's password:
[k4huser@localhost ~]$
```
(you can safely ignore warnings about setting LC_CTYPE).
Graphics should of course work well if you choose to work in the VirtualBox window.

The `cernvm-launch` also supports listing, stopping, starting virtual machines. Please run `cernvm-launch -h` for all the available options.


