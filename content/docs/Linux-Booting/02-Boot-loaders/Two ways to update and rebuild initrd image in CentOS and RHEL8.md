# 2 ways to update and rebuild initrd image in CentOS/RHEL 7 and 8

[https://www.golinuxcloud.com/update-rebuild-initrd-image-centos-rhel-7-8/](https://www.golinuxcloud.com/update-rebuild-initrd-image-centos-rhel-7-8/)

How do I unpack or uncompress, and then repack or re-compress, an initrd or initramfs boot image file? How do I modify the contents of an initrd or initramfs? How do I view an initrd or initramfs? How to customize initrd in RHEL Linux. How to rebuild initrd image in RHEL 8 Linux. How to update initrd in RHEL 7 Linux. How to update initrd with XV compressed data. How to rebuild initrd image with LZMA compressed data. How to rebuild the initial ramdisk image in Red Hat Enterprise Linux. How to rebuild initial ram disk image in Red Hat Enterprise Linux. How to remake or recreate the initrd or initramfs.

![[2 ways to update and rebuild initrd image in CentO 327aae521d6a489894f00648e19a906b initrd.jpg]]

## What is initrd?

- The initial RAM disk (initrd) is an initial root file system that is mounted prior to when the real root file system is available. The initrd is bound to the kernel and loaded as part of the kernel boot procedure. The kernel then mounts this initrd as part of the two-stage boot process to load the modules to make the real file systems available and get at the real root file system.
- The initrd file contains a minimal set of directories and executables to achieve this, such as the `insmod` tool to install kernel modules into the kernel. In other words, it contains the necessary executables and system files to support the [second-stage boot of a Linux](https://www.golinuxcloud.com/read-user-input-during-boot-stage-linux/) system.
- The initrd image is present under `/boot` directory and is owned by kernel package.
- The version of the running kernel on the system will be used to identify the current initrd image used during booting process.

There are two initrd image available with RHEL 7. The one which is created after kernel is installed on the root file system i.e. available inside `/boot/initramfs-$(uname -r).img` while the other one is available inside the RHEL ISO DVD which is loaded at the initial stage of system boot up. In this article we study about the steps to update and rebuild initrd available in the RHEL ISO DVD, to learn about the steps to extract and rebuild initramfs from the system you can follow [this article](https://www.golinuxcloud.com/extract-initramfs-cpio-premature-end-archive/).

## Why should I update initrd?

Initrd contains many drivers for third party vendors along with many modules and executables which help OS detect the underlying hardware. It is possible that on a new hardware the initrd fails to detect the underlying hardware part such as Network Card, Storage Adapter etc. In such situations we can modify the `initrd` image.

Although instead of adding driver modules from third party vendor into `initrd`, I would recommend creating a custom DUD (Driver Update Disk) as it also performs the same task and is a better alternative rather than updating and rebuilding `initrd`.

Modifying `initrd` in production environment is not recommended, if you have a valid subscription then you should get in touch with your support team to handle any issue which requires `initrd` modification.

Rather than modifying the `initrd` image, you can also opt to create an `updates.img` file which is called at a later stage of the BOOT UP. But if your problem is related to detection failure of underlying hardware then `updates.img` will not help.

## Which one to choose initrd.img vs updates.img?

anaconda has the capability to incorporate updates at runtime to fix any bugs or issues with the installer. These updates are generally distributed as a disk image file (referred to as updates.img in this article).

So we have two options with us to alter the boot up process with our customized changes, one with initrd and the other with `updates.img`

The answer to this question depends on your requirement. `updates.img` is called at a later stage of the boot up procedure so if you wish to include important modules to detect hardware then you should update and rebuild initrd while if you need to add some bug fixes for the RHEL OS then you can go ahead with `updates.img`

## Check initrd content

Before we update initrd, it is a good idea to verify the existing content of our initrd image. Here I am checking the content of initrd from the RHEL 8 ISO image.

Here in this list you can look for the content of initrd image file.

## Method 1: Extract initrd image

Based on the initrd file compression type the command to extract and rebuild initrd will vary. For our case in both RHEL 7 and 8 we have XZ compressed data in initrd file as shown below:

So we can use the same method to extract and rebuild initrd for both RHEL 7 and 8 Linux.

We will create a temporary directory where we will extract and update initrd

To extract initrd use the below command:

This will extract all the content of initrd in the current directory

## Method 2: Extract initrd image

Alternatively you can also extract the initrd using the below list of steps. To start with copy the initrd file from the RHEL 7/8 ISO DVD to a temporary directory

Verify the file

Now extract the file

With this the initrd.img will extract and create an initrd file

Extract the content of this initrd in the current directory

Verify the content of the initrd

## Update initrd image

Now since we have successfully extracted initrd, you can go ahead and do your modification. For example you can add new driver modules from the vendor to support some new hardware or any other custom change.

For the sake of this article I wish to add a udev rule file to my initrd to detect and map the NIC cards with pre-defined PCI ID

We will add this in our initrd under `/usr/lib/udev/rules.d`

## Method 1: Rebuild initrd image

If you extract initrd using [Method 1](https://www.golinuxcloud.com/update-rebuild-initrd-image-centos-rhel-7-8/#Method_1_Extract_initrd_image) then follow this procedure to rebuild initrd image, navigate to your temporary directory where you did extract initrd image.

Execute the below command to rebuild initrd image with xz as compression format

Check the compression type of your new initrd file

## Method 2: Rebuild initrd image

If you perform extract initrd using [Method 2](https://www.golinuxcloud.com/update-rebuild-initrd-image-centos-rhel-7-8/#Method_2_Extract_initrd_image) then follow this procedure to rebuild initrd image, navigate to your temporary directory where you did extract initrd image.

Remove the initrd file which was already extracted is in the same directory.

Next rebuild initrd image using the below command:

Verify the new initrd image

## Verify initrd image

Now since we successfully rebuild initrd image, let us verify the content of our new initrd and make sure our new rule file is present in this initrd image

So as you see our file is now part of the initrd file. So now you can use this initrd file to boot up your system.

Similarly you can verify the content of initrd which you create using the [Method 2](https://www.golinuxcloud.com/update-rebuild-initrd-image-centos-rhel-7-8/#Method_2_Extract_initrd_image).

Lastly I hope the steps from the article to update and rebuild initrd image in CentOS/RHEL 7 and 8 Linux was helpful. So, let me know your suggestions and feedback using the comment section.

***References:**[How to extract and repackage the anaconda installation initrd.img from Red Hat Enterprise Linux 7 DVD iso media?](https://access.redhat.com/solutions/3766431)*