---
date created: 13-11-2022, Sunday, 07:25 PM
---

# The Kernel Newbie Corner: "initrd" and "initramfs"-What's Up With That? - Linux.com

<https://www.linux.com/tutorials/kernel-newbie-corner-initrd-and-initramfs-whats/>

This week, I’m not going to write a formal column so much as just free associate a bit regarding an exchange we had recently on the Kernel Newbies mailing list regarding the ideas of initrd and initramfs, and what they’re for and, most importantly, how they differ. And that’s where we might get deliberately vague since different people use the terminology differently, so I’ll present *my* view of the terms and the way I use them, whereupon you’re free to disagree vehemently.

*(The archive of all previous “Kernel Newbie Corner” articles can be found [here](http://cli.gs/WG6WYX).)*

*This is ongoing content from the Linux Foundation training program. If you want more content, please consider signing up for one of [these classes](http://www.linuxfoundation.org/training).*

## So… What Are They?

If we can be a little sloppy for a minute or two, both of those concepts refer to a simple idea — that of an “early userspace” root filesystem that can be used to get at least the minimum functionality loaded in order to let the boot process continue. There’s a lengthy explanation in the kernel source tree in the file Documentation/filesystems/ramfs-rootfs-initramfs.txt, but I’ll try to simplify that just a bit.

In a nutshell, when your bootloader (GRUB?) loads your Linux kernel, it is of course the kernel’s job to finish the boot process. But to do so, it might require particular drivers to be able to work with, say, hardware RAID controllers, or a network, and so on. And depending on where those critically important drivers are, the kernel might not have the ability to load them; hence, the creation of a *preliminary* root file system that would contain just enough in the way of loadable modules to give the kernel access to the rest of the hardware.

Quite simply, it’s the bootloader’s job to pass control to the kernel, hand it the “initrd” (initial ram disk), let the kernel mount it and get what it needs, whereupon the kernel can toss the initrd and replace it with the *real* root filesystem. With me so far?

## So Tell Me About the “initrd”

Almost everyone is familiar with the use of an initrd file, since most of you have undoubtedly seen one or more of them sitting in your /boot directory. If you’re using the GRUB bootloader, you identify which initrd image matches which kernel in your GRUB configuration file thusly:

```
title Fedora (2.6.31)         
root (hd0,0)         
kernel /vmlinuz-2.6.31 ro root=/dev/mapper/f11-root nomodeset rhgb quiet         initrd /initrd-2.6.31.img
```

That “stanza” tells GRUB which initrd file to hand to each kernel at boot time. Simple enough. But what’s *in* that initrd file? I’m glad you asked.

Once upon a time, those files were compressed filesystem image files, most likely ext2-format filesystems. This meant that, to see their contents (and who hasn’t wanted to peek inside them?), you would have to first gunzip them (easy), then *mount* them somewhere, which was *not* so easy without being root, which meant that regular users were denied the fun of poking around inside those files to get a better understanding of the early boot process. But things have changed.

Nowadays, those files are almost certainly cpio-format files, which means they *are* perusable by regular users. Well, OK, not really since they’re read-protected so, sadly, you still have to be root for *that* part. But assuming you can get read access to one of those files, you could:

```
# gunzip -c /boot/initrd-2.6.31.img > /tmp/my_initrd $ cpio -it < /tmp/my_initrd         [examine contents] lib lib/udev lib/udev/console_init lib/firmware lib/firmware/radeon lib/firmware/radeon/RV730_me.bin ... snip ... lib/modules lib/modules/2.6.31 lib/modules/2.6.31/radeon.ko lib/modules/2.6.31/modules.isapnpmap ... and so on and so on ... $ cd [somewhere]                    [in preparation for unloading] $ cpio -i < /tmp/my_initrd          [unload]
```

And now that you’ve unloaded your initrd file, you can peruse its root file system-like contents at your leisure to get a better understanding of the early part of the boot process, before the *real* root file system comes into play.

But wait. There’s more.

## Where did that initrd file come from?

Typically, when you install a new kernel, you’ll get a matching initrd file automatically, but you can always build one manually using the mkinitrd command. I’m not going to get into horrendous detail with this command. If you truly want to play with it, feel free. Create a new initrd file or two, then pull it apart to see what’s inside.

But here’s where things get just a bit more interesting.

## OK, So What’s the “initramfs” Thingy?

And here’s where we might part ways regarding terminology. I will always refer to the above file as the “initrd” file since, in my opinion, the “initramfs” early root file system is something quite different.

Quite simply, the “initramfs” (initial RAM file system) is what I call an even *earlier* potential root file system that you can build *into* the kernel image itself. And because of its location (internal to the kernel), it will (if it exists) take precedence. So how do you add an internal root file system to your kernel image itself?

Assuming you’re building your own kernel, you need to select the following configuration option, defined in the kernel source tree in the init/Kconfig file:

```
config BLK_DEV_INITRD         bool "Initial RAM filesystem and RAM disk (initramfs/initrd) support"         depends on BROKEN || !FRV         help           The initial RAM filesystem is a ramfs which is loaded by the           boot loader (loadlin or lilo) and that is mounted as root           before the normal boot procedure. It is typically used to           load modules needed to mount the "real" root file system,           etc. See <file:Documentation/initrd.txt> for details.           If RAM disk support (BLK_DEV_RAM) is also included, this           also enables initial RAM disk (initrd) support and adds           15 Kbytes (more on some other architectures) to the kernel size.           If unsure say Y.
```

And based on what you read above, you should notice that this is the single option that selects support for *both* types of early root file systems. There is no (apparent) way to select support for only one or the other, and I’ve occasionally wondered if there would be any value in extending the configuration to allow that. In any event, the way it stands, you either get support for both or neither.

## So How Do I Identify What I Want in My “initramfs”?

Easy. If you look again in init/Kconfig right under the text you see above, you’ll see:

```
if BLK_DEV_INITRD source "usr/Kconfig" endif
```

which means that that single selection brings the entire top-level kernel usr directory into play, which represents everything you need to build your early userspace initramfs content that will be embedded in the kernel.

Take a look at the configuration options in usr/Kconfig, which includes how to specify what you want in your initramfs:

```
config INITRAMFS_SOURCE         string "Initramfs source file(s)"         default ""         help           This can be either a single cpio archive with a .cpio suffix or a           space-separated list of directories and files for building the           initramfs image.  A cpio archive should contain a filesystem archive           to be used as an initramfs image.  Directories should contain a           filesystem layout to be included in the initramfs image.  Files           should contain entries according to the format described by the           "usr/gen_init_cpio" program in the kernel tree.           When multiple directories and files are specified then the           initramfs image will be the aggregate of all of them.           See <file:Documentation/early-userspace/README> for more details.           If you are not sure, leave it blank.
```

In short, you can build (another) cpio-format image file that represents what you want in your initramfs, and just mention it during your kernel configuration process. After that, you can build your kernel, at which point the *final* cpio-format file that was used for your initramfs will be sitting in the generated file usr/initramfs_data.cpio, and you can use the same extraction commands from early on to examine *its* contents as well.

## But What if I Don’t Give any initramfs Contents?

Even if you select initrd/initramfs support, there’s nothing that *demands* that you have to whip up a cpio-format file to be used to build your kernel initramfs. But even if you don’t, you’ll still have one — it just won’t be very exciting.

If you examine the kernel shell script scripts/gen_initramfs_list.sh, you can examine just how that cpio-format initramfs file is created. And buried in there somewhere is the definition of the “default” initramfs if you choose not to specify any contents:

```
default_initramfs() {     cat <<-EOF >> ${output}         # This is a very simple, default initramfs         dir /dev 0755 0 0         nod /dev/console 0600 0 0 c 5 1         dir /root 0700 0 0         # file /kinit usr/kinit/kinit 0755 0 0         # slink /init kinit 0755 0 0     EOF }
```

The above should be self-explanatory — your default initramfs will contain all of two objects — a /root directory and a /dev/console special device file. That’s not terribly exciting, which means that if you don’t design a usable initramfs for your kernel, you’d *better* have a practical initrd file to pick up the slack.

## Anything Else?

Plenty, and the comments section is open for discussion. As a final observation, if you really want to see the code for the early boot process, that’s all in the top-level init directory, where you can see source files whose names *clearly* reflect that they’re doing *something* with mounts and root file systems and initrds and so on.

Perhaps the most interesting observation is this snippet from the Makefile in that directory, which shows what happens depending on whether you even select support for initrd/initramfs;

```
ifneq ($(CONFIG_BLK_DEV_INITRD),y) obj-y                          += noinitramfs.o else obj-$(CONFIG_BLK_DEV_INITRD)   += initramfs.o endif
```

Obviously, depending on your selection, only one of two source files will be compiled into your kernel image. You can follow the more involved of the two — initramfs.c — to see how the kernel uses that initramfs image, but it’s at least as educational to see what happens if the kernel has no such support whatsoever. Consider the code from noinitramfs.c:

```
/*  * Create a simple rootfs that is similar to the default initramfs  */ static int __init default_rootfs(void) {         int err;         err = sys_mkdir("/dev", 0755);         if (err < 0)                 goto out;         err = sys_mknod((const char __user *) "/dev/console",                         S_IFCHR | S_IRUSR | S_IWUSR,                         new_encode_dev(MKDEV(5, 1)));         if (err < 0)                 goto out;         err = sys_mkdir("/root", 0700);         if (err < 0)                 goto out;         return 0; out:         printk(KERN_WARNING "Failed to create a rootfsn");         return err; }
```

In other words, even if you don’t select initramfs support, you’re still going to get one built manually at boot time. Cute, no?

At this point, I’ll open up the comments section so feel free to discuss, debate or just plain argue. There is, in fact, quite a bit more that can be written about the entire early userspace process, and I’ll take a couple days to decide if I want to follow this up with a Part Two, if there’s sufficient interest.
