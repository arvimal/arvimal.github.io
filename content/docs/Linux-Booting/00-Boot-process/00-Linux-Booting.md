# The Linux Boot process

**1. Power up the machine**

The Boot process starts when a user powers up the machine.

**2. Power supply starts up, and regulates itself into the operating voltage.**

This may take less than a millisecond.

**3. The Power supply system sends the [PowerGood](https://en.wikipedia.org/wiki/Power_good_signal) signal to the Motherboard.**

* The ATX specification defines the Power-Good signal as a +5-volt (V) signal generated in the power supply when it has passed its internal self-tests and the output voltages have sthbilized.

* The Power Good signal (power-good) prevents a computer from attempting to operate on improper voltages and damage itself by alerting it to an improper power supply.

**4. The Motherboard starts the Processor, once it receives the `Power Good` signal.**

**5. The Processor resets its internal registers, and fill it with pre-defined information.**

* 80386 series and later series set the following registers and corresponding data.

```
        IP (16 Bit register)           - 0xfff0
        CS selector (16 Bit register)  - 0xf000
        CS base (16 Bit register)      - 0xffff0000
```

**6. The Processor starts in [Real Mode](https://en.wikipedia.org/wiki/Real_mode).**

* `Real` mode is characterised by a 20-bit segmented memory address space (giving exactly 1 MiB of addressable memory).
* This gives it unlimited direct software access to all addressable memory, the I/O addresses, and hardware.
* `Real` mode provides no support for memory protection, multitasking, or code privilege levels. Thus, all x86 CPUs start in `Real mode` with no memory protection, fixed 64 KiB segments, and only 20-bit (1024 KiB = 1 MiB) addressing.

**7. The x86 CPU adds both the**CS Selector**and**CS Base**register contents and expects to find the first instruction after reset, there.**

* All the registers, while in 8086, were 16-bit registers.
* This meant that only 64KiB addresses could be addressed in a single go.
* The CS (Code Segment) registers had two types (Selector and Base) each 16 bits long.
* These together (16 bits + 16 bits) were able to address 32 bit address locations.
* Hence, the 8086 and any x86 CPUs were able to address approximately 4GB of memory.
* Before starting up, the x86 CPU had cleared its registers and set it to the following values

```text
        IP (16 Bit register)           - 0xfff0
        CS selector (16 Bit register)  - 0xf000
        CS base (16 Bit register)      - 0xffff0000
```

Adding `CS Selector` and `CS Base` values gives `0xfffffff0`, which is `4 GB - 16 Bytes`.

```python3
In [4]: hex(0xffff0000 + 0xfff0)
Out[4]: '0xfffffff0'
```

This address is called the `Reset vector`. The reset vector is the default location a central processing unit will go to find the first instruction it will execute after a reset. The reset vector is a pointer or address, where the CPU should always begin as soon as it is able to execute instructions.

The address contains a `jump` instruction, which points to the BIOS entry point in a `Read-Only Memory` chip (ROM) on the Motherboard. The BIOS is initialised and it starts up.

**8. BIOS starts**

* Once the BIOS starts, it does the `Power-On Self Test` and verifies all hardware.
* Information on the bootable disk or boot order is maintained in the BIOS.
* If the boot device is a disk, the BIOS tries to find a boot sector. An HDD sector is 512 Bytes.
* On HDDs partitioned with MBR partitioning tables, the first 446 Bytes of the first sector contains the `BootStrap` code.
* On systems using GRUB, the first stage of GRUB is located here, and **is** the `Bootstrap` code.

**NOTE:**
    BIOS/UEFI cannot directly go ahead and read a disk, unless it has some way of addressing them. Almost all HDD manufacturers provide disk hardware that enable BIOS to utilise them, and access the HDD sectors through LBA (Logical Block Addressing). This is comparatively slow, but helps the BIOS to read the disks and pass control over to a Boot Loader.

**9. BIOS hands over control to the `Boot Sector code` (aka `Master Boot Code`) (GRUB Stage1)**

* BIOS loads the first sector (Sector #0 of 512B) of the bootable disk into RAM.
* It reads the `Bootstrap` code (`boot.img`, in case of GRUB) residing within the first 446 Bytes.
* The control is passed on to the `Bootstrap` code (boot.img) (GRUB Stage1), and executes in memory.

**10. GRUB starts**

* Once BIOS reads the first sector of the bootable disk via LBA addressing method, the Boot Strap code is called and executed (GRUB Stage1).

* Stage 1 : (`boot.img` in MBR BootStrap code area, ie.. Sector #0)

  * `boot.img` is stored in the master boot record (MBR) or optionally in any of the volume boot records (VBRs), and addresses the next stage by an LBA48 address (thus, the 1024-cylinder limitation of GRUB legacy is avoided).
  * The Stage1 is configured (automatically) to load the first sector of core.img (core.img = Stage 1.5)

* Stage 1.5: (`core.img` - Sector #1 to #62) (Can contain drivers to access partitions with Filesystems, for Grub)

  * `core.img` is by default written to the sectors between the MBR and the first partition, when these sectors are free and available.
  * For legacy reasons, the first partition of a hard drive does not begin at sector #1 (counting begins with 0) but starts at sector #63. This leaves 62 sectors of empty space not part of any partition or file system, and therefore not prone to any problems related with it.
  * Once executed, `core.img` will load its configuration file and any other modules needed, particularly file system drivers; at installation time, it is generated from diskboot.img and configured to load the stage 2 by its file path.

* Stage 2: (In /boot/grub/)

  * GRUB uses the filesystem drivers to access the filesystem partitions, and reads `grub.conf`.
  * Files belonging to Stage 2 are all in `/boot/grub`, which is a subdirectory of the /boot directory
  * This includes the configuration file `grub.cfg`, the kernels (vmlinuz), and the initrd files etc..
  * The GRUB menu as per `grub.conf` is shown and user selects a kernel to boot from.

**11. GRUB loads the selected/default kernel loads, and initrd.**

* GRUB reads the entry for the kernel selected (by the user or default kernel), and loads the kernel mentioned with directive `linux16` to memory.
* The kernel takes into consideration the kernel parameters set for `vmlinuz`, and acts accordingly.

---

**NOTE:** Some info on `grub.conf` and its parameters.

* The location where GRUB searches for the kernel and initrd, is set with the parameter `set root='hd0, msdos1'`. This is the GRUB root, or the location where GRUB intends to find the kernel and initrd.
* The `search` parameter in grub.conf sets the way the GRUB root should be checked, and the disk UUID it should check. This filesystem is where GRUB expects to find the kernel and initrd.
* The `search` keyword follows with the `vmlinuz` path, and initrd path. A vmlinuz and kernel parameters example:

```
`/vmlinuz-3.10.0-693.el7.x86_64 root=/dev/mapper/rhel_dell--r430--19-root ro crashkernel=auto rd.lvm.lv=rhel_dell-r430-19/root rd.lvm.lv=rhel_dell-r430-19/swap rhgb quiet LANG=en_US.UTF-8`
`initrd16 /initramfs-3.10.0-693.el7.x86_64.img`
```

* Note that the kernel parameters mention `ro` (read-only). This is normal, and it instructs the kernel to read the root filesystem as read-only so that the filesystem checker can run its checks safely. After the filesystem check, the root filesystem will be mounted as read-write.
* If the kernel comes upon any parameters that it doesn't understand, it saves it and passes it to `init` (or systemd), in order to process later.
* If the vmlinuz path starts with a slash ('/') as in `/vmlinuz-3.10.0-693.el7.x86_64`, it means that the /boot/ partition is different than the root partition ('/'). If /boot/ was on the same partition as root ('/'), the entry would have been `/boot/vmlinuz-3.10.0...`.

---

* Grub (not the kernel) loads both the `Kernel` and the `initrd` file, as listed in `grub.conf`.
* Initrd contains the necessary drivers for the kernel, to access the connected devices as well as form a virtual filesystem in memory.
* With a virtual filesystem running in memory, the kernel initializes `/sbin/init` (which was part of the initrd file).

**12. `init` or `systemd` starts**

* The kernel looks for an `init` binary in the following locations:
  * /sbin/init
  * /etc/init
  * /bin/init
  * /bin/sh

>**NOTE:**
>If the directive `init=<path>` is passed to grub via grub.conf (or
>editing at boot time),Grub loads that specific binary as the first process.
>Else, it looks for an `init` binary at the locations above.

* `/sbin/init` starts
  * On systemd machines, `/sbin/init` is usually a symlink to `/usr/lib/systemd/systemd`.
  * `init` reads `/etc/inittab` for run levels, and go to the specific runlevel locations at `/etc/init.d/` to start the scripts marked to startup in that level.
  * On Systemd machines, `Systemd` looks for the targets it has to reach (/usr/lib/systemd/system/default.target), and starts the units for it. By default, Systemd is configured to reach the `multi-user` target, and starts the services for it, and presents the login prompt.

**13. `mgetty`, `systemd-getty-generator`, `login`, and `PAM`**

* On SystemV machines with older `init`, `init` loads `mgetty` or `agetty`.
  * `agetty` takes control of the `login` binary
  * It presents a login prompt to the user, in the virtual console.
  * The user login credentials are passed to PAM settings in /etc/pam.d/
  * PAM checks /etc/passwd, and /etc/shadow for user info.
  * If the user info is correct, the shell set in /etc/passwd is spawned.
  * If not, `login` terminates and control is passed back to `agetty`.
  * `agetty` takes control over `login` and presents the user with a prompt.

* On Systemd machines, `systemd` loads `systemd-getty-generator`.
  * `systemd-getty-generator` takes control over the `login` binary.
  * The rest are similar to the sequence above.

---

---

### Notes

**1. History of Real Mode**

1. The _80286_ series of processors introduced the `Protected Mode` of operation.
2. `Real Mode` was the operational mode available before `Protected Mode` emerged in 80826.
3. `Protected Mode` enabled features such as virtual memory, paging etc.., and these were not available in `Real Mode` mode of operation.
4. Backward compatibility is a design decision in x86 series, hence it was a requirement to get any software written for processor series before 80286 to be able to run on any x86 series. The existing system software which were written for `Real Mode` would have to be re-written to use the `Protected Mode`.
5. Hence, to maintain backward compatibility with all previous series as well as for using the existing system software, all x86 processors from `80286` till the latest x86 64-bit processors (those using Protected mode), start in `Real Mode`.
6. The Processor switches from `Real Mode` to `Protected Mode` after the system software sets up a few descriptor tables and enables the Protection Enable (PE) bit in the control register 0 (CR0).

**2. Why was the change to Protected mode required?**

1. The Intel 8086, the predecessor to the 80286, was originally designed with a 20-bit address bus for its memory.
2. This allowed the processor to access 220 bytes of memory, equivalent to 1 megabyte.
3. At the time, 1 MB of memory was considered a relatively large amount of memory, so the designers of the IBM Personal Computer reserved the first 640 kilobytes for use by applications and the operating system, and the remaining 384 kilobytes for the BIOS and memory for add-on devices.
4. As the cost of memory decreased and memory use increased, the 1 MB limitation became a significant problem. Intel intended to solve this limitation along with others with the release of the 286, through the `Protected Mode`.

**3. How does Real mode address memory?**

1. `Real Mode` was the only mode available in the series prior 80286, ie.. 8086.
2. This series had 20-bit address buses capable of addressing 1MiB of Memory, but had only 16-bit CPU registers that could load upto 64KiB of memory at a time.
3. This meant that, even though the bus had the width to accomodate a larger bit size and access the memory, the Processor registers were not big enough to load the data in a single go.
4. Hence, 8086 processors used a method known as [Memory Segmentation](https://en.wikipedia.org/wiki/Memory_segmentation).
5. In 8086, Memory segmenatation worked by creating 64KiB chunks of the 1MiB data space, and loading it as required.

**4. 80826 series provides memory protection compared to 8086, what is it?**

1. Memory segmentation is the process of dividing the system memory into sections.
2. 8086 series used this technique to address a memory of 1MiB when its registers were only capable of storing 64KiB.
3. In a system that uses memory segmentation, a reference to the memory location would include a value that points to a segment and an offset. This enables the processor to read the entire segment.
4. The `Memory Management Unit` is responsible for mapping the segments to the actual locations in RAM, as well as checking the access permissions for that specific memory location.
5. The Memory Segmentation used by 8086 did not provide any protection. ie. it didn't have a mechanism to prevent access to specific memory segments. Any software running on these processors can access any memory segments as it chose, even if those were not in use by the said system software.
6. The lack of Memory protection in 8086 prevented features such as Virtual Memory from being realized.
7. 80826 came with the `Protected Mode` of operation which brought in memory protection and features such as virtual memory, paging etc.
8. As said earlier, due to backward compatibility, 80286 still started up in `Real mode` even though it came with `Protected Mode`.

**5. Master Boot Record**

1. A master boot record (MBR) is a special type of boot sector at the very beginning of a partitioned storage device.
2. The MBR holds the information on how the partitions are organized on that medium.
3. The organization of the partition table in the MBR limits the maximum addressable storage space of a disk to 2 TiB (232 × 512 bytes)
4. The first `446 Bytes` of the sector of an MBR partitioned disk, contains the `Bootstrap` code.
5. The next `four 16 Bytes` contains the four partition entries. Hence the limit of four primary partitions.
6. The final `two bytes` contain the `Boot signature`, which denotes the disk is bootable and acts as an indicator that the sector is ending here.

Thus, **Total size =`446 + (4 x16) + 2` = 512 Bytes**

**NOTE:** GPT (Guid Partition Table) is a replacement to MBR. Some of the differences between MBR and GPT are:

* MBR uses 32-bit addresses, hence is limited to read upto 2TiB of disk space (2**32 - 1)
* GPT uses 64-bit addresses and can address larger disks.
* MBR uses the Cylinder-Head-Sector (CHS) mode for disk access, which is not always correct due to outer cylinders being large than inner ones and thus the number of sectors per cylinder being different.
* GPT uses Logical-Block-Address (LBA) mode which is more accurate than GPT.

* GPT still maintains the MBR structure in Sector #0 to maintain backward compatibility. ie.. in LBA #0.
* GPT header is in LBA #1, the Partition table is at LBA #2, and the filesystem starts from LBA #34.

**6. Why does GRUB have multiple stages?**

1. GRUB has multiple stages, `Stage 1` being in the `Bootstrap` section of the first sector of MBR formatted bootable disk.
2. The Bootstrap code has only a space of around 446 Bytes.
3. This is enough for simple bootloaders, but not so for bootloaders that support Menu-drive selection, supports multiple filesystems etc.
4. Hence, the first stage of Grub exists in the Bootstrap code area, and the remaining at multiple locations such as the sectors between Sector #0 and Filesystem partition, as well as the Active partition.
5. Although every MBR formatted HDD contains an MBR, the master boot code is used only if the disk contains the active, primary partition.

**7. Difference between GRUB1 (Legacy) and GRUB2**

1. GRUB1 works only on x86 and x86_64 architecture. GRUB2 works on multiple architectures including SPARC and PowerPC.
2. GRUB1 supported only MBR and BIOS, while GRUB2 supports MBR, GPT, EFI, BIOS, OpenFirmware etc..
3. GRUB1 supported boot from normal filesystems, while GRUB2 supports reading LVM, RAID etc..
4. GRUB1 could only read a few filesystems such as EXT, XFS, JFS, FAT, ReiserFS etc.., while GRUB2 supports additional FS such as Apple FS, NTFS etc.

**8. Difference between MBR and GPT partition methods**

1. MBR (also called msdos partitions) uses 32-bits to store Block (LBA) addresses. For HDDs with 512 byte sectors, the MBR partition table entries allow a single partition upto 2TB.
2. GPT (Guid Partition Table) use logical block addressing (LBA) in place of the historical cylinder-head-sector (CHS) addressing.
3. On a system using GPT, the MBR is still maintained for backward compatibility. The protective MBR is contained in LBA 0, the GPT header is in LBA 1, and the GPT header has a pointer to the partition table, or Partition Entry Array, typically LBA 2.
4. The UEFI specification stipulates that a minimum of 16,384 bytes, regardless of sector size, be allocated for the Partition Entry Array.
5. On a disk having 512-byte sectors, a partition entry array size of 16,384 bytes and the minimum size of 128 bytes for each partition entry, LBA 34 is the first usable sector on the disk.

**9. Difference between BIOS and EFI firmware systems**

**10. Troubleshooting GRUB**

1. Press `e` from GRUB menu, to enter the GRUB configuration and edit it.
2. Check the GRUB root where GRUB checks for the UUID, at the __set root=`hd<X>, <type>`__ parameter. The `type` would be usually `msdos` for MBR partitions and `gpt` for GPT partitions.
3. Press `Ctrl + C` to access the GRUB command prompt.
   * `ls` and `ls -l` (for more details) to list the partitions on the disks, on the machine.
4. Update/Edit grub.cfg
   * Any changes to grub.cfg won't be permanent. Hence, don't directly edit it.
   * Add changes in /etc/default/grub
   * Run `grub2-mkconfig > /etc/grub2.cfg` to update the changes to grub2.cfg.

5. GRUB 2 works as:

* /etc/default/grub contains customizations
* /etc/grub.d/ scripts contain GRUB menu information and operating system boot scripts.
* When the command `grub2-mkconfig > /etc/grub2.cfg` is run, it reads the contents of the grub file and the grub.d scripts and creates the grub.cfg file.

---

---

### Appendix

1. <https://en.wikipedia.org/wiki/Power_good_signal>
2. <https://en.wikipedia.org/wiki/Real_mode>
3. <https://en.wikipedia.org/wiki/Protected_mode>
4. <https://en.wikipedia.org/wiki/Memory_segmentation>
5. <https://en.wikipedia.org/wiki/Master_boot_record>
6. <https://technet.microsoft.com/en-us/library/cc976786.aspx>


---
date created: 13-11-2022, Sunday, 04:18 PM
---

# Arch boot process

<https://wiki.archlinux.org/index.php/Arch_boot_process#Boot_loader>

Since each OS or vendor can maintain its own files within the [EFI system partition](https://wiki.archlinux.org/index.php/EFI_system_partition) without affecting the other, multi-booting using UEFI is just a matter of launching a different EFI application corresponding to the particular operating system's boot loader. This removes the need for relying on [chain loading](https://en.wikipedia.org/wiki/Chain_loading) mechanisms of one [boot loader](https://wiki.archlinux.org/index.php/Arch_boot_process) to load another OS.

See also [Dual boot with Windows](https://wiki.archlinux.org/index.php/Dual_boot_with_Windows).

A boot loader is a piece of software started by the firmware ([BIOS](https://en.wikipedia.org/wiki/BIOS) or [UEFI](https://wiki.archlinux.org/index.php/UEFI)). It is responsible for loading the kernel with the wanted [kernel parameters](https://wiki.archlinux.org/index.php/Kernel_parameters), and [initial RAM disk](https://wiki.archlinux.org/index.php/Mkinitcpio) based on configuration files. In the case of UEFI, the kernel itself can be directly launched by the UEFI using the EFI boot stub. A separate boot loader or boot manager can still be used for the purpose of editing kernel parameters before booting.

**Warning:** A boot loader must be able to access the kernel and initramfs image(s), otherwise the system will not boot. Thus, in a typical setup, it must support accessing `/boot`. That means it must have support for everything starting from the block devices, stacked block devices (LVM, RAID, dm-crypt, LUKS, etc) and ending with the file system on which the kernel(s) and initramfs image(s) reside.

1. A [boot manager](https://www.rodsbooks.com/efi-bootloaders/principles.html). It can only launch other EFI applications, for example, Linux kernel images built with `CONFIG_EFI_STUB=y` and Windows `bootmgfw.efi`.

The [kernel](https://wiki.archlinux.org/index.php/Kernel) is the core of an operating system. It functions on a low level (kernelspace) interacting between the hardware of the machine and the programs which use the hardware to run. The kernel temporarily stops programs to run other programs in the meantime, which is known as [preemption](https://en.wikipedia.org/wiki/Preemption_(computing)). This creates the illusion of many tasks being executed simultaneously, even on single-core CPUs. The kernel uses the CPU scheduler to decide which program takes priority at any given moment.

## initramfs

After the [boot loader](https://wiki.archlinux.org/index.php/Arch_boot_process) loads the [kernel](https://wiki.archlinux.org/index.php/Kernel) and possible initramfs files and executes the kernel, the kernel unpacks the initramfs (initial RAM filesystem) archives into the (then empty) rootfs (initial root filesystem, specifically a ramfs or tmpfs). The first extracted initramfs is the one embedded in the kernel binary during the kernel build, then possible external initramfs files are extracted. Thus files in the external initramfs overwrite files with the same name in the embedded initramfs. The kernel then executes `/init` (in the rootfs) as the first process. The early userspace starts.

Arch Linux uses an empty archive for the builtin initramfs (which is the default when building Linux). See [mkinitcpio](https://wiki.archlinux.org/index.php/Mkinitcpio) for more and Arch-specific info about the external initramfs.

The purpose of the initramfs is to bootstrap the system to the point where it can access the root filesystem (see [FHS](https://wiki.archlinux.org/index.php/FHS) for details). This means that any modules that are required for devices like IDE, SCSI, SATA, USB/FW (if booting from an external drive) must be loadable from the initramfs if not built into the kernel; once the proper modules are loaded (either explicitly via a program or script, or implicitly via [udev](https://wiki.archlinux.org/index.php/Udev)), the boot process continues. For this reason, the initramfs only needs to contain the modules necessary to access the root filesystem; it does not need to contain every module one would ever want to use. The majority of modules will be loaded later on by udev, during the init process.

At the final stage of early userspace, the real root is mounted, and then replaces the initial root filesystem. `/sbin/init` is executed, replacing the `/init` process. Arch uses [systemd](https://wiki.archlinux.org/index.php/Systemd) as the default [init](https://wiki.archlinux.org/index.php/Init).

[init](https://wiki.archlinux.org/index.php/Init) calls [getty](https://wiki.archlinux.org/index.php/Getty) once for each [virtual terminal](https://en.wikipedia.org/wiki/Virtual_console) (typically six of them), which initializes each tty and asks for a username and password. Once the username and password are provided, getty checks them against `/etc/passwd` and `/etc/shadow`, then calls [login](https://wiki.archlinux.org/index.php/Arch_boot_process). Alternatively, getty may start a display manager if one is present on the system.

A [display manager](https://wiki.archlinux.org/index.php/Display_manager) can be configured to replace the getty login prompt on a tty.

In order to automatically initialize a display manager after booting, it is necessary to manually enable the service unit through [systemd](https://wiki.archlinux.org/index.php/Systemd). For more information on enabling and starting service units, see [systemd#Using units](https://wiki.archlinux.org/index.php/Systemd).

The login program begins a session for the user by setting environment variables and starting the user's shell, based on `/etc/passwd`.

The login program displays the contents of [/etc/motd](https://en.wikipedia.org/wiki/motd_(Unix)) (message of the day) after a successful login, just before it executes the login shell. It is a good place to display your Terms of Service to remind users of your local policies or anything you wish to tell them.

Once the user's [shell](https://wiki.archlinux.org/index.php/Shell) is started, it will typically run a runtime configuration file, such as [bashrc](https://wiki.archlinux.org/index.php/Bashrc), before presenting a prompt to the user. If the account is configured to [Start X at login](https://wiki.archlinux.org/index.php/Start_X_at_login), the runtime configuration file will call [startx](https://wiki.archlinux.org/index.php/Startx) or [xinit](https://wiki.archlinux.org/index.php/Xinit).

[xinit](https://wiki.archlinux.org/index.php/Xinit) runs the user's [xinitrc](https://wiki.archlinux.org/index.php/Xinitrc) runtime configuration file, which normally starts a [window manager](https://wiki.archlinux.org/index.php/Window_manager). When the user is finished and exits the window manager, xinit, startx, the shell, and login will terminate in that order, returning to [getty](https://wiki.archlinux.org/index.php/Arch_boot_process).


---
date created: 12-11-2022, Saturday, 08:55 PM
---

All modern personal computer [operating systems](https://en.wikipedia.org/wiki/Operating_system "Operating system") support GPT. Some, including [macOS](https://en.wikipedia.org/wiki/MacOS "MacOS") and [Microsoft Windows](https://en.wikipedia.org/wiki/Microsoft_Windows "Microsoft Windows") on the x86 architecture, support booting from GPT partitions only on systems with EFI firmware, but [FreeBSD](https://en.wikipedia.org/wiki/FreeBSD "FreeBSD") and most [Linux distributions](https://en.wikipedia.org/wiki/Linux_distribution "Linux distribution") can boot from GPT partitions on systems with either the BIOS or the EFI firmware interface.

The Master Boot Record (MBR) partitioning scheme, widely used since the early 1980s, imposed limitations for use of modern hardware. The available size for block addresses and related information is limited to 32 bits. For hard disks with 512‑byte sectors, the MBR partition table entries allow a maximum size of 2 [TiB](https://en.wikipedia.org/wiki/Tebibyte "Tebibyte") (2³² × 512‑bytes) or 2.20 [TB](https://en.wikipedia.org/wiki/Terabyte "Terabyte") (2.20 × 10¹² bytes).<sup id="cite_ref-UEFIFAQ_1-0"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-UEFIFAQ-1">[1]</a></sup>

In the late 1990s, [Intel](https://en.wikipedia.org/wiki/Intel "Intel") developed a new partition table format as part of what eventually became the [Unified Extensible Firmware Interface](https://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface "Unified Extensible Firmware Interface") (UEFI). The GUID Partition Table is specified in chapter 5 of the UEFI 2.8 specification.<sup id="cite_ref-UEFI2.8_2-0"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-UEFI2.8-2">[2]</a></sup> GPT uses 64 bits for logical block addresses, allowing a maximum disk size of 2<sup>64</sup> sectors. For disks with 512‑byte sectors, the maximum size is 8 [ZiB](https://en.wikipedia.org/wiki/ZiB "ZiB") (2<sup>64</sup> × 512‑bytes) or 9.44 [ZB](https://en.wikipedia.org/wiki/Zettabyte "Zettabyte") (9.44 × 10²¹ bytes).<sup id="cite_ref-UEFIFAQ_1-1"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-UEFIFAQ-1">[1]</a></sup> For disks with 4,096‑byte sectors the maximum size is 64 [ZiB](https://en.wikipedia.org/wiki/ZiB "ZiB") (2<sup>64</sup> × 4,096‑bytes) or 75.6 [ZB](https://en.wikipedia.org/wiki/Zettabyte "Zettabyte") (75.6 × 10²¹ bytes).

In 2010, hard-disk manufacturers introduced drives with 4,096‑byte sectors ([Advanced Format](https://en.wikipedia.org/wiki/Advanced_Format "Advanced Format")).<sup id="cite_ref-bittech_3-0"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-bittech-3">[3]</a></sup> For compatibility with legacy hardware and software, those drives include an emulation technology ([512e](https://en.wikipedia.org/wiki/Advanced_Format#512e "Advanced Format")) that presents 512‑byte sectors to the entity accessing the hard drive, despite their underlying 4,096‑byte physical sectors.<sup id="cite_ref-anandAF_4-0"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-anandAF-4">[4]</a></sup>

Like MBR, GPTs use [logical block addressing](https://en.wikipedia.org/wiki/Logical_block_addressing "Logical block addressing") (LBA) in place of the historical [cylinder-head-sector](https://en.wikipedia.org/wiki/Cylinder-head-sector "Cylinder-head-sector") (CHS) addressing. The protective MBR is stored at LBA 0, and the GPT header is in LBA 1. The GPT header has a [pointer](https://en.wikipedia.org/wiki/Pointer_(computer_programming) "Pointer (computer programming)") to the partition table (*Partition Entry Array*), which is typically at LBA 2. Each entry on the partition table has a size of 128 bytes. The UEFI specification stipulates that a minimum of 16,384 bytes, regardless of sector size, are allocated for the Partition Entry Array.<sup id="cite_ref-uefi_spec_5-0"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-uefi_spec-5">[5]</a></sup> Thus, on a disk with 512-byte sectors, at least 32 sectors are used for the Partition Entry Array, and the first usable block is at LBA 34 or higher, while on a 4,096-byte sectors disk, at least 4 sectors are used for the Partition Entry Array, and the first usable block is at LBA 6 or higher.

For limited backward compatibility, the space of the legacy [Master Boot Record](https://en.wikipedia.org/wiki/Master_boot_record "Master boot record") (MBR) is still reserved in the GPT specification, but it is now used in a way that prevents MBR-based disk utilities from misrecognizing and possibly overwriting GPT disks. This is referred to as a *protective MBR*.<sup id="cite_ref-IBMLargeDrivesGPT_6-0"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-IBMLargeDrivesGPT-6">[6]</a></sup>

A single partition of type [EEh](https://en.wikipedia.org/wiki/Partition_type#PID_EEh "Partition type"), encompassing the entire GPT drive (where "entire" actually means as much of the drive as can be represented in an MBR), is indicated and identifies it as GPT. Operating systems and tools which cannot read GPT disks will generally recognize the disk as containing one partition of unknown type and no empty space, and will typically refuse to modify the disk unless the user explicitly requests and confirms the deletion of this partition. This minimizes accidental erasures.<sup id="cite_ref-IBMLargeDrivesGPT_6-1"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-IBMLargeDrivesGPT-6">[6]</a></sup> Furthermore, GPT-aware OSes may check the protective MBR and if the enclosed partition type is not of type EEh or if there are multiple partitions defined on the target device, the OS may refuse to manipulate the partition table.<sup id="cite_ref-tn2166_7-0"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-tn2166-7">[7]</a></sup>

If the actual size of the disk exceeds the maximum partition size representable using the legacy 32-bit LBA entries in the MBR partition table, the recorded size of this partition is clipped at the maximum, thereby ignoring the rest of the disk. This amounts to a maximum reported size of 2 TiB, assuming a disk with 512 bytes per sector (see [512e](https://en.wikipedia.org/wiki/512e "512e")). It would result in 16 TiB with 4 KiB sectors ([4Kn](https://en.wikipedia.org/wiki/4Kn "4Kn")), but since many older operating systems and tools are hard coded for a sector size of 512 bytes or are limited to 32-bit calculations, exceeding the 2 TiB limit could cause compatibility problems.<sup id="cite_ref-IBMLargeDrivesGPT_6-2"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-IBMLargeDrivesGPT-6">[6]</a></sup>

In operating systems that support GPT-based boot through BIOS services rather than EFI, the first sector may also still be used to store the first stage of the bootloader code, but modified to recognize GPT partitions. The bootloader in the MBR must not assume a sector size of 512 bytes.<sup id="cite_ref-IBMLargeDrivesGPT_6-3"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-IBMLargeDrivesGPT-6">[6]</a></sup>

The partition table header defines the usable blocks on the disk. It also defines the number and size of the partition entries that make up the partition table (offsets 80 and 84 in the table).<sup id="cite_ref-UEFI2.8_2-1"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-UEFI2.8-2">[2]</a></sup><sup><span title="Page: 119">: 119 </span></sup> 

After the header, the Partition Entry Array describes partitions, using a minimum size of 128 bytes for each entry block.<sup id="cite_ref-9"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-9">[8]</a></sup> The starting location of the array on disk, and the size of each entry, are given in the GPT header. The first 16 bytes of each entry designate the partition type's globally unique identifier (GUID). For example, the GUID for an [EFI system partition](https://en.wikipedia.org/wiki/EFI_system_partition "EFI system partition") is C12A7328-F81F-11D2-BA4B-00A0C93EC93B. The second 16 bytes are a GUID unique to the partition. Then follow the starting and ending 64 bit LBAs, partition attributes, and the 36 character (max.) [Unicode](https://en.wikipedia.org/wiki/Unicode "Unicode") partition name. As is the nature and purpose of GUIDs and as per RFC 4122, no central registry is needed to ensure the uniqueness of the GUID partition type designators.<sup id="cite_ref-RFC_4122_10-0"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-RFC_4122-10">[9]</a></sup><sup id="cite_ref-UEFI2.8_2-2"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-UEFI2.8-2">[2]</a></sup><sup>: <span title="Page / location: 2200
Quotation : &quot;All EFI GUIDs (Globally Unique Identifiers) have the format described in RFC 4122 and comply with the referenced algorithms for generating GUIDs.&quot;">2200</span> </sup> 

The 64-bit partition table attributes are shared between 48-bit common attributes for all partition types, and 16-bit type-specific attributes:

Windows 7 and earlier do not support UEFI on 32-bit platforms, and therefore do not allow booting from GPT partitions.<sup id="cite_ref-GPTFAQ_28-0"><a href="https://en.wikipedia.org/wiki/GUID_Partition_Table#cite_note-GPTFAQ-28">[27]</a></sup>

Each partition has a "partition type GUID" that identifies the type of the partition and therefore partitions of the same type will all have the same "partition type GUID". Each partition also has a "partition unique GUID" as a separate entry, which as the name implies is a unique id for each partition.



# How to know if I'm booting using UEFI? 

[https://unix.stackexchange.com/questions/148356/how-to-know-if-im-booting-using-uefi](https://unix.stackexchange.com/questions/148356/how-to-know-if-im-booting-using-uefi)


**First method:**

Ok, I booted up my UEFI box to check. First clue, near the top of `dmesg`. This shouldn't appear if you're booted via BIOS:

```
[    0.000000] efi: EFI v2.31 by American Megatrends
[    0.000000] efi:  ACPI=0xd8769000  ACPI 2.0=0xd8769000  SMBIOS=0xd96d4a98 
[    0.000000] efi: mem00: type=6, attr=0x800000000000000f, range=[0x0000000000000000-0x0000000000001000) (0MB)
⋮
```

**Second method:**

```
$ sudo efibootmgr
BootCurrent: 0000
Timeout: 0 seconds
BootOrder: 0000
Boot0000* debian
```

If you are not, then the following should appear:

```
$ sudo efibootmgr        

EFI variables are not supported on this system.
```

Note that you'll have to have the efibootmgr package installed. You can also attempt to list the EFI variables:

```
$ efivar -l 
... over 100 lines of output ...
```

**Third method:**

Check if you have a `/boot/efi`:

```
$ df -h --local | grep /boot
/dev/sda2       229M   31M  187M  14% /boot
/dev/sda1       120M  250K  119M   1% /boot/efi
```

Inside that partition should be the files that UEFI executes to boot.

If using any of these methods the relevant entries doesn't appear, is very likely you are not using UEFI.