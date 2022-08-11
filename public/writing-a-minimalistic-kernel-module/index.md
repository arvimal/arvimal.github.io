# Writing a minimalistic kernel module in Linux - Part 1

<!--more-->
## Introduction

_**L**_oadable Kernel Modules (LKM) are object code that can be loaded into memory, often used for supporting hardware or enable specific features. Kernel modules enable the core kernel to be minimal and have features to be loaded as required.

A kernel module is a normal file usually suffixed with `.ko` denoting it's a kernel object file. It contains compiled code from one or more source files, gets linked to the kernel when loaded, and runs in kernel space. It can dynamically adds functionality to a running kernel, without requiring a reboot.

Linux kernel modules are written in C (not sure if anything else like C++ is possible), and is compiled for a specific kernel version. This is the ideal practice since kernel data structures may change across versions, and using a module compiled for a specific version may break for another.

Since kernel modules can be loaded and unloaded at will, it is pretty easy to unload an older version and load a newer one. This helps immensely in testing out new features since it is easy to change the source code, re-compile, unload the older version, load the newer version, and test the functionality.

## Structure

Modules are expected to be under `/lib/modules/$(uname -r)/` within directories specified according to use case.

\[code language="bash"\] \[root@centos7 3.10.0-514.26.2.el7.x86\_64\]# ls -l total 2940 lrwxrwxrwx. 1 root root 43 Jul 8 05:10 build -> /usr/src/kernels/3.10.0-514.26.2.el7.x86\_64 drwxr-xr-x. 2 root root 6 Jul 4 11:17 extra drwxr-xr-x. 12 root root 128 Jul 8 05:10 kernel -rw-r--r--. 1 root root 762886 Jul 8 05:11 modules.alias -rw-r--r--. 1 root root 735054 Jul 8 05:11 modules.alias.bin -rw-r--r--. 1 root root 1326 Jul 4 11:17 modules.block -rw-r--r--. 1 root root 6227 Jul 4 11:15 modules.builtin -rw-r--r--. 1 root root 8035 Jul 8 05:11 modules.builtin.bin -rw-r--r--. 1 root root 240071 Jul 8 05:11 modules.dep -rw-r--r--. 1 root root 343333 Jul 8 05:11 modules.dep.bin -rw-r--r--. 1 root root 361 Jul 8 05:11 modules.devname -rw-r--r--. 1 root root 132 Jul 4 11:17 modules.drm -rw-r--r--. 1 root root 110 Jul 4 11:17 modules.modesetting -rw-r--r--. 1 root root 1580 Jul 4 11:17 modules.networking -rw-r--r--. 1 root root 90643 Jul 4 11:15 modules.order -rw-r--r--. 1 root root 89 Jul 8 05:11 modules.softdep -rw-r--r--. 1 root root 350918 Jul 8 05:11 modules.symbols -rw-r--r--. 1 root root 432831 Jul 8 05:11 modules.symbols.bin lrwxrwxrwx. 1 root root 5 Jul 8 05:10 source -> build drwxr-xr-x. 2 root root 6 Jul 4 11:17 updates drwxr-xr-x. 2 root root 95 Jul 8 05:10 vdso drwxr-xr-x. 2 root root 6 Jul 4 11:17 weak-updates \[/code\]

As we can see, there are several files that deals with the inter-dependencies of modules, which is used by `modprobe` to understand which modules to load before the one being actually requested to load.

For example:

- `modules.block` lists the modules for block devices
- `modules.networking` lists the ones for network devices.
- `modules.builtin` lists the path of modules included in the kernel.
- `modules.devname` lists the ones that would be loaded automatically if a particular device is created.

The kernel folder contains modules divided according to their use cases.

\[code language="bash"\] \[root@centos7 3.10.0-514.26.2.el7.x86\_64\]# ls -l kernel/ total 16 drwxr-xr-x. 3 root root 17 Jul 8 05:10 arch drwxr-xr-x. 3 root root 4096 Jul 8 05:10 crypto drwxr-xr-x. 67 root root 4096 Jul 8 05:10 drivers drwxr-xr-x. 26 root root 4096 Jul 8 05:10 fs drwxr-xr-x. 3 root root 19 Jul 8 05:10 kernel drwxr-xr-x. 5 root root 222 Jul 8 05:10 lib drwxr-xr-x. 2 root root 32 Jul 8 05:10 mm drwxr-xr-x. 33 root root 4096 Jul 8 05:10 net drwxr-xr-x. 11 root root 156 Jul 8 05:10 sound drwxr-xr-x. 3 root root 17 Jul 8 05:10 virt \[/code\]

