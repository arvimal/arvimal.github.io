# Creating a SWAP space in Linux

<!--more-->
**Adding Swap Space:**

Sometimes it is necessary to add more swap space after installation. For example, you may upgrade the amount of RAM in your system from 64 MB to 128 MB, but there is only 128 MB of swap space. It might be advantageous to increase the amount of swap space to 256 MB if you perform memory-intense operations or run applications that require a large amount of memory.

You have two options: add a swap partition or add a swap file. It is recommended that you add a swap partition, but sometimes that is not easy if you do not have any free space available.

To add a swap partition (assuming /dev/hdb2 is the swap partition you want to add):

1)  The hard drive can not be in use (partitions can not be mounted, and swap space can not be enabled). The easiest way to achieve this it to boot your system in rescue mode. Refer to Chapter 8 for instructions on booting into rescue mode. When prompted to mount the filesystem, select Skip. Alternately, if the drive does not contain any partitions in use, you can unmount them and turn off all the swap space on the hard drive with the swapoff command.

2)  Create the swap partition using parted or fdisk. Using parted is easier than fdisk; thus, only parted will be explained. To create a swap partition with 'parted:'. At a shell prompt as root, type the command parted /dev/hdb, where /dev/hdb is the device name for the hard drive with free space. At the (parted) prompt, type print to view the existing partitions and the amount of free space. The start and end values are in megabytes. Determine how much free space is on the hard drive and how much you want to allocate for a new swap partition. At the (parted) prompt, type mkpartfs part-type linux-swap start end, where part-type is one of primary, extended, or logical, start is the starting point of the partition, and end is the end point of the partition.

>             Warning     Warning \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
>
> Changes take place immediately; be careful when you type.
>
> Exit parted by typing quit.

3) Now that you have the swap partition, use the command mkswap to setup the swap partition. At a shell prompt as root, type the following:

> \# mkswap /dev/hdb2

4) To enable the swap partition immediately, type the following command:

> \# swapon /dev/hdb2

5) To enable it at boot time, edit /etc/fstab to include:

> /dev/hdb2               swap                    swap    defaults        0 0

The next time the system boots, it will enable the new swap partition.

6) After adding the new swap partition and enabling it, make sure it is enabled by viewing the output of the command cat /proc/swaps or free.

To add a swap file: -------------------------- 1.  Determine the size of the new swap file and multiple by 1024 to determine the block size. For example, the block size of a 64 MB swap file is 65536.

2.  At a shell prompt as root, type the following command with count being equal to the desired block size:

> \# dd if=/dev/zero of=/swapfile bs=1024 count=65536

3\. Setup the swap file with the command:

> \# mkswap /swapfile

4\. To enable the swap file immediately but not automatically at boot time:

> \# swapon /swapfile

5\. To enable it at boot time, edit /etc/fstab to include:

> /swapfile               swap                    swap    defaults        0 0

The next time the system boots, it will enable the new swap file.

6\. After adding the new swap file and enabling it, make sure it is enabled by viewing the output of the command cat /proc/swaps or free.

