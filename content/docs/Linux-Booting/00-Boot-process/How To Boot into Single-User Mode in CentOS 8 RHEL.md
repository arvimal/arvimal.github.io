# How To Boot into Single-User Mode in CentOS 8 / RHEL 8 | ITzGeek

[https://www.itzgeek.com/how-tos/linux/centos-how-tos/how-to-boot-into-single-user-mode-in-rhel-8.html](https://www.itzgeek.com/how-tos/linux/centos-how-tos/how-to-boot-into-single-user-mode-in-rhel-8.html)

Single-User mode is one of the user run levels in the Linux operating system. It is used for doing the administrative task such as recovering the file system and the [lost root password](https://www.itzgeek.com/how-tos/linux/centos-how-tos/how-to-reset-lost-root-password-in-rhel-8.html) etc.

In single-user mode, the services won’t start, and none of the users are allowed to log in except root. Also, the system would not prompt for login, which means you do not need a password to get root access.

Here, we will see how to boot into a single-user mode in [CentOS 8](https://www.itzgeek.com/tag/centos-8) / [RHEL 8](https://www.itzgeek.com/tag/rhel-8).

## 1.Interrupt Boot

While the system boots, you might see the splash screen like below. The system waits for 5 seconds before booting the operating system. Here, press any key to interrupt the autoboot.

Interrupt Boot

![https://www.itzgeek.com/wp-content/uploads/2019/07/Interrupt-Boot.jpg](https://www.itzgeek.com/wp-content/uploads/2019/07/Interrupt-Boot.jpg)

## 2. Choose Kernel

It would display the list of kernels and operating systems you have it on the machine. If you are booting into Single-User mode to reset root password or other administrative tasks, you can choose the latest kernel. Whereas, if you have problem with the latest kernel and want to fix the kernel issue, choose the previous kernel.

To go into single-user mode, select the kernel and press e edit arguments of the kernel.

Select Kernel

![https://www.itzgeek.com/wp-content/uploads/2019/07/Select-Kernel.jpg](https://www.itzgeek.com/wp-content/uploads/2019/07/Select-Kernel.jpg)

## 3. Edit Kernel Parameters

Now, you should see the information about the selected operating system like hard disk, root partition, location of the kernel, crash kernel, and initrd (Initial ram disk).

Go to the line that starts with **linux** using up and down arrow then delete the ro argument.

Kernel Parameter

![https://www.itzgeek.com/wp-content/uploads/2019/07/Delete-Kernel-Parameter.jpg](https://www.itzgeek.com/wp-content/uploads/2019/07/Delete-Kernel-Parameter.jpg)

## 4. Boot into Single-User Mode

Add this rw init=/sysroot/bin/sh in the line. Once done, press Ctrl+x.

Boot into Single-User Mode

![https://www.itzgeek.com/wp-content/uploads/2019/07/Boot-Into-Single-User-Mode-1.jpg](https://www.itzgeek.com/wp-content/uploads/2019/07/Boot-Into-Single-User-Mode-1.jpg)

## 5. Single-User Mode

Now, you should be in shell prompt with root privileges.

Single-User Mode in RHEL 8

![https://www.itzgeek.com/wp-content/uploads/2019/07/Single-User-Mode.jpg](https://www.itzgeek.com/wp-content/uploads/2019/07/Single-User-Mode.jpg)

Now, mount root file system with chroot command.

```
chroot /sysroot
```

Mount Root File System

![https://www.itzgeek.com/wp-content/uploads/2019/07/Mount-Root-File-System-1.jpg](https://www.itzgeek.com/wp-content/uploads/2019/07/Mount-Root-File-System-1.jpg)

You can now troubleshoot your system or can do maintenance of your system. The single-user mode is often used to [reset the lost root password in CentOS 8 / RHEL 8](https://www.itzgeek.com/how-tos/linux/centos-how-tos/how-to-reset-lost-root-password-in-rhel-8.html).

Once you complete the activities, exit from the chroot.

```
exit
```

Then, [reboot the system](https://www.itzgeek.com/how-tos/linux/how-to-use-linux-shutdown-poweroff-and-reboot-command.html) to boot into the default run level.

```
reboot
```

## Conclusion

That’s all. You have learned how to boot into a single-user mode in [CentOS 8](https://www.itzgeek.com/tag/centos-8) / [RHEL 8](https://www.itzgeek.com/tag/rhel-8). Please share your feedback in the comments section.