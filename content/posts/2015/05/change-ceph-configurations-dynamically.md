---
title: "How to dynamically change a configuration value in a Ceph cluster?"
date: 2015-05-27
categories:
  - "ceph"
tags:
  - "ceph"
  - "ceph-tell"
---

It is possible to change a particular configuration setting in a Ceph cluster dynamically, and I think it is a very neat and useful feature.

Imagine the case where you want to change the replica count of a particular PG from 3 to 4. How would you change this without restarting the Ceph cluster itself? That is where the 'ceph tell' command comes in.

As we saw in the [previous post](https://arvimal.wordpress.com/2015/05/27/how-can-we-get-a-list-of-all-the-configurations-from-a-ceph-cluster-node/), you can get the list of configuration settings using the administrator socket, from either a monitor or an OSD node.

To change a configuration use:

\[sourcecode language="bash" gutter="false"\]

\# ceph tell mon.\* injectargs '--{tunable value\_to\_be\_set}'

\[/sourcecode\]

For example, to change the timeout value after which an OSD is out and down, can be changed with:

\[sourcecode language="bash" gutter="false"\]

\# ceph tell mon.\* injectargs '--mon\_osd\_report\_timeout 400'

\[/sourcecode\]

By default, it is 300 seconds, ie.. 5 minute
