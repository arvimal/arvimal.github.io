---
date created: 13-11-2022, Sunday, 07:22 PM
---

# Preliminary Work: Getting GRUB2 on a qemu disk

<https://codezen.org/viridis-ng/2012/08/31/preliminary-work-getting-a-grub2-on-a-qemu-disk/>

In this article, we’ll cover the very first step in writing a toy operating system: preparing a disk to boot your kernel from.

We’ll be using GRUB (GRand Unified Bootloader) version 2, which has plenty of nice features, is modern, and is what Linux uses so it’s very well tested.

## Assumptions

This is not a hand-holdy kind of write-up because this isn’t a hand-holdy subject. Before you start you should have a Linux machine running natively (unless you want to nest VMs which is a terrible idea for debugging). You should have `qemu` installed, preferably the kvm variant but that will be an unimportant distinction for quite awhile.

## Reasoning

### Why QEMU?

QEMU provides seamless KVM integration, and has a myriad of devices supported, and has GDB support. In my prior efforts I used [Bochs](http://bochs.sf.net/) which is a fine x86 emulator with a decent debugger, but it’s device selection is limited and I’ve become more familiar with QEMU in the intervening years.

### Why GRUB2?

GRUB is a solid, flexible bootloader. Traditionally, toy OSes target floppy like devices and part of the learning experience is writing that initial 512 bytes of assembly and the boot signature. I’ve written too many of those already, but the honest truth is that bootloaders aren’t part of the kernel and so they are uninteresting.

The second reason is that using GRUB allows us to be hosted on a real filesystem (we use an ext2 boot partition in this article) and with a real file-format (ELF) which comes in handy when manipulating the FS from Linux or using debug tools on the binary.

The last reason is that GRUB provides an abstraction from BIOS interrupts like e820 to count memory.

And, as for why version 2 specifically, for no other reason than it’s the latest.

## Create a QEMU disk

QEMU comes with a nice tool to create disks. We’re going to use the **raw** format because it will allow us to easily mount portions of the disk later with `losetup`.

First, create a decent size raw disk. I made mine 10G which is overkill for our purposes, but I’ve got plenty of room to spare.

```
jack@sagan:$ qemu-img create -f raw disk.img 10g

```

## Grab a Linux ISO

I tried and tried to convince my local copy of the grub utilities to install to a partition I created in the disk.img but when booting in qemu it failed to find the secondary boot files, tossed a message and dumped to a useless rescue prompt. In the end I decided it would be 10x easier to install from within the QEMU environment so that all of the device maps and IDs would naturally sort themselves out.

I chose to install from the [Arch Linux](http://archlinux.org/) [install CD](http://archlinux.org/download). In particular the August 2012 version, although future installation media will probably be okay.

## Boot the ISO in QEMU

Use the following command to boot QEMU with the Linux ISO, and the disk image.

```
jack@sagan:$ qemu -hda disk.img -cdrom [path to Linux ISO] -m 1024

```

This should get you to a prompt. At this point, the architecture (x86/x86_64) doesn’t matter as the GRUB media is identical.

## Setup the Disk

I used `cfdisk` to create two new primary partitions. 1 100MB partition for boot and 1 with the rest.

```
livecd:# cfdisk /dev/sda

```

Then create your filesystems. I want to use ext2 for the /boot and ext4 for the other partition because later I plan on having some fun with ext4.

```
livecd:# mkfs.ext2 /dev/sda1
...
livecd:# mkfs.ext4 /dev/sda2

```

## Install GRUB2 to the Disk

Mount the boot FS to /mnt

```
livecd:# mount /dev/sda1 /mnt

```

And then use `grub-install` to copy the relevant files and setup the MBR. We specify boot directory because otherwise `grub-install` will try to use /boot on the live CD and will fail to map that to a usable device.

```
livecd:# grub-install --boot-directory=/mnt /dev/sda

```

It should report no errors.

Finally, unmount the boot FS

```
livecd:# umount /mnt

```

And you can either shutdown like it’s a real machine or just kill QEMU afterwards.

## Testing the Boot

Now, restart the QEMU without the ISO argument to see if you can get to a GRUB prompt.

```
jack@sagan:$ qemu -hda disk.img -m 1024

```

Almost instantaneously you should get a window that looks like:

![[/2012-08-30-184653_718x880_scrot-e1346370405695.png]]

## Mounting Partitions from Linux

Now that we have a bootloader in place, hopefully we won’t have to use any other outside help in our QEMU environment. However, obviously the next step requires we have a file to boot. That’s for the next post, but to get to that point we need to be able to copy the file into our disk, which is complicated by the fact that it’s not just a stupid filesystem image, but a full disk image with a partition table and everything.

To mount the partitions we need to use `losetup` to create a loopback devices for just the relevant parts of the image file. Conveniently `losetup` takes the `-o` (offset) and `--sizelimit` arguments which allow you to loopback map a portion of a file.

First, let’s take a look at the output of `fdisk`‘s `p` (print) command to get the byte offsets and sizes of our partitions.

```
jack@sagan:$ fdisk disk.img
...
Command (m for help):p
Disk disk.img: 10.7 GB, 10737418240 bytes
255 heads, 63 sectors/track, 1305 cylinders, total 20971520 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000000

   Device Boot      Start         End      Blocks   Id  System
disk.img1              63      192779       96358+  83  Linux
disk.img2          192780    20971519    10389370   83  Linux

```

The important things here are the partitions starts and ends, and the unit size.

Our first partition, the ext2 boot partition that GRUB cares about, starts at byte `(63 * 512 =) 32256`. It ends at byte `(192779 * 512) = 98702848`. So it’s size, in bytes is `98702848 - 32256 = 98670592`

We can then use the starting offset and the size to bind a loopback device to that portion of the disk.img.

```
jack@sagan:$ sudo losetup -f -o 32256 --sizelimit 98670592 disk.img

```

The `-f` flag lets losetup use the first available loopback device. `/dev/loop0` is the likely choice, but you can check it with `losetup -a` to list the current loopback devices.

```
jack@sagan:$ losetup -a
/dev/loop0: []: (/path/to/disk.img), offset 32256, sizelimit 98670592

```

Now that the loopback is setup, you can mount the filesystem like any other block device and it should work without error and even show the grub files placed there from the ISO.

```
jack@sagan:$ sudo mount /dev/loop0 /mount/point
jack@sagan:$ ls /mount/point/
grub  lost+found
jack@sagan:$ ls /mount/point/grub
fonts  grubenv  i386-pc  locale  themes

```

In the next post we’ll be loading our kernel to `/mount/point/` and using the GRUB prompt to boot into it.
