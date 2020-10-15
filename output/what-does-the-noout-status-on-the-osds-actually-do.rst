'noout' flag in Ceph
####################
:date: 2015-05-28 02:45
:author: arvimal
:category: Ceph
:tags: ceph, noout, osd
:slug: what-does-the-noout-status-on-the-osds-actually-do
:status: published

You may have seen the '**noout**' flag set in the output of '**ceph -s**'. What does this actually mean?

This is a global flag for the cluster, which means that if an OSD is out, the said OSD is not marked out of the cluster and data balancing shouldn't start to maintain the replica count. By default, the monitors mark the OSDs out of the acting set if it is not reachable for 300 seconds, ie.. 5 minutes.

To know the default value set in your cluster, use:

   # ceph daemon /var/run/ceph/ceph-mon.*.asok config show \| grep mon_osd_report_timeout

When an OSD is marked as out, another OSD takes its place and data replication starts to that OSD depending on the number of replica counts each pool has.

If this flag (**noout**) is set, the monitor will not mark the OSDs out from the acting set. The PGs will be reporting an inconsistent state, but the OSD will still be in the acting set.

This can be helpful when we want to remove an OSD from the server, but don't want the data objects to be replicated over to another OSD.

To set the '**noout**' flag, use:

   # ceph osd set noout

Once everything you've planned has been done/finished, you can reset it back using:

   # ceph osd unset noout
