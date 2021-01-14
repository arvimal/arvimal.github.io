---
title: "How to fetch the entire list of tunables along with the values for a Ceph cluster node?"
date: "2015-05-27"
categories: 
  - "ceph"
tags: 
  - "admin-socket"
  - "ceph"
  - "config-show"
---

In many cases we would like to get the active configurations from a Ceph node, either a monitor or an OSD node. A neat feature, I must say, is to probe the administrative socket file to get a listing of all the active configurations, be it on the OSD node or the monitor node.

This comes handy when we have changed a setting and wants to confirm if it had indeed changed or not.

The admin socket file exists for both the monitors and the OSD nodes. The monitor node will have a single admin socket file, while the OSD nodes will have an admin socket for each of the OSDs present on the node.

- Listing of the admin socket on a monitor node

\[sourcecode language="bash" gutter="false"\] # ls /var/run/ceph/ -l total 4 srwxr-xr-x. 1 root root 0 May 13 05:13 ceph-mon.hp-m300-2.asok -rw-r--r--. 1 root root 7 May 13 05:13 mon.hp-m300-2.pid \[/sourcecode\]

- Listing of the admin sockets on an OSD node

\[sourcecode language="bash" gutter="false"\] # ls -l /var/run/ceph/ total 20 srwxr-xr-x. 1 root root 0 May  8 02:42 ceph-osd.0.asok srwxr-xr-x. 1 root root 0 May 26 11:18 ceph-osd.2.asok srwxr-xr-x. 1 root root 0 May 26 11:18 ceph-osd.3.asok srwxr-xr-x. 1 root root 0 May  8 02:42 ceph-osd.4.asok srwxr-xr-x. 1 root root 0 May 26 11:18 ceph-osd.5.asok -rw-r--r--. 1 root root 8 May  8 02:42 osd.0.pid -rw-r--r--. 1 root root 8 May 26 11:18 osd.2.pid -rw-r--r--. 1 root root 8 May 26 11:18 osd.3.pid -rw-r--r--. 1 root root 8 May  8 02:42 osd.4.pid -rw-r--r--. 1 root root 8 May 26 11:18 osd.5.pid \[/sourcecode\]

For example, consider that we have changed the 'mon\_osd\_full\_ratio' value, and need to confirm that the cluster has picked up the change.

We can get a listing of the active configured settings and grep out the setting we are interested in.

\[sourcecode language="bash" gutter="false"\]

\# ceph daemon /var/run/ceph/ceph-mon.\*.asok config show

\[/sourcecode\]

The above command prints out a listing of all the active configurations and their current values. We can easily grep out 'mon\_osd\_full\_ratio' from this list.

\[sourcecode language="bash" gutter="false"\]

\# ceph daemon /var/run/ceph/ceph-mon.\*.asok config show | grep mon\_osd\_full\_ratio

\[/sourcecode\]

On my test cluster, this printed out '0.75' which is the default setting. The cluster should print out 'near full' warnings once any OSD has reached 75% of its size.

This can be checked by probing the OSD admin socket as well.

NOTE: In case you are probing a particular OSD, please make sure to use the OSD admin socket on the node in which the OSD is. In order to locate the OSD and the node it is on, use :

\[sourcecode language="bash" gutter="false"\]

\# ceph osd tree

\[/sourcecode\]

Example: We try probing the OSD admin socket on its node, for 'mon\_osd\_full\_ratio' as we did on the monitor. It should return the same value.

\[sourcecode language="bash" gutter="false"\]

\# ceph daemon /var/run/ceph/ceph-osd.5.asok config show | grep mon\_osd\_full\_ratio

\[/sourcecode\]

NOTE: Another command exists which should print the same configuration settings, but only for OSDs.

\[sourcecode language="bash" gutter="false"\]

\# ceph daemon osd.5 config show

\[/sourcecode\]

A drawback worth mentioning, this should be executed on the node on which the OSD is present. To find that the OSD to node mapping, use 'ceph osd tree'.
