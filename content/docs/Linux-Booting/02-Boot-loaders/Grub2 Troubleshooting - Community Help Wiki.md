# Grub2/Troubleshooting - Community Help Wiki

[https://help.ubuntu.com/community/Grub2/Troubleshooting#grub_rescue.3E-1](https://help.ubuntu.com/community/Grub2/Troubleshooting#grub_rescue.3E-1)

[[Grub2 Troubleshooting - Community Help Wiki 8b8db45a75634d82a27b2181e8904881 Troubleshooting]]

1. **set prefix=(hd*X,Y*)/boot/grub**

Use the values determined earlier.

Example: If the Ubuntu system is on sda5, enter: *set prefix=(hd0,5)/boot/grub*

Confirm the correct X,Y values and press *ENTER*.

Example: If the Ubuntu system is on sda5, enter: *set root=(hd0,5)*

Load the *normal* module.

If the module fails to load, try the full path: *insmod (hdX,Y)/boot/grub/normal.mod*

Transition to the normal GRUB 2 mode with increased functionality.

If the module loads, *HELP*, TAB completion and command recall using the UP/DN keys should be available.

(Optional) Review the current settings.

Load the *linux* module. An error message usually means the path is incorrect.

If the *vmlinuz* symlink does not exist in /, use the full path to the kernel in /boot

Selects the latest initrd image.

If the *initrd* symlink does not exist in /, use the full path to the initrd image in /boot