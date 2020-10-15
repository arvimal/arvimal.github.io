How to get a Ceph MON/OSD map at a specific epoch?
##################################################
:date: 2016-05-08 11:12
:author: arvimal
:category: Ceph
:slug: how-to-get-a-ceph-monosd-map-at-a-specific-epoch
:status: published

To get a MON map or an OSD map of a specific epoch, use:

   | # ceph osd getmap <epoch-value>
   | # ceph mon getmap <epoch-value>

The map can be forwarded to a file as following:

   # ceph osd getmap <epoch-value> -o /tmp/ceph_osd_getmap.bin

This would be in a binary format, and hence will need to be dumped to a human-readable form.

   # osdmaptool --print /tmp/ceph-osd-getmap.bin

This will print the current OSD map, similar to the output of 'ceph osd dump'.

Where this command shines is when you can fetch maps from previous epochs, and pull information on specific placement groups in those epochs.

For example, I've had all the OSDs on one of my node down some time back (in a previous epoch). The ability to query a previous epoch gives the administrator the power to understand how exactly the cluster was at a specific time period.
