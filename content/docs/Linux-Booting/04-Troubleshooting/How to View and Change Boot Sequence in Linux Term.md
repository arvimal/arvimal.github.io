# How to View and Change Boot Sequence in Linux Terminal

[https://www.makeuseof.com/how-to-view-and-change-boot-sequence-in-linux-terminal/](https://www.makeuseof.com/how-to-view-and-change-boot-sequence-in-linux-terminal/)

Have you ever had a need to change your boot sequence via terminal? Maybe you're doing so remotely via SSH, or maybe you can't manage to get into the BIOS during that two second sweet spot when your computer is first turned on. In this article, we'll explain how to easily change the boot sequence via terminal.

## View the Boot Sequence

Assuming your computer supports [EFI (Extensive Firmware Interface)](https://www.makeuseof.com/tag/what-is-uefi-and-how-does-it-keep-you-more-secure/), which is pretty near all computers nowadays, you may view the current boot sequence via terminal with the command:

```
efibootmgr -v
```

This will display all boot devices on your computer, and resemble something like:

```
BootCurrent: 0000
Timeout: 2 seconds
BootOrder: 0000,0004,0005,0003
Boot0000* ubuntu	HD(...)/File(\EFI\UBUNTU\SHIMX64.EFI)
Boot0003* Hard Drive	BBS(...)
Boot0004* UEFI: JetFlashTranscend 32GB 1100 ...
Boot0005* UEFI: JetFlashTranscend 32GB 1100, Partition 1...
```

The first line shows the current device that was booted from, the third line shows the computer's current boot sequence, and the following lines list each bootable device.

Take note of the numbers such as 000, 003, etc. In this example, we can see the current boot sequence is the [Ubuntu installation](https://www.makeuseof.com/tag/6-things-ubuntu-better-windows/), followed by the hard drive, and the two different partitions on a 32GB USB drive.

## Change Boot Sequence

Choose your new boot sequence by the device numbers, and change your boot sequence with the command:

```
sudo efibootmgr -o 5,0,4,3
```

Using the above example, that command would change the boot sequence to try the USB drive first, followed by the main Ubuntu installation.

It's that simple, and you can now change the boot sequence on any Linux computer via terminal without scrambling to get into the BIOS when first powering on the computer.

Image Credit: Logan Weaver/[Unsplash](https://unsplash.com/photos/Oaxd6VsCMr8)

   [**Running Linux From a USB Drive: Are You Doing It Right?**](https://www.makeuseof.com/tag/running-linux-usb-right/)

[Did you know that can do a full install of Linux on a USB drive? Here's how to create a Linux USB PC in your pocket!](https://www.makeuseof.com/tag/running-linux-usb-right/)

**About The Author**