Each directory within kernel contains modules depending on the area they're used for. For example, `kernel/fs/` contains filesystem drivers.

\[code language="bash"\] \[root@centos7 3.10.0-514.26.2.el7.x86\_64\]# ls -l kernel/fs total 48 -rw-r--r--. 1 root root 21853 Jul 4 11:51 binfmt\_misc.ko drwxr-xr-x. 2 root root 22 Jul 8 05:10 btrfs drwxr-xr-x. 2 root root 27 Jul 8 05:10 cachefiles drwxr-xr-x. 2 root root 21 Jul 8 05:10 ceph drwxr-xr-x. 2 root root 21 Jul 8 05:10 cifs drwxr-xr-x. 2 root root 23 Jul 8 05:10 cramfs drwxr-xr-x. 2 root root 20 Jul 8 05:10 dlm drwxr-xr-x. 2 root root 23 Jul 8 05:10 exofs drwxr-xr-x. 2 root root 21 Jul 8 05:10 ext4 drwxr-xr-x. 2 root root 51 Jul 8 05:10 fat drwxr-xr-x. 2 root root 24 Jul 8 05:10 fscache drwxr-xr-x. 2 root root 36 Jul 8 05:10 fuse drwxr-xr-x. 2 root root 21 Jul 8 05:10 gfs2 drwxr-xr-x. 2 root root 22 Jul 8 05:10 isofs drwxr-xr-x. 2 root root 21 Jul 8 05:10 jbd2 drwxr-xr-x. 2 root root 22 Jul 8 05:10 lockd -rw-r--r--. 1 root root 19597 Jul 4 11:51 mbcache.ko drwxr-xr-x. 6 root root 128 Jul 8 05:10 nfs drwxr-xr-x. 2 root root 40 Jul 8 05:10 nfs\_common drwxr-xr-x. 2 root root 21 Jul 8 05:10 nfsd drwxr-xr-x. 2 root root 4096 Jul 8 05:10 nls drwxr-xr-x. 2 root root 24 Jul 8 05:10 overlayfs drwxr-xr-x. 2 root root 24 Jul 8 05:10 pstore drwxr-xr-x. 2 root root 25 Jul 8 05:10 squashfs drwxr-xr-x. 2 root root 20 Jul 8 05:10 udf drwxr-xr-x. 2 root root 20 Jul 8 05:10 xfs \[/code\]

## depmod, and related commands

Modules can export the features it carry, called `symbols` which can be used by other modules. If module `A` depends on a symbol exported by module `B`, module `B` should be loaded first followed by module `A`.

`depmod` creates a list of symbol dependencies each module has, so that `modprobe` can go ahead and load the modules serving the symbols, prior loading the actual module.

`depmod` works by:

1. Creating a list of symbols each module exports.
2. Creating a list of symbol dependencies each module has.
3. Dumping the list of symbols each module exports, to `lib/modules/$(uname -r)/modules.symbols.bin` and `/lib/modules/$(uname -r)/modules.symbols`
4. Dumping the module dependency information to `/lib/modules/$(uname -r)/modules.dep.bin` and `/lib/modules/$(uname -r)/modules.dep`.
5. Creating `/lib/modules/$(uname -r)/modules.devnames` which contains the device file information (device type, major:minor number) that gets created at boot for this module to function properly.

**NOTE**:

- `modprobe` refers `/lib/modules/$(uname -r)/modules.dep.bin` to understand the dependencies each module require. A human-readable version of this file is maintained at `/lib/modules/$(uname -r)/modules.dep` but `modprobe` does not refer this.
- The binary file `modules.symbols.bin` carry the symbols exported (if any) by each module, one symbol per line. A human-readable version of the same is kept at `modules.symbols`.

A sneak peek into `modules.symbols` and `modules.dep`:

#### modules.symbols

\[code language="bash"\] \[root@centos7 3.10.0-514.26.2.el7.x86\_64\]# head modules.symbols # Aliases for symbols, used by symbol\_request(). alias symbol:cfg80211\_report\_obss\_beacon cfg80211 alias symbol:drm\_dp\_link\_train\_channel\_eq\_delay drm\_kms\_helper alias symbol:\_\_twofish\_setkey twofish\_common alias symbol:mlx4\_db\_free mlx4\_core alias symbol:nf\_send\_unreach nf\_reject\_ipv4 alias symbol:sdhci\_remove\_host sdhci alias symbol:videobuf\_dma\_init\_kernel videobuf\_dma\_sg alias symbol:ar9003\_paprd\_is\_done ath9k\_hw alias symbol:cxgbi\_ep\_disconnect libcxgbi \[/code\]

