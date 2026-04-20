# Check if Your Computer Uses UEFI or BIOS [Both in Linux and Windows]

[https://itsfoss.com/check-uefi-or-bios/](https://itsfoss.com/check-uefi-or-bios/)

***Brief: A quick tutorial to tell you if your system uses the modern UEFI or the legacy BIOS. Instructions for both Windows and Linux have been provided.***

When you are trying to [dual boot Linux with Windows](https://itsfoss.com/guide-install-linux-mint-16-dual-boot-windows/), you would want to know if you have UEFI or BIOS boot mode on your system. It helps you decide in partition making for installing Linux.

I am not going to discuss [what is BIOS](https://www.lifewire.com/bios-basic-input-output-system-2625820) here. However, I would like to tell you a few advantages of [UEFI](https://www.howtogeek.com/56958/htg-explains-how-uefi-will-replace-the-bios/) over BIOS.

UEFI or Unified Extensible Firmware Interface was designed to overcome some of the limitations of BIOS. It added the ability to use larger than 2 TB disks and had a CPU independent architecture and drivers. With a modular design, it supported remote diagnostics and repairing even with no operating system installed and a flexible without-OS environment including networking capability.

### Advantage of UEFI over BIOS

- UEFI is faster in initializing your hardware.
- Offer Secure Boot which means everything you load before an OS is loaded has to be signed. This gives your system an added layer of protection from running malware.
- BIOS do not support a partition of over 2TB.
- Most importantly, if you are dual booting it’s always advisable to install both the OS in the same booting mode.

![[/uefi-or-bios.png]]

If you are trying to find out whether your system runs UEFI or BIOS, it’s not that difficult. Let me start with Windows first and afterward, we’ll see how to check UEFI or BIOS on Linux systems.

## Check if you are using UEFI or BIOS on Windows

On Windows, “System Information” in Start panel and under BIOS Mode, you can find the boot mode. If it says Legacy, your system has BIOS. If it says UEFI, well it’s UEFI.

![[/BIOS.png]]

**Alternative**: If you using Windows 10, you can check whether you are using UEFI or BIOS by opening File Explorer and navigating to C:\Windows\Panther. Open file setupact.log and search for the below string.

```
Detected boot environment
```

I would advise opening this file in notepad++, since its a huge text file and notepad may hang (at least it did for me with 6GB RAM).

You will find a couple of lines which will give you the information.

```
BIOS
```

## Check if you are using UEFI or BIOS on Linux

The easiest way to find out if you are running UEFI or BIOS is to look for a folder /sys/firmware/efi. The folder will be missing if your system is using BIOS.

![[/uefi-bios.png]]

/sys/firmware/efi exists means system uses UEFI

**Alternative**: The other method is to install a package called efibootmgr.

On Debian and Ubuntu based distributions, you can install the efibootmgr package using the command below:

```
sudo apt install efibootmgr
```

Once done, type the below command:

```
# sudo efibootmgr
```

If your system supports UEFI, it will output different variables. If not you will see a message saying EFI variables are not supported.

![[Check if Your Computer Uses UEFI or BIOS [Both in  62b9bd99b5c74fafaca6cf6238995dc2 bootmanager.jpg]]

### Final Words

Finding whether your system is using UEFI or BIOS is easy. On one hand, features like faster and secure boot provide an upper hand to UEFI, there is not much that should bother you if you are using BIOS – unless you are planning to use a 2TB hard disk to boot.