---
date created: 13-11-2022, Sunday, 07:27 PM
---

# 2 ways to boot with old kernel version in RHEL 8 using grubby

<https://www.golinuxcloud.com/boot-with-old-kernel-version-rhel-8-grubby/>

How to set default boot kernel in RHEL 8 Linux using [[Grubby]]? How to change the default boot entry for kernel in RHEL 8? How to boot with old kernel version in RHEL 8? How to revert to previous kernel version ?

![[2 ways to boot with old kernel version in RHEL 8 u a8dc265805864b838050c6c5c42008b6 old-kernel.jpg]]

Earlier I had shared the [steps to set default kernel in RHEL/CentOS 7 Linux node](https://www.golinuxcloud.com/set-default-boot-kernel-version-old-previous-rhel-linux/). Now with RHEL 8 the GRUB2 configuration parameter has changed again and now we use grubby to set default kernel or to change the default boot entry for kernel in the system.

*At the time of writing this article CentOS 8 was not available hence the steps could not be validated on CentOS 8 but I will assume that the same steps should work also on CentOS 8. If you face any problems while executing these steps on CentOS 8 then please drop in the details in the comment box at the end of this article.*

## What is Grubby?

**grubby** is a command line tool for updating and displaying information about the configuration files for various architecture specific bootloaders. It is primarily designed to be used from scripts which install new kernels and need to find information about the current boot environment.

## GRUB configuration file

The default bootloader target is primarily determined by the architecture for which grubby has been built. Each architecture has a preferred bootloader, and each bootloader has its own configuration file. If no bootloader is selected on the command line, grubby will use these default settings to search for an existing configuration. If no bootloader configuration file is found, grubby will use the default value for that architecture. These defaults are listed in the table below.

## Grubby Arguments

Below are some of the arguments which we will use in this article. These snippets are taken from man page of [grubby](https://linux.die.net/man/8/grubby)

## Check default boot kernel

Before we [configure our system to boot with old kernel version](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/sec-making_persistent_changes_to_a_grub_2_menu_using_the_grubby_tool) or set different boot kernel for our RHEL 8 system, let us check the current default kernel.

Here this means that post reboot the node will continue to boot from `/boot/vmlinuz-4.18.0-80.7.1.el8_0.x86_64` and mapped entries

To check the mapped index with this kernel use below command

You can get the list of initrd image available on your system under `/boot` as shown below:

To get more information about the respective initrd image, you can use `grubby --info`

## Get index ID of kernel using grubby

Before we configure our system to boot with old kernel version in RHEL 8, we must be familiar with the index mapping. Get the list of available kernels installed on your system

So as you see for the demonstration of this article I have installed 3 versions of kernel. Similarly I have three different initrd images mapped to respective kernel

Here the latest kernel will be considered to have index 0 then the older version will be mapped with index 1 then the next older version will be mapped with index 2**and so on..**

Now here since my system is running with the latest available kernel on my system, the index will be shown as "**0**"

Similarly if I boot my system with older kernel then the index will be shown respectively

For the oldest kernel available on my system

## Set default boot kernel (Grubby)

Now since we know the default kernel and index, we can proceed with the next steps to set default boot kernel using grubby in RHEL 8 and allow your system to boot with old kernel version. There are two methods to set default kernel using grubby tool

### Method 1: Boot with old kernel version using index

I hope we are clear on the kernel to index mapping part. So here I will demonstrate the usage of --set-default-index to set default kernel using index ID. Currently my system is running with index 0 i.e. latest kernel, which now I will change to older kernel version with index 1

Next you can check the default kernel using which the system will be booted during next reboot.

Similarly check the default index value which will be active post reboot

To activate the changes, reboot the node

Post reboot validate the changes

As expected now our system is running with kernel mapped with index 1 i.e. `4.18.0-80.4.2.el8`

Verify the same in the active GRUB2 configuration file

### Method 2: Boot with old kernel version using initrd image

Now here this step is little less confusing as you don't have to remember the index value. Here you can directly give the initrd image location using which you wish to set the default boot kernel.

Now currently my system is running with below kernel version

To change default kernel to `4.18.0-80.7.1.el8_0.x86_64` which is the latest available kernel on our system we will use the mapped initrd image

Next you can verify the status of default kernel and default index which will be active post reboot of the node

Next let us reboot our node to activate the changes

Post reboot as expected, our new kernel is loaded on the system

verify the same using GRUB2 configuration file

The same details can be checked using below commands again

Lastly I hope the steps from the article to **set default boot kernel** using **grubby** and **boot with old kernel version** in **RHEL 8** Linux was helpful. So, let me know your suggestions and feedback using the comment section.
