# Tip: VM won’t boot, troubleshoot with guestfish | Richard WM Jones

[https://rwmj.wordpress.com/2010/02/09/tip-vm-wont-boot-troubleshoot-with-guestfish/](https://rwmj.wordpress.com/2010/02/09/tip-vm-wont-boot-troubleshoot-with-guestfish/)

Unbootable virtual machine? Here are three useful guestfish commands to help. (You can also consider using [virt-rescue](http://libguestfs.org/FAQ.html#rescue)).

### 1. Edit /boot/grub/grub.conf

```
$ guestfish -i Rawhide

Welcome to guestfish, the libguestfs filesystem interactive shell for
editing virtual machine filesystems.

Type: 'help' for help with commands
      'quit' to quit the shell

><fs> ls /boot/
System.map-2.6.32.1-9.fc13.x86_64
System.map-2.6.32.3-21.fc13.x86_64
System.map-2.6.33-0.40.rc7.git0.fc13.x86_64
config-2.6.32.1-9.fc13.x86_64
config-2.6.32.3-21.fc13.x86_64
config-2.6.33-0.40.rc7.git0.fc13.x86_64
[...]

```

Use the “edit”, “emacs” or “vi” commands to edit grub.conf:

```
><fs> vi /boot/grub/grub.conf
```

From here you can change the boot kernel, change it to boot in single user mode, enable the grub menu, remove the “rhgb quiet” option so you can see boot messages, and much more.

### 2. Look at the /init script

When the kernel panics because it cannot mount root, it’s often because the initrd or initramfs is broken in some way. Two commands help here:

```
><fs> initrd-list /boot/initramfs-2.6.33-0.40.rc7.git0.fc13.x86_64.img | less
><fs> initrd-cat /boot/initramfs-2.6.33-0.40.rc7.git0.fc13.x86_64.img init | less
```

The first command lists all the files in the initrd, which lets you see if the right drivers got included for the (virtual) hardware. The second command lists out the init script — which is the shell script that runs first before the OS proper starts to boot.