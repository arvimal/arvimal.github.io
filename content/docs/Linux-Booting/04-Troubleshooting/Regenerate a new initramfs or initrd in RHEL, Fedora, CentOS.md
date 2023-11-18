---
date created: 13-11-2022, Sunday, 07:27 PM
tags:
  - rhel
  - boot
  - initramfs
  - initrd
  - dracut
  - mkinitrd
---

<https://wiki.centos.org/TipsAndTricks/CreateNewInitrd>

If you have changed a motherboard or moved a disk to a different system it may fail to boot due to the lack of appropriate drivers in the initial RAM disk image (initramfs for CentOS 6, initrd for CentOS 5).

## Boot in Rescue Mode

1. Boot from a CentOS installation disc (for example, CD #1 or DVD).
2. Type "**linux rescue**" at the "**boot:**" prompt.
3. Mount all filesystems in read-write mode.

## Create the New Initramfs or Initrd

Change root to real root ('/') on your hard disk and make the new initramfs or initrd.

```
mount --bind /proc /mnt/sysimage/proc
mount --bind /dev /mnt/sysimage/dev
mount --bind /sys /mnt/sysimage/sys
chroot /mnt/sysimage
```

For **CentOS 7** and multipathed root ('/') issue the following before chroot-ing to '/mnt/sysimage':

```
mount --bind /run /mnt/sysimage/run
systemctl start multipathd.service
```

For **CentOS 6**:

* Create a backup copy of the current initramfs:

  ```
  cp -p /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.bak
  ```

* Now create the initramfs for the current kernel:

  ```
  dracut -f 
  ```

* If you need to build it for a specific kernel version (replace the version appropriately):

  ```
  dracut -f /boot/initramfs-2.6.32-358.el6.x86_64.img 2.6.32-358.el6.x86_64
  ```

* One useful option you might want to add is -H (--hostonly). With this option dracut installs only what is needed for booting your system. Otherwise dracut by default adds many drivers to the initramfs making its size larger than necessary. Many other options may be exercised. Please see **man dracut**, **man dracut.conf** and the [upstream Deployment Guide](http://docs.redhat.com/docs/en-US/Red_Hat_Enterprise_Linux/6/html/Deployment_Guide/sec-Verifying_the_Initial_RAM_Disk_Image.html).

For **CentOS 5**:

* Create a backup copy of the current initrd:

  ```
  cp -p /boot/initrd-$(uname -r).img /boot/initrd-$(uname -r).img.bak
  ```

* Now create the initrd for the current kernel:

  ```
  mkinitrd -f -v /boot/initrd-$(uname -r).img $(uname -r)
  ```

* If you need to build it for a specific kernel version (replace the version appropriately):

  ```
  mkinitrd -f -v /boot/initrd-2.6.18-371.el5.img 2.6.18-371.el5
  ```

* If you are migrating a physical machine to a virtual one using the Xen hypervisor, replace the last command above with:

  ```
  mkinitrd --with-xenblk initrd-2.6.18-371.el5xen.img 2.6.18-371.el5xen
  ```

* Many other options may be exercised, such as adding non-loaded modules manually. See **man mkinitrd** for details. It may be necessary to modify /boot/grub/grub.conf and/or /etc/fstab depending on the details of your installation. This depends on your use of LABEL and/or UUID versus physical devices in the files, and is too complex an issue to get into in any detail in a [TipsAndTricks](https://wiki.centos.org/TipsAndTricks) article.

Reboot

```
cd /
sync
telinit 6
```

This page was created by [PhilSchaffner](https://wiki.centos.org/PhilSchaffner). Other Wiki contributors are invited to make corrections, additions, or modifications.

The page was inspired by this [forum thread](https://www.centos.org/forums/viewtopic.php?t=16803). Please see the thread for additional discussion.
