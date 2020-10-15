lsusb and chroot in anaconda.. Is usbfs mounted in anaconda %post installation ?
################################################################################
:date: 2010-12-23 07:53
:author: arvimal
:category: Techno
:tags: anaconda, installation, lsusb, rhel, strace, usb
:slug: lsusb-and-chroot-in-anaconda-is-usbfs-mounted-in-anaconda-post-installation
:status: published

**T**\ he binary '/sbin/lsusb' in a chroot-ed environment have problems running properly. I have not checked this in a manually created chroot environment or using tools like 'mock'.

The scenario is as following :

We were trying to check the output of 'lsusb' in the %post section of a kickstart installation. I had specified 'noreboot' in the kickstart file so the machine will wait for the user to manually reboot the machine. This helps to check the logs and the situation of the machine just after the installation finishes.

After the installation and prior to the reboot, i checked in the second available terminal (Alt + F2) created by anaconda and was astonished to see that the command 'lsusb' does not give us the required output but an error that '/usr/share/hwdata/usb.ids' is not accessible or found.

By default, i think only the 'installation' ie.. the %post section starts in a 'chroot' mode and the terminal available is not chroot-ed. So we will have to use '/mnt/sysimage/sbin/lsusb'. This didn't work as expected since the 'lsusb' binary needs to check the file '/usr/share/hwdata/usb.ids' and won't be able to find it.

So I did a chroot from the second terminal and did an /sbin/lsusb, since /sbin in not in the 'PATH' by default. That too, didn't work out. But this time it didn't even complain anything. Just nothing at all, no output. Last time, at-least it complained it could not find something. So how do we go forward now ??? Here comes 'strace' to the rescue !!!

strace is of-course a really nice tool to know what system calls are made and lots of internal stuff a binary will do while being executed. But 'strace' is not installed by default on a RHEL5 machine, which is the case here. As most of you would know, anaconda creates a virtual file system which consists of most of the folders found under a linux main /. The location where the OS is installed is mounted under /mnt/sysimage.

Since we already have an ISO from where we have booted the machine from (DVD/CD), we are free to mount it on the filesystem, which is what we did. :

| [sourcecode language="bash" gutter="false"]
| # mkdir /mnt/source
| # mount -t iso9660 /dev/hdc /mnt/source
| # cd /mnt/source/Server/
| [/sourcecode]

In case you want to know how the DVD/CD drive is detected, all you need to do is execute 'dmesg' in the available terminal. ie.. after pressing 'Alt + Ctrl + F2'.

So we went forward and mounted the DVD to /mnt/source and changed the directory to /mnt/source/Server where all the rpm packages reside. Installed the package 'strace' using an 'rpm -ivh'. Please note that we need to use '--root /mnt/sysimage' as an option since we are installing the package to our newly installed file system which is at /mnt/sysimage. If this is not used, the installer will try to install the package to the virtual environment created in the memory.

| [sourcecode language="bash" gutter="false"]
| # cd /mnt/source/Server
| # rpm -ivh strace-&lt;version&gt;.rpm --root /mnt/sysimage
| # cd
| # chroot /mnt/sysimage
| [/sourcecode]

This will make /mnt/sysimage as the working root, ie.. where our installation was done. OK.. now for the 'strace' stuff.

| [sourcecode language="bash" gutter="false"]
| # strace -fxvto strace.log -s 1024 /sbin/lsusb
| [/sourcecode]

The strace output will be saved to 'strace.log' which we can open up in a text editor of our choice. Opening it in 'vi', shows a lot of stuff such as the command run, the default language, location of libraries loaded, the environment variables etc.. In this case we would only need to be interested in the last parts, ie.. to know where the binary failed :

| [sourcecode language="text" gutter="true"]
| 15:16:17 open("/dev/bus/usb", O_RDONLY|O_NONBLOCK|O_DIRECTORY) = -1 ENOENT (No such file or directory) = 03067
| 15:16:17 open("/proc/bus/usb", O_RDONLY|O_NONBLOCK|O_DIRECTORY) = 33067
| 15:16:17 fstat(3, {st_dev=makedev(0, 3), st_ino=4026532146, st_mode=S_IFDIR|0555, st_nlink=2, st_uid=0, st_gid=0, st_blksize=4096, st_blocks=0, st_size=0, st_atime=2009/09/25-15:16:17, st_mtime=2009/09/25-15:16:17, st_ctime=2009/09/25-15:16:17}) = 03067
| 15:16:17 fcntl(3, F_SETFD, FD_CLOEXEC) = 03067
| 15:16:17 getdents(3, {{d_ino=4026532146, d_off=1, d_reclen=24, d_name="."} {d_ino=4026531879, d_off=2, d_reclen=24, d_name=".."}}, 4096) = 483067
| 15:16:17 getdents(3, {}, 4096) = 03067
| 15:16:17 close(3) = 03067
| 15:16:17 exit_group(1) = ?
| [/sourcecode]

The above trace output shows how the 'lsusb' binary proceeded at its last time and where it failed. We can see that it went to open '/dev/bus/usb', only to find that the said location does not exist. We can understand that it is a directory from the call

| [sourcecode language="text" gutter="false"]
| open("/dev/bus/usb", O_RDONLY|O_NONBLOCK|O_DIRECTORY)
| [/sourcecode]

Ok,, fine.. so what does it do next ?

As the next step, it tries to open '/proc/bus/usb' and it is present, which we know since there are no 'No such file or directory' errors. Going further, the binary goes on to do a 'stat' on '/proc/bus/usb'. After doing an 'fstat', it goes to check the file descriptor using 'fcntl' and further goes to list the directory contents using 'getdents'.

This is where we find the interesting output :

| [sourcecode language="text" gutter="false"]
| getdents(3, {{d_ino=4026532146, d_off=1, d_reclen=24, d_name="."} {d_ino=4026531879, d_off=2, d_reclen=24, d_name=".."}}, 4096) = 48
| [/sourcecode]

As you can see in the above trace, it returns '.' and '..', which means there are nothing in /proc/bus/usb. So what we do understand is 'lsusb' refers /dev/bus/usb and /proc/bus/usb for its outputs.. If it was not able to find anything, strace would have given us an error which obviously would have made life much easier.

And that's how '/sbin/lsusb' failed silently.. Isn't strace a nice tool ??

Okay, those who want to know why is this so... 'lsusb' needs either /mnt/sysimage/proc/bus/usb or /mnt/sysimage/dev/bus/usb display contents to work properly. Anaconda is not mounting /mnt/sysimage/proc/bus/usb with the 'usbfs' file system in the limited installation environment and hence 'lsusb' fails...

And we have a fix for that which goes into yuminstall.py in the anaconda source :

| [sourcecode language="python" gutter="false"]
| try:
|     isys.mount("/proc/bus/usb", anaconda.rootPath + "/proc/bus/usb", "usbfs")
| except Exception, e:
|     log.error("error mounting usbfs: %s" %(e,))
| [/sourcecode]

This piece of python code, tries mounting /proc/bus/usb on /mnt/sysimage/proc/bus/usb as 'usbfs. If its not possible, the code excepts an Exception error and reports "error mounting 'usbfs'.
