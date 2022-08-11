# lvcreate fails with the error "Aborting. Failed to activate new LV to wipe the start of it.". Why ??

<!--more-->
In case anyone out there gets an error message like "Aborting. Failed to activate new LV to wipe the start of it." while doing an 'lvcreate', check (/etc/lvm/lvm.conf) once more.

Most probably, a 'volume\_list' would have been defined in there, which in turns want you to specify the 'volume\_list' tag specified along with the lvcreate command.

Excerpt from /etc/lvm/lvm.conf:

> \# If volume\_list is defined, each LV is only activated if there is a # match against the list. #   vgname and vgname/lvname are matched exactly. #   @tag matches any tag set in the LV or VG. #   @\* matches if any tag defined on the host is also set in the LV or VG # # volume\_list = \[ vg1, vg2/lvol1, @tag1, @\* \] volume\_list = \[ VG01, @foo.com \]

In this case, you will have to use the 'lvcreate' command as follows, which will create the logical volume properly.

> \# lvcreate --addtag @foo.com    ... following-options

