---
title: "How to change the filling ratio for a Ceph OSD?"
date: 2015-05-07
categories:
  - "ceph"
tags:
  - "ceph"
  - "fill-ratio"
  - "osd"
---
<!--more-->
There could be many scenarios where you'd need to change the percentage of space usage on a Ceph OSD. One such use case would be when your OSD space is about to hit the hard limit, and is constantly sending you warnings.

For some reason or other, you may need to extend the threshold limit for some time. In such a case, you don't need to change/add the configuration in ceph.conf and push it across. Rather you can do it while the cluster is online, via command mode.

The 'ceph tell' is a very useful command in the sense the administrator don't need to stop/start the OSDs, MONs etc.. after a configuration change. In our case, we are looking to set the 'mon\_osd\_full\_ratio' to 98%. We can do it by using:

\[sourcecode language="bash" gutter="false"\]

\# ceph tell mon.\* injectargs "--mon\_osd\_full\_ratio .98"

\[/sourcecode\]

In an earlier post ([https://goo.gl/xjXOoI](https://goo.gl/xjXOoI)) we had seen how to get all the configurable options from a monitor. If I understand correct, almost all the configuration values can be changed online by injecting the values using 'ceph tell'.
