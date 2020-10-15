lvcreate fails with the error "Aborting. Failed to activate new LV to wipe the start of it.". Why ??
####################################################################################################
:date: 2009-11-02 19:00
:author: arvimal
:category: Techno
:slug: lvcreate-fails-with-the-error-aborting-failed-to-activate-new-lv-to-wipe-the-start-of-it-why
:status: published

In case anyone out there gets an error message like "Aborting. Failed to activate new LV to wipe the start of it." while doing an 'lvcreate', check (/etc/lvm/lvm.conf) once more.

Most probably, a 'volume_list' would have been defined in there, which in turns want you to specify the 'volume_list' tag specified along with the lvcreate command.

Excerpt from /etc/lvm/lvm.conf:

   | # If volume_list is defined, each LV is only activated if there is a
   | # match against the list.
   | #   vgname and vgname/lvname are matched exactly.
   | #   @tag matches any tag set in the LV or VG.
   | #   @\* matches if any tag defined on the host is also set in the LV or VG
   | #
   | # volume_list = [ vg1, vg2/lvol1, @tag1, @\* ]
   | volume_list = [ VG01, @foo.com ]

In this case, you will have to use the 'lvcreate' command as follows, which will create the logical volume properly.

   # lvcreate --addtag @foo.com    ... following-options
