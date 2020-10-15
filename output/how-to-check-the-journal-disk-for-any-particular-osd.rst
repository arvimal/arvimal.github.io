How to identify the journal disk for a Ceph OSD?
################################################
:date: 2015-08-05 22:34
:author: arvimal
:slug: how-to-check-the-journal-disk-for-any-particular-osd
:status: published

In many cases, one would like to understand the journal disk a particular OSD is using. There are two methods to understand this:

a) This is the most direct method, and should give you details on the OSD disks and the corresponding journal disks.

[sourcecode language="bash" gutter="false"]

# ceph-disk list

[/sourcecode]

This should output something like:

[sourcecode language="bash" gutter="false"]

| # ceph-disk list
| /dev/sda :
|  /dev/sda1 other, xfs, mounted on /boot
|  /dev/sda2 other, LVM2_member
| /dev/sr0 other, unknown
| /dev/vda :
|  /dev/vda1 ceph data, active, cluster ceph, osd.0, journal /dev/vda2
|  /dev/vda2 ceph journal, for /dev/vda1
| /dev/vdb :
|  /dev/vdb1 ceph data, active, cluster ceph, osd.1, journal /dev/vdc1
| /dev/vdc :
|  /dev/vdc1 ceph journal, for /dev/vdb1
| [/sourcecode]

b) The second method is cruder, and involves listing the OSD mount point on the file system.

[sourcecode language="bash" gutter="false"]

# ls -l /var/lib/ceph/osd/ceph-0/

| total 52
| -rw-r--r--.  1 root root  191 Aug  3 18:02 activate.monmap
| -rw-r--r--.  1 root root    3 Aug  3 18:02 active
| -rw-r--r--.  1 root root   37 Aug  3 18:02 ceph_fsid
| drwxr-xr-x. 70 root root 4096 Aug  4 00:38 current
| -rw-r--r--.  1 root root   37 Aug  3 18:02 fsid
| lrwxrwxrwx.  1 root root   58 Aug  3 18:02 journal -&gt; /dev/disk/by-partuuid/d9ebc4bd-7b5e-4e12-b909-0c72c4f58ee0
| -rw-r--r--.  1 root root   37 Aug  3 18:02 journal_uuid
| -rw-------.  1 root root   56 Aug  3 18:02 keyring
| -rw-r--r--.  1 root root   21 Aug  3 18:02 magic
| -rw-r--r--.  1 root root    6 Aug  3 18:02 ready
| -rw-r--r--.  1 root root    4 Aug  3 18:02 store_version
| -rw-r--r--.  1 root root   42 Aug  3 18:02 superblock
| -rw-r--r--.  1 root root    0 Aug  5 13:09 sysvinit
| -rw-r--r--.  1 root root    2 Aug  3 18:02 whoami

| # ls -l /dev/disk/by-partuuid/d9ebc4bd-7b5e-4e12-b909-0c72c4f58ee0
| lrwxrwxrwx. 1 root root 10 Aug  5 13:08 /dev/disk/by-partuuid/d9ebc4bd-7b5e-4e12-b909-0c72c4f58ee0 -&gt; ../../vda2

[/sourcecode]

As you can see, the file 'journal' is a symlink to the journal disk. The first method is much easier, but its always better to know how things are layered out underneath.