#### modules.dep

\[code language="bash"\] \[root@centos7 3.10.0-514.26.2.el7.x86\_64\]# head modules.dep kernel/arch/x86/kernel/cpu/mcheck/mce-inject.ko: kernel/arch/x86/kernel/test\_nx.ko: kernel/arch/x86/kernel/iosf\_mbi.ko: kernel/arch/x86/crypto/ablk\_helper.ko: kernel/crypto/cryptd.ko kernel/arch/x86/crypto/glue\_helper.ko: kernel/arch/x86/crypto/camellia-x86\_64.ko: kernel/crypto/xts.ko kernel/crypto/lrw.ko kernel/crypto/gf128mul.ko kernel/arch/x86/crypto/glue\_helper.ko kernel/arch/x86/crypto/blowfish-x86\_64.ko: kernel/crypto/blowfish\_common.ko kernel/arch/x86/crypto/twofish-x86\_64.ko: kernel/crypto/twofish\_common.ko kernel/arch/x86/crypto/twofish-x86\_64-3way.ko: kernel/arch/x86/crypto/twofish-x86\_64.ko kernel/crypto/twofish\_common.ko kernel/crypto/xts.ko kernel/crypto/lrw.ko kernel/crypto/gf128mul.ko kernel/arch/x86/crypto/glue\_helper.ko kernel/arch/x86/crypto/salsa20-x86\_64.ko: \[/code\]

`lsmod` is a parser that reads through `/proc/modules` and presents it in an easy-to-read format.

Note how `lsmod` parse throug the content of `/proc/modules` below:

\[code language="bash"\] \[root@centos7 3.10.0-514.26.2.el7.x86\_64\]# head /proc/modules test 12498 0 - Live 0xffffffffa0492000 (POE) binfmt\_misc 17468 1 - Live 0xffffffffa048c000 uhid 17369 0 - Live 0xffffffffa0486000 ipt\_MASQUERADE 12678 2 - Live 0xffffffffa0481000 nf\_nat\_masquerade\_ipv4 13412 1 ipt\_MASQUERADE, Live 0xffffffffa0451000 xt\_addrtype 12676 2 - Live 0xffffffffa044c000 br\_netfilter 22209 0 - Live 0xffffffffa0468000 dm\_thin\_pool 65565 1 - Live 0xffffffffa046f000 dm\_persistent\_data 67216 1 dm\_thin\_pool, Live 0xffffffffa0456000 dm\_bio\_prison 15907 1 dm\_thin\_pool, Live 0xffffffffa043f000

\[root@centos7 3.10.0-514.26.2.el7.x86\_64\]# lsmod | head Module Size Used by test 12498 0 binfmt\_misc 17468 1 uhid 17369 0 ipt\_MASQUERADE 12678 2 nf\_nat\_masquerade\_ipv4 13412 1 ipt\_MASQUERADE xt\_addrtype 12676 2 br\_netfilter 22209 0 dm\_thin\_pool 65565 1 dm\_persistent\_data 67216 1 dm\_thin\_pool \[/code\] **NOTE:**

