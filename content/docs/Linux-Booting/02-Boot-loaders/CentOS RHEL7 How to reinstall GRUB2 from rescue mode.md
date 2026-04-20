# CentOS / RHEL 7 : How to reinstall GRUB2 from rescue mode

[https://www.thegeekdiary.com/centos-rhel-7-how-to-reinstall-grub2-from-rescue-mode/](https://www.thegeekdiary.com/centos-rhel-7-how-to-reinstall-grub2-from-rescue-mode/)

CentOS / RHEL 7 now includes GRUB2 which uses a new way of installing to the MBR of your boot device. You may have to reinstall the GRUB2 bootloader if your system is not bootable after a failure. In order to reinstall GRUB2 you have to boot into rescue mode. Follow the steps below to boot into rescue mode and reinstall GRUB2 bootloader.

## Booting into rescue mode and reinstalling GRUB2

1. Boot from the RHEL7 installation DVD by altering the boot order in Bios and selecting DVD media as the first booting preference.

**Note** : Older version of RHEL 7 DVD will not work here. So make sure you have latest version RHEL 7 DVD with you.

2. At the boot screen, Select the Troubleshooting option at the end of the screen.

![[/troubleshooting-option-for-RHEL-7-rescue-mode.png]]

3. At the next screen, select the option **Rescue a CentOS Linux system**.

![[/rescue-a-centos-7-system-reinstall-GRUB2.png]]

4. On the next screen, press enter to continue. When asked if you would like Rescue to find your installation, choose Continue.

![[/find-linux-installation-for-rescue-mode-RHEL-7-reinstall-GRUB2.png]]

If you run into trouble detecting your install, retry using the Skip option and manually detect and mount your storage. You would get a message shown in the picture below if the rescue mode has detected the correct installation.

![[/system-has-been-mounted-under-mntsysimage-RHEL-7-reinstall-GRUB2.png]]

5. Next step is to change your root directory to **/mnt/sysimage** using the chroot command. This makes your system the root environment.

6. Use the grub2-install command to re-write the MBR to your boot device. The boot device is usually /dev/sda.

You should get a successful installation message as shown below.

![[/grub2-install-RHEL-7.png]]

To reboot the system first exit from the chroot environment and the run reboot command.

## Reinstalling grub2 on UEFI-based machines

If you are on an UEFI-based machine, make sure you add the below 2 steps as well before you re-install GRUB2 using “grub2-install” command.

1. If the EFI System Partition has been recreated or damaged, these files can be recovered by reinstalling the **grub2-efi**, **grub2-efi-modules** and **shim** packages.

```
# yum reinstall grub2-efi grub2-efi-modules  shim
```

2. If **/boot/efi/EFI/redhat/grub.cfg** has been removed or damaged, it can be restored with the following command:

```
# grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg
```