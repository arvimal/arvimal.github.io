---
tags:
- grub
- grub2
- bootloader
- mbr
- guid
- gpt
- efi
- bios
- boot
- grub2-mkconfig
---

# Get started with GRUB2

<https://www.certdepot.net/rhel7-get-started-grub2/>

Note: This is an [RHCSA 7 exam objective](https://www.certdepot.net/rhel7-rhcsa-exam-objectives/).

## Presentation of GRUB2

**GRUB2** is the new Linux bootloader. **GRUB2** stands for **GR**and **U**nified **B**ootloader version **2**.

As **GRUB** was not maintained for some time and lacked some critical features like **GPT** management needed to handle disks bigger than 2.4TB, it was decided to start a new version from scratch with modularity in mind.

**GRUB2** provides the following new features:

* ability to boot on various file systems (xfs, ext4, ntfs, hfs+, raid, etc),
* gzip files decompression on the fly,
* management of all disk geometries,
* support for **GPT** (**G**UID **P**artition **T**ables) and **MBR** (**M**aster **B**oot **R**ecord),
* portability with different architectures (BIOS, EFI, Coreboot, etc),
* ability to load modules at execution time.

## GRUB2 Organization

The **GRUB2** configuration is spread over several files:

* **/boot/grub2/grub.cfg**: this file contains the final **GRUB2** configuration (do not edit it directly!),
* **/etc/grub2.cfg**: this is a symbolic link to the **/boot/grub2/grub.cfg** file,
* **/etc/default/grub**: this file contains the list of the **GRUB2** variables (the values of the environment variables can be edited),
* **/etc/sysconfig/grub**: this is a symbolic link to the **/etc/default/grub** file,
* **/etc/grub.d**: this directory contains all the individual files internally used by **GRUB2**.

This tutorial will only explore knowledge required for the **RHCSA** exam. Refer to the **Additional Resources** section for more details.

## Basic Management

To get the details about the current active kernel, type:

```bash
# grub2-editenv list
saved_entry=CentOS Linux (3.10.0-229.11.1.el7.x86_64) 7 (Core)
```

Note: This information is stored in the **/boot/grub2/grubenv** file.

To get the list of the kernels displayed at boot time, type:

```bash
# grep ^menuentry /boot/grub2/grub.cfg
menuentry 'CentOS Linux (3.10.0-229.20.1.el7.x86_64) 7 (Core)' ...
menuentry 'CentOS Linux (3.10.0-229.14.1.el7.x86_64) 7 (Core)' ...
menuentry 'CentOS Linux 7 (Core), with Linux 0-rescue-f19b719117b44bf3a3fb777bd4127' ...caf
```

To permanently define the kernel to execute at boot time (here **0** for the first entry), type:

```bash
# grub2-set-default 0
```

To display the **GRUB2** variables, type:

```bash
# cat /etc/default/grub 
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL="serial console"
GRUB_SERIAL_COMMAND="serial --speed=115200"
GRUB_CMDLINE_LINUX="rd.lvm.lv=rhel/swap crashkernel=auto rd.lvm.lv=rhel/root console=ttyS0,115200"
GRUB_DISABLE_RECOVERY="true"

```

Where

* **GRUB_TIMEOUT** defines the boot waiting delay (here **5** seconds),
* **GRUB_DISTRIBUTOR** contains the distribution name (here **CentOS Linux**),
* **GRUB_DEFAULT** specifies the default menu entry; it can be a number, an entry name or the string **saved** which means the entry saved during the last reboot or the execution of the **grub2-set-default** command,
* **GRUB_DISABLE_SUBMENU** allows (**false**) or not (**true**) the display of a submenu (see below),
* **GRUB_TERMINAL** defines the terminal input & output device (here **console** and **serial**),
* **GRUB_SERIAL_COMMAND** configures the serial port,
* **GRUB_CMDLINE_LINUX** specifies the command-line arguments added to the menu entries for the Linux kernel,
* **GRUB_DISABLE_RECOVERY** defines if all entries can be selected in recovery mode through a separate line (**false**) or only the default entry (**true**).

If you want to change the content of any variables in the previous file, you will need to type:

```bash
# grub2-mkconfig -o /boot/grub2/grub.cfg
```

Note: This is the main command to memorize for the exam. You can also replace **/boot/grub2/grub.cfg** with **/etc/grub2.cfg**

To better understand some of the environment variables, here are the standard display with **GRUB_DISABLE_RECOVERY**=”true” and **GRUB_DISABLE_SUBMENU**=true:

```bash
      CentOS Linux 7 (Core), with Linux 3.10.0-229.20.1.el7.x86_64
      CentOS Linux 7 (Core), with Linux 3.10.0-229.14.1.el7.x86_64
      CentOS Linux 7 (Core), with Linux 0-rescue-f19b719117b44bf3a3fb777bd4127>

      Use the ^ and v keys to change the selection.                       
      Press 'e' to edit the selected item, or 'c' for a command prompt.   

```

If **GRUB_DISABLE_RECOVERY** is set to “false”, here is the new display:

```bash
      CentOS Linux 7 (Core), with Linux 3.10.0-229.20.1.el7.x86_64              
      CentOS Linux 7 (Core), with Linux 3.10.0-229.20.1.el7.x86_64 (recovery m>
      CentOS Linux 7 (Core), with Linux 3.10.0-229.14.1.el7.x86_64             
      CentOS Linux 7 (Core), with Linux 3.10.0-229.14.1.el7.x86_64 (recovery m>
      CentOS Linux 7 (Core), with Linux 0-rescue-f19b719117b44bf3a3fb777bd4127>
      CentOS Linux 7 (Core), with Linux 0-rescue-f19b719117b44bf3a3fb777bd4127>

      Use the ^ and v keys to change the selection.                       
      Press 'e' to edit the selected item, or 'c' for a command prompt.   

```

Each kernel line gets an associated line in recovery mode.

If **GRUB_DISABLE_RECOVERY** is now set to “true” (like in the initial standard display) and **GRUB_DISABLE_SUBMENU** is set to false, here is the new display:

```bash
      CentOS Linux 7 (Core)                                                     
      Advanced options for CentOS Linux 7 (Core)                               
      Use the ^ and v keys to change the selection.                       
      Press 'e' to edit the selected item, or 'c' for a command prompt.   

```

If the first entry is selected (“CentOS Linux 7 (Core)”), the system boots. If the second option is chosen, the standard menu is shown with an additional line at the bottom to go back to the first menu with the Esc key:

```bash
      CentOS Linux 7 (Core), with Linux 3.10.0-229.20.1.el7.x86_64              
      CentOS Linux 7 (Core), with Linux 3.10.0-229.14.1.el7.x86_64             
      CentOS Linux 7 (Core), with Linux 0-rescue-f19b719117b44bf3a3fb777bd4127>

      Use the ^ and v keys to change the selection.                       
      Press 'e' to edit the selected item, or 'c' for a command prompt.   
      Press Escape to return to the previous menu.                        

```

## Additional Resources

To better explore **GRUB2**, you can:

* read [Brendan Swigart’s article](http://mathematicbren.blogspot.fr/2014/12/grub2-rundown.html),
* loot at a [GRUB2 CentOS article](https://wiki.centos.org/HowTos/Grub2),
* explore the [GRUB2 configuration manual](http://www.gnu.org/software/grub/manual/grub.html),
* read a **Tecmint** article about [configuring and troubleshooting GRUB2](http://www.tecmint.com/configure-and-troubleshoot-grub-boot-loader-linux/),
* read a **LinuxSecrets** tutorial about [changing boot order with GRUB2](https://www.linuxsecrets.com/blog/6managing-linux-systems/2017/01/21/2140-change-boot-order-in-grub2),
* read this article describing the [RHEL 7 booting process](https://opensourceblogging.wordpress.com/2017/02/15/rhel-7-booting-process/).


# Customizing the GRUB 2 Configuration File

[https://docs.fedoraproject.org/en-US/Fedora/23/html/System_Administrators_Guide/sec-Customizing_the_GRUB_2_Configuration_File.html](https://docs.fedoraproject.org/en-US/Fedora/23/html/System_Administrators_Guide/sec-Customizing_the_GRUB_2_Configuration_File.html)

GRUB 2 scripts search the user's computer and build a boot menu based on what operating systems the scripts find. To reflect the latest system boot options, the boot menu is rebuilt automatically when the kernel is updated or a new kernel is added.

However, users may want to build a menu containing specific entries or to have the entries in a specific order. GRUB 2 allows basic customization of the boot menu to give users control of what actually appears on the screen.

GRUB 2 uses a series of scripts to build the menu; these are located in the `/etc/grub.d/` directory. The following files are included:

- `01_users`, which is created only when a boot loader password is assigned in a **kickstart** file.
- `10_linux`, which locates kernels in the default partition of Fedora.
- `30_os-prober`, which builds entries for operating systems found on other partitions.
- `40_custom`, a template, which can be used to create additional menu entries.

Scripts from the `/etc/grub.d/` directory are read in alphabetical order and can be therefore renamed to change the boot order of specific menu entries.

With the `GRUB_TIMEOUT` key set to `0` in the `/etc/default/grub` file, GRUB 2 does not display the list of bootable kernels when the system starts up. In order to display this list when booting, press and hold any alphanumeric key when the BIOS information is displayed; GRUB 2 will present you with the GRUB menu.

By default, the key for the `GRUB_DEFAULT` directive in the `/etc/default/grub` file is the word `saved`. This instructs GRUB 2 to load the kernel specified by the `saved_entry` directive in the GRUB 2 environment file, located at `/boot/grub2/grubenv`. You can set another GRUB record to be the default, using the `grub2-set-default` command, which will update the GRUB 2 environment file.

By default, the `saved_entry` value is set to the name of latest installed kernel of package type kernel. This is defined in `/etc/sysconfig/kernel` by the `UPDATEDEFAULT` and `DEFAULTKERNEL` directives. The file can be viewed by the `root` user as follows:

```
~]# cat /etc/sysconfig/kernel
# UPDATEDEFAULT specifies if new-kernel-pkg should make
# new kernels the default
UPDATEDEFAULT=yes

# DEFAULTKERNEL specifies the default kernel package type
DEFAULTKERNEL=kernel-core
```

The `DEFAULTKERNEL` directive specifies what package type will be used as the default. Installing a package of type kernel-debug will not change the default kernel while the `DEFAULTKERNEL` is set to package type kernel.

GRUB 2 supports using a numeric value as the key for the `saved_entry` directive to change the default order in which the operating systems are loaded. To specify which operating system should be loaded first, pass its number to the `grub2-set-default` command. For example:

```
~]# grub2-set-default 2
```

Note that the position of a menu entry in the list is denoted by a number starting with zero; therefore, in the example above, the third entry will be loaded. This value will be overwritten by the name of the next kernel to be installed.

To force a system to always use a particular menu entry, use the menu entry name as the key to the `GRUB_DEFAULT` directive in the `/etc/default/grub` file. To list the available menu entries, run the following command as `root`:

```
~]# awk -F\' '$1=="menuentry " {print $2}' /etc/grub2.cfg
```

The file name `/etc/grub2.cfg` is a symlink to the `grub.cfg` file, whose location is architecture dependent. For reliability reasons, the symlink is not used in other examples in this chapter. It is better to use absolute paths when writing to a file, especially when repairing a system.

Changes to `/etc/default/grub` require rebuilding the `grub.cfg` file as follows:

# GRUB 2 - Fedora Project Wiki

[https://fedoraproject.org/wiki/GRUB_2](https://fedoraproject.org/wiki/GRUB_2)

GRUB 2 is the latest version of GNU GRUB, the GRand Unified Bootloader. A bootloader is the first software program that runs when a computer starts. It is responsible for loading and transferring control to the operating system kernel, (Linux, in the case of Fedora). The kernel, in turn, initializes the rest of the operating system.

GRUB 2 has replaced what was formerly known as GRUB (i.e. version 0.9x), which has, in turn, become GRUB Legacy.

Starting with Fedora 16, GRUB 2 is the default bootloader on x86 BIOS systems. For upgrades of BIOS systems the default is also to install GRUB 2, but you can opt to skip bootloader configuration entirely.

## Updating GRUB 2 configuration on BIOS systems

The grub2 packages contain commands for installing a bootloader and for creating a bootloader configuration file.

grub2-install will install the bootloader - usually in the MBR, in free unpartioned space, and as files in /boot. The bootloader is installed with something like:

```
grub2-install /dev/sda
```

grub2-mkconfig will create a new configuration based on the currently running system, what is found in /boot, what is set in /etc/default/grub, and the customizable scripts in /etc/grub.d/ . A new configuration file is created with:

```
grub2-mkconfig -o /boot/grub2/grub.cfg
```

The configuration format has evolved over time, and a new configuration file might be slightly incompatible with the old bootloader. It is therefore a good idea to first run grub2-install whenever you would need to run grub2-mkconfig.

The Fedora installer, anaconda, will run these grub2 commands and there is usually no reason to run them manually.

It is generally safe to directly edit /boot/grub2/grub.cfg in Fedora. Grubby in Fedora patches the configuration when a kernel update is performed and will try to not make any other changes than what is necessary. (Other distributions, in particular Debian and Debian-derived distributions provide a software patch that adds an `update-grub` command which is neither included nor needed in Fedora.) Manual changes might however be overwritten with grub2-mkconfig next time the system is upgraded with anaconda. Some customizations can be placed in /etc/grub.d/40_custom or /boot/grub2/custom.cfg and will survive running grub2-mkconfig.

## Updating GRUB 2 configuration on UEFI systems

To install or fix GRUB 2 on a UEFI system on Fedora 18 or newer, you need to do four things:

UEFI firmware, in general, likes to boot from an EFI System Partition on a disk with a GPT label. In `gdisk`, it looks something like this:

```
Number  Start (sector)    End (sector)  Size       Code  Name
   1            2048          264191   128.0 MiB   EF00  EFI System

```

That partition should be formatted as FAT. If in doubt, FAT32 is a good dialect of FAT to choose.

Fedora expects this partition to be mounted at `/boot/efi`.

### Install the bootloader files

If you don't already have the relevant packages installed, do for Fedora 22 and later versions with [DNF](https://fedoraproject.org/wiki/Dnf) or with YUM for older Fedora releases:

```
dnf install grub2-efi shim
yum install grub2-efi shim
```

If you do, then try:

```
dnf reinstall grub2-efi shim
yum reinstall grub2-efi shim
```

instead.

Make sure that /boot/efi is mounted when you do this.

This installs the signed shim and the GRUB 2 binary.

### Create a GRUB 2 configuration

Under EFI, GRUB 2 looks for its configuration in `/boot/efi/EFI/fedora/grub.cfg`. For newly installed kernels to work, `grubby` expects `/etc/grub2-efi.cfg` to be a symlink to the real grub.cfg (i.e. `/boot/efi/EFI/fedora/grub.cfg`).

If you already have a grub 2 EFI config file, you should be okay. If not, grub2-mkconfig can help, but your mileage may vary.

```
grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg
```

**grub2-install shouldn't be used on EFI systems. The grub2-efi package installs a prebaked grubx64.efi on the EFI System partition, which looks for grub.cfg on the ESP in /EFI/fedora/ whereas the grub2-install command creates a custom grubx64.efi, deletes the original installed one, and looks for grub.cfg in /boot/grub2/.**

### Create a boot menu entry

TL;DR: This should happen automatically. If it doesn't, read on.

When you power on your system, your firmware will look for EFI variables that tell it how to boot. If you're already booted in EFI mode and EFI runtime services are working correctly, you can configure your boot menu with `efibootmgr`. If not, you'll have to bootstrap the process.

Fortunately, `shim` can help you bootstrap. The EFI program `/boot/efi/EFI/BOOT/fallback.efi` will look for files called `BOOT.CSV` in your ESP and will add boot entries corresponding to them, **if such entries do not already appear to exist**. `shim` provides a `BOOT.CSV` file that will add an entry for `grub2-efi` for you. So just using the EFI Shell to invoke `fallback.efi` should do the trick. You can do this with commands like:

```
> fs0:
> cd EFI\BOOT
> fallback.efi

```

If you have no boot entries at all, then just booting off your disk in UEFI mode should automatically invoke `/boot/efi/EFI/BOOT/BOOTX64.EFI`, which will, in turn, invoke `fallback.efi`.

If you already have incorrect boot entries, you'll either need to delete them or to modify `BOOT.CSV` to create new entries with different names.

## Adding Other operating systems to the GRUB 2 menu

grub2-mkconfig will add entries for other operating systems it can find. That will be done based on the output of the os-prober tool.

That might however not work so well, especially not for booting other Linux operating systems, and especially not on UEFI systems. See [http://www.gnu.org/software/grub/manual/grub.html#Multi_002dboot-manual-config](http://www.gnu.org/software/grub/manual/grub.html#Multi_002dboot-manual-config) .

## Setting default entry

**Please look to (default) kernel sysconfig options.** 
if file `/etc/sysconfig/kernel` have

```
UPDATEDEFAULT=yes
```

in every kernel update the grub entry is update to last entry, if you don't want that please set:

```
UPDATEDEFAULT=no
```

(write "no" in lower case)

Due to `grub2-mkconfig` (and os-prober) we cannot predict the order of the entries in `/boot/grub2/grub.cfg`, so we set the default by name/title instead.

Open `/etc/default/grub` and ensure this line exists:

```
GRUB_DEFAULT=saved
```

and ensure this line not exists:

```
GRUB_SAVEDEFAULT=true
```

or ensure this line exists:

```
GRUB_SAVEDEFAULT=false
```

Apply the change to `grub.cfg` by running:

Now list all possible menu entries

```
grep -P "submenu|^menuentry" /boot/grub2/grub.cfg | cut -d "'" -f2
```

Now set the desired default menu entry

```
grub2-set-default "<submenu title><menu entry title>"
```

Verify the default menu entry

```
grub2-editenv list
```

If you understand the risks involved and still want to directly modify /boot/grub2/grub.cfg, here's how you can do it:

Edit /boot/grub2/grub.cfg, and change the line

```
set default="0" 

```

to

```
set default="5"

```

## Encountering the dreaded GRUB 2 boot prompt

If improperly configured, GRUB 2 may fail to load and subsequently drop to a boot prompt. To address this issue, proceed as follows:

0. Load the XFS and LVM modules

```
insmod xfs
insmod lvm

```

1. List the drives which GRUB 2 sees:

```
grub2> ls

```

2. The output for a dos partition table /dev/sda with three partitons will look something like this:

```
(hd0) (hd0,msdos3) (hd0,msdos2) (hd0,msdos1)

```

3. While the output for a gpt partition table /dev/sda with four partitions will look something like this:

```
(hd0) (hd0,gpt4) (hd0,gpt3)  (hd0,gpt2) (hd0,gpt1)

```

4. With this information you can now probe each partition of the drive and locate your vmlinuz and initramfs files:

```
ls (hd0,1)/ 

```

Will list the files on /dev/sda1. If this partition contains /boot, the output will show the full name of vmlinuz and initramfs.

5. Armed with the location and full name of vmlinuz and initramfs you can now boot your system.

5a. Declare your root partition:

```
grub> set root=(hd0,3)

```

5b. Declare the kernel you wish to use:

```
grub> linux (hd0,1)/vmlinuz-3.0.0-1.fc16.i686 root=/dev/sda3 rhgb quiet selinux=0 
# NOTE : add other kernel args if you have need of them
# NOTE : change the numbers to match your system

```

5c. Declare the initrd to use:

```
  
grub> initrd (hd0,1)/initramfs-3.0.0-1.fc16.i686.img
# NOTE : change the numbers to match your system

```

5d. Instruct GRUB 2 to boot the chosen files:

```
grub> boot

```

6. After boot, open a terminal.

7. Issue the grub2-mkconfig command to re-create the grub.cfg file grub2 needed to boot your system:

```
grub2-mkconfig -o /boot/grub2/grub.cfg

```

8. Issue the grub2-install command to install grub2 to your hard drive and make use of your config:

```
grub2-install --boot-directory=/boot /dev/sda
# Note: your drive may have another device name. Check for it with mount command output.

```

## Additional Scenario

It's also possible to boot into a configfile that's located on another partition. If the user is faced with such a scenario, as is often the case with multi-boot systems containing Ubuntu and Fedora, the following steps in the grub rescue shell might become useful to know:

```
insmod part_msdos
insmod xfs
insmod lvm
set root='hd0,msdos1'
configfile /grub2/grub.cfg

```

Where, **hd0,msdos1** is the pertinent boot partition, which holds the grub.cfg file.

## Other GRUB 2 issues

**Absent Floppy Disk** : It has been reported by some users that GRUB 2 may fail to install on a partition's boot sector if the computer floppy controller is activated in BIOS without an actual floppy disk drive being present. A possible workaround is to run (post OS install) from rescue mode:

```
grub2-install <target device> --no-floppy

```

## Setting a password for interactive edit mode

If you wish to password-protect GRUB2's interactive edit mode **but** you do not want to require users to enter a password to do a plain, simple, ordinary boot, create /etc/grub.d/01_users with the following lines:

```
cat << EOF
set superusers="root"
export superusers
password root secret
EOF

```

To apply your changes run:

```
grub2-mkconfig -o /boot/grub2/grub.cfg

```

You can encrypt the password by using pbkdf2. Use grub2-mkpasswd-pbkdf2 to encrypt the password, then replace the password line with:

```
password_pbkdf2 root grub.pbkdf2.sha512.10000.1B4BD9B60DE889A4C50AA9458C4044CBE129C9607B6231783F7E4E7191D8254C0732F4255178E2677BBE27D03186E44815EEFBAD82737D81C87F5D24313DDDE7.E9AEB53A46A16F30735E2558100D8340049A719474AEEE7E3F44C9C5201E2CA82221DCF2A12C39112A701292BF4AA071EB13E5EC8C8C84CC4B1A83304EA10F74

```

Starting from atleast Fedora 21, the `--md5pass` kickstart option must be set using output from grub2-mkpasswd-pbkdf2.

## Using old graphics modes in bootloader

Terminal device is chosen with GRUB_TERMINAL; additional quote from [http://www.gnu.org/software/grub/manual/grub.html#Simple-configuration](http://www.gnu.org/software/grub/manual/grub.html#Simple-configuration)

`Valid terminal output names depend on the platform, but may include ‘console’ (PC BIOS and EFI consoles), ‘serial’ (serial terminal), ‘gfxterm’ (graphics-mode output), ‘ofconsole’ (Open Firmware console), or ‘vga_text’ (VGA text output, mainly useful with Coreboot).`

`The default is to use the platform's native terminal output.`

The default in Fedora is gfxterm and to get the legacy graphics modes you need to set GRUB_TERMINAL to right variable from the description above in /etc/default/grub

## Enable Serial Console in Grub

To enable Serial console in grub add the following entry's to /etc/default/grub

( Adjust baudrate/parity/bits/flow control to fit your environment and cables)

```
GRUB_CMDLINE_LINUX='console=tty0 console=ttyS0,115200n8'
GRUB_TERMINAL=serial
GRUB_SERIAL_COMMAND="serial --speed=115200 --unit=0 --word=8 --parity=no --stop=1"

```

And re-generate grub

`grub2-mkconfig -o /boot/grub2/grub.cfg`

**NOTE:** in UEFI boot environment, use `efi0` instead of `--unit=0`. If that doesn't work, check that your serial port is visible in your UEFI environment, e.g. by running `devtree` or `dh -p SerialIO` in EFI Shell. See [this discussion](https://lists.gnu.org/archive/html/help-grub/2017-01/msg00007.html) for more information.

Normally, **GRUB2** will be installed and set up by the installer, **Anaconda**, during the installation process. You will probably never have to deal with manual installation of **GRUB2**. However, in certain situations , you will want to install **GRUB2** manually, especially if you need to repair the existing **GRUB2** installation or you want to change its configuration.

This procedure shows the steps to install **GRUB2** on a UEFI system on Fedora 18 or newer. The procedure consists of four parts.

### Creating an EFI System Partition

The UEFI firmware requires to boot from an _EFI System Partition_ on a disk with a GPT label. To create such a partition:

1.  List available block devices to find a place to create your ESP.
    
2.  Create at least a 128 MiB disk partition using a GPT label on the primary hard disk.
    
    For the sake of this procedure, we assume that the created partition is recognized as `/dev/sda1`.
    
3.  Format the partition with the _FAT32_ file system.
    
4.  Create the `/boot/efi` directory as a mount point for the new partition.
    
5.  Mount the partition to the `/boot/efi` mount point.
    
    ```
    # mount /dev/sda1 /boot/efi
    ```
    
6.  Proceed to the next part.
    

### Install the bootloader files

In order to use **GRUB2** with on the UEFI systems, you need to install or re-install appropriate packages:

1.  Re-install the necessary packages.
    
    ```
    # dnf reinstall grub2-efi grub2-efi-modules shim
    ```
    
2.  If the above command ends with an error, install the packages.
    
    ```
    # dnf install grub2-efi grub2-efi-modules shim
    ```
    

More information

-   This installs the signed **shim** and the **GRUB2** binary.
    

### Create a GRUB2 configuration

If you already have a working **GRUB2** EFI configuration file, you do not need to do anything else.

Otherwise, create the configuration file using the `grub2-mkconfig` command.

```
# grub2-mkconfig -o /boot/grub2/grub.cfg
```

More information

-   Under EFI, **GRUB2** looks for its configuration in `/boot/efi/EFI/fedora/grub.cfg`, however the postinstall script of `grub2-common` installs a small shim which chains to the standard configuration at `/boot/grub2/grub.cfg` which is generated above. To reset this shim to defaults, delete the existing `/boot/efi/EFI/fedora/grub.cfg` and then `dnf reinstall grub2-common`.
    
-   For newly installed kernels to work, `grubby` expects `/etc/grub2-efi.cfg` to be a symlink to the real `grub.cfg` (for example `/boot/grub2/grub.cfg`).
    

### Solving problems with UEFI bootloader

When you power on your system, your firmware will look for EFI variables that tell it how to boot. On running systems, which have booted into the EFI mode and their EFI runtime services are working correctly, you can configure your boot menu with `efibootmgr`.

If not, `shim` can help you bootstrap. The EFI program `/boot/efi/EFI/BOOT/fallback.efi` will look for files called `BOOT.CSV` in your ESP and will add boot entries corresponding to them. The `shim` command provides its own `BOOT.CSV` file that will add an entry for `grub2-efi`.

During the boot process, you can use the **EFI Shell** to invoke the `fallback.efi` profile to boot the system:

1.  Enter the boot partition.
    
2.  Navigate into the `EFI\BOOT` directory.
    
3.  Invoke the `fallback.efi` profile.
    

More information

-   If you have no boot entries at all, then just booting off your disk in UEFI mode should automatically invoke `/boot/efi/EFI/BOOT/BOOTX64.EFI`, which will, in turn, invoke `fallback.efi`.
    
-   If you already have incorrect boot entries, you’ll either need to delete them or to modify `BOOT.CSV` to create new entries with different names.

---
# The Grub2 Rescue shell

<https://aty.sdsu.edu/bibliog/latex/debian/grub2rescue.html>

## Introduction

Nothing is more frustrating than making some small change to your system, and then discovering that it won't boot. This must have happened to me dozens of times over the years; and the problem is always something different and unexpected.

The most frustrating experience you can have with GRUB is to be dropped into its “Rescue shell”. You might get a cryptic error message, followed by

Entering rescue mode . . .

grub rescue>

No help; no advice on how to proceed; and even the Grub2 Manual tells you nothing useful. Yuck.

The rescue shell is an exceedingly minimal, Spartan environment. It offers only a tiny subset of the regular Grub shell's commands:

set unset ls insmod

These commands offer no options, and it is impossible even to learn which ones are available. Even common commands like cat and cd are not available. At first glance, it would seem impossible to do anything useful in this limited environment.

And yet, it's actually possible to go through the booting process **manually** — provided that you know something about the booting process, and how Grub handles it. In fact, the operations that Grub executes automatically can be done by hand, just with the limited means provided by the rescue shell.

## Understanding Disaster

Actually, the fact that you see the grub rescue> prompt is good news in disguise. It means you haven't wiped out Grub's booting system. The hardware has gone through the POST process, and loaded the primary stage of the boot loader; but the information available to that stage (supposedly, the addresses of the disk blocks that hold the next stage) was wrong. Grub is alive, but it needs a little help.

The common causes of this situation are things that changed the locations of the next pieces of Grub's boot-time subsystem. Maybe you re-formatted the filesystem that holds those files; maybe you updated a kernel, but didn't re-generate Grub's configuration files; maybe you ran update-grub with incorrect partition identifiers in the /etc/grub.d/40_custom shell script. The result was that Grub's early stages that depend on absolute block addresses couldn't find the following pieces. You can tell the part of Grub that's already working how to proceed.

With luck, the error message that precedes the rescue prompt will tell you what Grub looked for but couldn't find. Write it down, and take appropriate action after you've re-booted your box.

### Diagnosing disaster

The first thing to do is to find out what Grub knows already. At the

grub rescue>

prompt, enter the command:

set

and Grub will tell you what little it knows. Again, take note of this information, as it will provide clues to what you need to do next — as well as clues to fixing the problem **before** the next reboot.

The main Grub variables available at this point are usually the prefix and root parameters. What Grub calls prefix is the location (in Grub's peculiar notation) of the directory that holds Grub's pieces. In normal *IX terminology, this would usually be /boot/grub. But Grub doesn't have mounted filesystems yet; it only knows about disk partitions, which it calls things like (hd0,msdos1).

So, if you have a separate boot partition, which is normally mounted on /boot, Grub will need to have prefix set to an address of the form (hd0,msdos1)/grub. On the other hand, if your /boot directory is in your root-filesystem's partition, Grub will need to have prefix=(hd0,msdos1)/boot/grub.

Similarly, what Grub calls root is NOT the partition that contains the root **filesystem**, but the partition that contains the kernel and initial RAM filesystem (i.e., initramfs) files. That usually means that Grub thinks root=(hd0,msdos1).

## Fixing the problem

First of all, make sure Grub can see the partitions that contain these vital parts. Tell the rescue shell:

ls

and it will show you the partitions it knows about. This will be a list of things like

(hd0,msdos1) (hd0,msdos2) . . .

which mean /dev/sda1, /dev/sda2, and so on. Remember that Grub's name for the first disk is hd0; the second disk is hd1, etc. — but the partitions themselves are numbered normally, starting at 1 instead of zero.

Don't be misled by a superficial resemblance between the rescue-shell ls command and the normal ls that you use at a bash prompt. The normal command has scads of options; the rescue-shell command is a stripped-down version with no options, and a different output format. Only the names are similar.

If the rescue shell had a cat command, you could list the contents of /boot/grub/device.map to learn Grub's correspondence between disks and names; but it doesn't, so you can't. Keep a copy of the device.map file printed out beforehand, because the devices might not map out the way you expect. (For example, on my machine, Grub thinks sda is hd0, as you'd expect; but it also thinks sdb is hd2, and sdc is hd1, which is screwy.)

Then, if Grub has the wrong values for either prefix or root, you can fix its error by telling the rescue shell something like

set prefix=(hd0,msdos1)/boot/grub

or whatever the correct value is in your box.

Remember that you can verify that Grub has the correct values for these parameters with a simple

set

command. And you can double-check by telling the rescue shell to list the contents of those directories:

ls $prefix/

## Proceed to boot manually

Now you need to lead Grub through its normal booting sequence. The first step is to make sure it has its module available:

insmod normal

This module is the “guts” of Grub2: it contains the apparatus for reading configuration files, and displaying the usual Grub boot menu. The correct prefix and root parameter values are needed, if Grub is to find any modules.

Once the module is inserted, you can execute it as a **new** rescue-shell command:

normal

Another vital module that must be loaded is the linux.mod file:

insmod linux

Now you can set up the linux kernel's command line:

linux /boot/vmlinuz-3.16.0-4-686-pae root=/dev/sda2 ro

or whatever is the correct name for your kernel. Note that the “root” in this line points (in normal terms) to your root filesystem's disk partition; it is **different** from Grub's root parameter! You can specify the root partition here in perfectly normal terms — either by specifying --fs-uuid and the UUID of the partition, or by using a filesystem label, as in root=LABEL=ROOT (if your root filesystem is named ROOT). If you need additional command-line parameters, like video=640x480, be sure to add them here as well.

Similarly, you need to tell Grub where the initial RAMdisk filesystem is:

initrd /boot/initrd.img-3.16.0-4-686-pae

Make sure it matches the kernel version!

Now, with both the kernel and the initrd modules installed, and their arguments supplied, Grub should be able to boot. Tell the rescue shell to do so:

boot

Once the linux and normal modules are inserted, most of Grub's apparatus will be working, and the larger set of normal GrubScript commands will be accessible. Or, if you get everything messed up and want to start over, the usual invocation will re-boot the system.

## Back to normal

When you are back up, be sure to fix the errors that caused the booting problem. If the configuration parameters are set in the file and any special scripts (like ), you should be able to get a correct just by executing (as **root**):

update-grub

and

grub-install /dev/sda

(or whatever disk is marked as the boot device in your BIOS).

Sometimes, the error that brought up the rescue shell was

error: no such device:

followed by a UUID for some partition that has disappeared — usually, due to a re-made partition. In this case, you may need to invoke

update-initramfs -u -v

to get the correct partition named in the initrd.img file.

Copyright © 2015, 2017 Andrew T. Young

Back to the . . . **[main LaTeX page](https://aty.sdsu.edu/bibliog/latex/latex_top.html)**


# GrubEFIReinstall

[https://wiki.debian.org/GrubEFIReinstall](https://wiki.debian.org/GrubEFIReinstall)

Starting with Windows 8 most Desktop PC have EFI as firmware instead of the legacy [BIOS](https://wiki.debian.org/BIOS). If your EFI based PC is not booting debian, here is an easy way to reinstall grub-efi, the bootloader used by debian on these PCs.

To reinstall grub, you need either a live CD/USB to access your current system , or you can use the rEFInd boot manager on a live CD/USB to boot your current system.

## Using the rEFInd rescue media

At the author's web page [http://www.rodsbooks.com/refind/getting.html](http://www.rodsbooks.com/refind/getting.html), you will find updated direct links to all sorts of packaging. To boot from a rescue media, select either the CD iso or the image for USB stick, most firmware offers the choice nowadays. If choosing the latter make sure to follow the instructions in the readme. It is recommended to read the author's web pages to get a better understanding of what you are doing.

## Boot your computer with the Refind media

Refind will parse your hard drive for installed kernels, and provide you a graphic menu to boot them. Choose your Linux Kernel and boot it.

## Reinstalling grub-efi on your hard drive

Check that the computer booted in computer in EFI mode:

```
[ -d /sys/firmware/efi ] && echo "EFI boot on HDD" || echo "Legacy boot on HDD"
should return "EFI boot on HDD".
```

After starting a root shell ( if you boot from a live media, you should start a chroot shell instead, as explained in [https://help.ubuntu.com/community/Grub2/Installing#via_ChRoot](https://help.ubuntu.com/community/Grub2/Installing#via_ChRoot) ) check that your EFI system partition (most probably /dev/sda1) is mounted on /boot/efi. If the /boot/efi directory does not exist, you will need to create it.

```
mount /dev/sda1 /boot/efi
```

Reinstall the grub-efi package

```
apt-get install --reinstall grub-efi
```

Put the debian bootloader in /boot/efi and create an appropriate entry in the computer NVRAM

```
grub-install /dev/sda
```

Re create a grub config file based on your disk partitioning schema

```
update-grub
```

You should check afterwards that:

Check 1. the bootloader is existing in /boot/efi/EFI/debian/grubx64.efi

```
file /boot/efi/EFI/debian/grubx64.efi

/boot/efi/EFI/debian/grubx64.efi: PE32+ executable (EFI application) x86-64 (stripped to external PDB), for MS Windows
```

Check 2. the nvram entry was properly created.

```
efibootmgr --verbose | grep debian
```

You can now reboot, and Grub should greet you.

## Troubleshooting

If after this steps you're not booting, the EFI of your PC might have some bugs.

### Problem1: Weak EFI implementation only recognizes the fallback bootloader

The uefi firmware refuses to boot the debian/grubx64.efi bootloader, and so we have to hijack the uefi fallback boot loader. See [http://mjg59.livejournal.com/138188.html](http://mjg59.livejournal.com/138188.html) for details.

Using debian installer in rescue mode, /dev/sda1 being the FAT32 ESP partition, /dev/sda2 the root partition

```
mkdir /target
mount /dev/sda2 /target
mount /dev/sda1 /target/boot/efi
for i in /sys /proc /dev; do mount --bind $i /target$i; done
chroot /target
```

```
cd /boot/efi/EFI
mkdir boot
cp debian/grubx64.efi boot/bootx64.efi
exit
for i in /sys /proc /dev; do umount /target$i; done
umount /target/boot/efi
umount /target
```

Once booted into your normal Debian, tell grub to ensure the fallback boot loader up to date. To do that, run the following:

```
echo "grub-efi-amd64 grub2/force_efi_extra_removable boolean true" | sudo debconf-set-selections
```

Note: The above command will permanently hijack the fallback boot loader, which might be undesirable in dual-boot setups.

### Problem2: EFI boot entries disappear after reboot

The uefi firmware did not create a proper boot entry in NVRAM. This has been seen in a Lenovo Thinkcenter M92Z. The symptom for this will be a missing HD path after the debian entry in the efibootmgr --verbose output.

```
BootCurrent: 0024
Timeout: 0 seconds
BootOrder: 0024,0022,0023,0016,0000,0001
Boot0000* debian        Vendor(99e275e7-75a0-4b37-a2e6-c5385e6c00cb,)
Boot0016* Generic Usb Device    Vendor(99e275e7-75a0-4b37-a2e6-c5385e6c00cb,)
Boot0022* UEFI: IPv4 Intel(R) 82579LM Gigabit Network Connection        ACPI(a0341d0,0)PCI(19,0)MAC(d43d7e6d8bfc,0)IPv4(0.0.0.0:0<->0.0.0.0:0,0, 0AMBO
Boot0023* UEFI: IPv6 Intel(R) 82579LM Gigabit Network Connection        ACPI(a0341d0,0)PCI(19,0)MAC(d43d7e6d8bfc,0)030d3c000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000AMBO
Boot0024* UEFI: Generic Flash Disk 8.00 ACPI(a0341d0,0)PCI(1d,0)USB(1,0)USB(1,0)HD(1,800,2a5f,02f23208-1aa9-4b6c-b6e1-8155390eb9db)AMBO
```

You can then try to install Refind as your bootloader in the hard drive, following the steps at this gist: [https://gist.github.com/EmmanuelKasper/9590327](https://gist.github.com/EmmanuelKasper/9590327).

# How to update GRUB2 using grub2-editenv and grubby in RHEL 8 Linux

[https://www.golinuxcloud.com/update-grub2-grubby-grub2-editenv-rhel-8/](https://www.golinuxcloud.com/update-grub2-grubby-grub2-editenv-rhel-8/)

## Notes:

- In rescue mode, in case chroot to the filesystem on-disk does not work, do the following manually:
    1. Check the partitions and type (fdisk -l), and identify if LVM volumes exist.
    2. If LVM exists, activate them using `lvm vgscan` and `lvm vgchange -ay`
    3. Mount /dev/<VG_name>/root onto a folder that will be used as a chroot folder later (mount /dev/<VG_name>/root /sysroot)
    4. Mount /dev/sda1 on /boot (Check if /dev/sda1 is the disk containing /boot)
    5. Mount other valid logical volumes (Check with lvm lvs) onto folders under /sysroot/ 
        1. Eg.. /dev/rhel_vg/var/ on /sysroot/var
    6. Bind mount /proc, /sys, /dev onto /sysroot
        1. mount —bind /proc /sysroot/proc
        2. mount —bind /dev /sysroot/dev
        3. mount —bind /sys /sysroot/sys
        

**The boot loader Grand Unified Boot Loader (GRUB2) in RHEL 8 differs from the GRUB2 in RHEL 7.** In this article I will share different commands to update GRUB2 and set kernel command line argument in RHEL 8 Linux.

An update to Red Hat Enterprise Linux 8 Beta results in `/etc/default/grub` changes no longer being included when issuing `grub2-mkconfig -o /boot/grub2/grub.cfg`. It seems that at least some options set there are now silently ignored.

In this article I will disable IPv6 using GRUB2 (`ipv6.disable`) on [RHEL 8 Linux](https://www.golinuxcloud.com/step-by-guide-install-rhel-8-beta-screenshots/) to demonstrate the steps to update GRUB2 in RHEL 8 Linux host.

## Update GRUB2 using grub2-editenv

The `grub2-editenv` utility is actually the recommended path to alter these variables. As a result, the following can be used. Appending an extra argument:

```
[root@rhel-8 ~]# grub2-editenv - list | grep kernelopts
kernelopts=root=/dev/mapper/rhel-root ro crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet
```

Here copy paste the content from above command and append the additional kernel parameter you wish to add to the GRUB2.

```
[root@rhel-8 ~]# grub2-editenv - set "kernelopts=root=/dev/mapper/rhel-root ro crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet ipv6.disable=1"
```

Alternatively you can also choose a shorter and less error prone approach as shown below

```
[root@rhel-8 ~]# grub2-editenv - set "$(grub2-editenv - list | grep kernelopts) ipv6.disable=1"
```

Here, `$(grub2-editenv - list | grep kernelopts)` will automatically select the existing `kernelopts` and will append the additional kernel command line argument.

Verify the newly added output

```
[root@rhel-8 ~]# grub2-editenv - list | grep kernelopts
kernelopts=root=/dev/mapper/rhel-root ro crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet ipv6.disable=1
```

Next reboot the node and verify the configuration to make sure your changes are persistent

```
[root@rhel-8 ~]# grub2-editenv - list | grep kernelopts
kernelopts=root=/dev/mapper/rhel-root ro crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet ipv6.disable=1
```

As you can see our IPv6 is disabled in the GRUB2 command line.

```
[root@rhel-8 ~]# cat /proc/cmdline
BOOT_IMAGE=(hd0,msdos1)/vmlinuz-4.18.0-80.el8.x86_64 root=/dev/mapper/rhel-root ro crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet ipv6.disable=1
```

Similarly to **remove a parameter** or argument from kernel command line in GRUB2, use the below syntax

```
# grub2-editenv - set "$(grub2-editenv - list | grep kernelopts | sed -e 's///')"
```

Lastly reboot your system for the changes to take effect.

## Update GRUB2 using grub2-mkconfig

The older method of achieving this behaviour is still possible, but the existing `kernelopts` value will need to be unset first:

```
[root@rhel-8 ~]# grep GRUB_CMDLINE_LINUX /etc/default/grub
GRUB_CMDLINE_LINUX="crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet"
```

Here I will update `ipv6.disable=1` in the GRUB2 configuration file `/etc/default/grub`

```
[root@rhel-8 ~]# grep GRUB_CMDLINE_LINUX /etc/default/grub
GRUB_CMDLINE_LINUX="crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet ipv6.disable=1"
```

But as you see the existing kernelopts reflects old GRUB2 entry, so if we reboot the node or rebuild our GRUB2 then the new changes will not reflect on the node.

```
[root@rhel-8 ~]# grub2-editenv - list | grep kernelopts
kernelopts=root=/dev/mapper/rhel-root ro crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet
```

So we need to unset the kernelopts which is an additional step here:

```
[root@rhel-8 ~]# grub2-editenv - unset kernelopts
```

next rebuild the grub configuration

```
[root@rhel-8 ~]# grub2-mkconfig -o /boot/grub2/grub.cfg
Generating grub configuration file ...
done
```

Next re-verify `kernelopts`

```
[root@rhel-8 ~]# grub2-editenv - list | grep kernelopts
kernelopts=root=/dev/mapper/rhel-root ro crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet ipv6.disable=1
```

So our changes are visible as expected.

## Update GRUB2 using grubby

grubby is a utility for manipulating bootloader-specific configuration files.

You can use grubby also for changing the default boot entry, and for adding/removing arguments from a GRUB2 menu entry.

```
[root@rhel-8 ~]# grubby --info DEFAULT
index=0
kernel="/boot/vmlinuz-4.18.0-80.el8.x86_64"
args="ro crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet $tuned_params"
root="/dev/mapper/rhel-root"
initrd="/boot/initramfs-4.18.0-80.el8.x86_64.img $tuned_initrd"
title="Red Hat Enterprise Linux (4.18.0-80.el8.x86_64) 8.0 (Ootpa)"
id="f653c3662e81432aa484cd1639a04047-4.18.0-80.el8.x86_64"
```

Add the argument you wish to append to the kernel command line menu

```
[root@rhel-8 ~]# grubby --args ipv6.disable=1 --update-kernel DEFAULT
```

Next verify the GRUB2 configuration

```
[root@rhel-8 ~]# grubby --info DEFAULT
index=0
kernel="/boot/vmlinuz-4.18.0-80.el8.x86_64"
args="ro crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet $tuned_params ipv6.disable=1"
root="/dev/mapper/rhel-root"
initrd="/boot/initramfs-4.18.0-80.el8.x86_64.img $tuned_initrd"
title="Red Hat Enterprise Linux (4.18.0-80.el8.x86_64) 8.0 (Ootpa)"
id="f653c3662e81432aa484cd1639a04047-4.18.0-80.el8.x86_64"
```

Next reboot the node to activate the changes

```
[root@rhel-8 ~]# cat /proc/cmdline
BOOT_IMAGE=(hd0,msdos1)/vmlinuz-4.18.0-80.el8.x86_64 root=/dev/mapper/rhel-root ro crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet ipv6.disable=1
```

Lastly I hope the steps from the article to **set kernel command line argument, update GRUB2 using grub2-editenv, grub2-mkconfig and grubby in RHEL 8 Linux** was helpful. So, let me know your suggestions and feedback using the comment section.