1. The first field lists the module name.
2. The second field lists the size of the module in memory.
3. The third field lists the number of times the module is in use. \`0\` means the module is not used despite it being loaded.
4. The fourth field lists the modules which uses this module as their dependency.

## Creating a dummy module

The steps for creating a kernel module includes:

1. Writing the module file.
2. Writing the `Makefile` for the module.
3. Compile the module file using `make` , which will refer the `Makefile` to build it.

The module file and its corresponding Makefile are put in a separate directory so as to keep the kernel module directory clean. Once the module code and the Makefile are ready, the following `make` command is used to build the module, the `$(PWD)` being the directory where the module code and its Makefile is present.

\# make -C /lib/modules/$(uname -r)/build M=$PWD modules

The `make` command above does the following:

1. Change to the path mentioned after `-C`, ie.. to the location where the kernel Makefile is present. (`/lib/modules/$(uname -r)/build/`)
2. Use the kernel Makefile's macro `M` which denotes the location from which the code should be compiled, ie.. in this case, the PWD where the module code/Makefile is present.
3. Use the target `modules` which tells `make` to build the module.

Hence, the above command is trying to build a module in the current working directory, using the kernel Makefile at `/lib/modules/$(uname -r)/build/Makefile`

If we have a module file named `test.c` and its corresponding Makefile in `$(PWD)`, the `make` command would follow the steps below:

1. `make` calls the `modules` target and refers to the kernel `Makefile`.
2. The kernel Makefile looks for the module Makefile in $PWD.
3. The kernel Makefile read the module's Makefile and gets a list of the objects assigned to the macro `obj-m`.
4. The `make` command builds modules for each object assigned to the macro `obj-m`.

## Writing a simple module

The following is a very simple module, which prints a message while loading, and another one while unloading.

\[code language="C"\] #include #include #include

int test\_module(void) {     printk("Loading the test module!\\n");     return 0; }

void unload\_test(void) {     printk("Unloading the test module!\\n"); }

module\_init(test\_module) module\_exit(unload\_test) \[/code\] This has two functions, `test_module()` and `unload_test()` which simply prints a text banner upon loading and unloading respectively.

`module_init()` is used to load the module, and can call whatever functions that needs to initialize the module. We load our `test_module()` function into `module_init()` so that it gets initialized when the module is loaded.

`module_exit()` is called whenever the module has to be unloaded, and it can take in whatever functions are required to do a proper cleanup (if required) prior the module being unloaded. We load our `unload_test()` function in `module_exit()`.

## Writing a Makefile

Since the kernel Makefile will look in for the `obj-m` macro in the module Makefile with the object filename as its argument, add the following in the Makefile:

\[code language="text"\] obj-m := test.o \[/code\]

`make` will create an object file `test.o` from `test.c`, and then create a kernel object file `test.ko`.

## Compiling the module with \`make\`

Let's compile the module

\[code language="bash"\] \[root@centos7 test\]# pwd /lib/modules/3.10.0-514.26.2.el7.x86\_64/test \[root@centos7 test\]# ls Makefile test.c \[root@centos7 test\]# make -C /lib/modules/$(uname -r)/build M=$PWD modules make: Entering directory \`/usr/src/kernels/3.10.0-514.26.2.el7.x86\_64' CC \[M\] /lib/modules/3.10.0-514.26.2.el7.x86\_64/test/test.o Building modules, stage 2. MODPOST 1 modules CC /lib/modules/3.10.0-514.26.2.el7.x86\_64/test/test.mod.o LD \[M\] /lib/modules/3.10.0-514.26.2.el7.x86\_64/test/test.ko make: Leaving directory \`/usr/src/kernels/3.10.0-514.26.2.el7.x86\_64' \[/code\] Listing the contents show lot of new files, including the module code, the Makefile, the object file `test.o` created from `test.c`, the kernel object file `test.ko`.

`test.mod.c` contains code which should be the one ultimately being built to `test.ko`, but that should be for another post since much more is yet to be read/learned on what's happening there.

\[code language="bash"\] \[root@centos7 test\]# ls -l total 292 -rw-r--r--. 1 root root 16 Jul 27 11:52 Makefile -rw-r--r--. 1 root root 60 Jul 27 11:57 modules.order -rw-r--r--. 1 root root 0 Jul 27 11:57 Module.symvers -rw-r--r--. 1 root root 281 Jul 27 11:53 test.c -rw-r--r--. 1 root root 137768 Jul 27 11:57 test.ko -rw-r--r--. 1 root root 787 Jul 27 11:57 test.mod.c -rw-r--r--. 1 root root 52912 Jul 27 11:57 test.mod.o -rw-r--r--. 1 root root 87776 Jul 27 11:57 test.o \[/code\]

## Loading/Unloading the module

Loading and unloading the module should print the messages passed via `printk` in `dmesg`.

\[code language="bash"\] \[root@centos7 test\]# insmod ./test.ko \[root@centos7 test\]# lsmod | grep test test 12498 0 \[root@centos7 test\]# rmmod test \[/code\]

Checking `dmesg` shows the informational messages in the module code:

\[code language="bash"\] \[root@centos7 test\]# dmesg | tail \[35889.187282\] test: loading out-of-tree module taints kernel. \[35889.187288\] test: module license 'unspecified' taints kernel. \[35889.187290\] Disabling lock debugging due to kernel taint \[35889.187338\] test: module verification failed: signature and/or required key missing - tainting kernel \[35889.187548\] Loading the test module! \[35899.216954\] Unloading the test module! \[/code\] Note the messages about the module `test` tainting the kernel. Read more on how a module can taint the kernel, at [https://www.kernel.org/doc/html/latest/admin-guide/tainted-kernels.html.](https://www.kernel.org/doc/html/latest/admin-guide/tainted-kernels.html)

More on customizing the Makefile in another post.

