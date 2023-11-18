---
tags:
- grub
- grubx64
- shim
- shimx64
- grub2
- efi
- boot
- linux
---

# Difference between grubx64 and shimx64?

[https://askubuntu.com/questions/342365/what-is-the-difference-between-grubx64-and-shimx64](https://askubuntu.com/questions/342365/what-is-the-difference-between-grubx64-and-shimx64)

Typically, `EFI/ubuntu/grubx64.efi` on the EFI System Partition (ESP) is the GRUB binary, and `EFI/ubuntu/shimx64.efi` is the binary for shim. 

The latter is a relatively simple program that provides a way to boot on a computer with Secure Boot active. On such a computer, an unsigned version of GRUB won't launch, and signing GRUB with Microsoft's keys is impossible, so shim bridges the gap and adds its own security tools that parallel those of Secure Boot. In practice, shim registers itself with the firmware and then launches a program called `grubx64.efi` in the directory from which it was launched, so on a computer without Secure Boot (such as a Mac), launching `shimx64.efi` is just like launching `grubx64.efi`. On a computer with Secure Boot active, launching `shimx64.efi` should result in GRUB starting up, whereas launching `grubx64.efi` directly probably won't work.

Note that there's some ambiguity possible. In particular, if you want to use a boot manager or boot loader *other than* GRUB in a Secure Boot environment with shim, you must call that program `grubx64.efi`, even though it's not GRUB. Thus, if you were to install rEFInd on a Secure Boot-enabled computer, `grubx64.efi` could be the rEFInd binary. This binary would probably not reside in `EFI/ubuntu`, though; both it and a shim binary would probably go in `EFI/refind`. Also, as you've got a Mac (which doesn't support Secure Boot), there's no need to install rEFInd in this way; it makes much more sense to install rEFInd as `EFI/refind/refind_x64.efi` (its default location and name).

Note that the rEFInd documentation includes [a whole page on Secure Boot.](http://www.rodsbooks.com/refind/secureboot.html) Chances are you won't benefit from reading it, user190735, since you're using a Mac. I mention it only in case some other reader comes along who's trying to use rEFInd in conjunction with Secure Boot.

### References:

1. [wiki.ubuntu.com/SecurityTeam/SecureBoot](http://wiki.ubuntu.com/SecurityTeam/SecureBoot)
2. [https://askubuntu.com/questions/342365/what-is-the-difference-between-grubx64-and-shimx64](https://askubuntu.com/questions/342365/what-is-the-difference-between-grubx64-and-shimx64)
