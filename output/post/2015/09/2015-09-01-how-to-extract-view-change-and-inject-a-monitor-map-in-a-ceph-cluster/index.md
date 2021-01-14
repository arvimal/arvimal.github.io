---
title: "Monitor maps, how to edit them?"
date: "2015-09-01"
categories: 
  - "ceph"
tags: 
  - "ceph"
  - "monitors"
  - "monmaptool"
---

The **MON map** is used by the monitors in a Ceph cluster, where they keep track of various attributes relevant to the working of the cluster.

Similar to the [CRUSH](http://ceph.com/papers/weil-crush-sc06.pdf) map, a monitor map can be pulled out of the cluster, inspected, changed, and injected back to the monitors, manually. A frequent use-case is when the IP address of a monitor changes and the monitors cannot agree on a quorum.

Monitors use the monitor map (**monmap**) to get the details of other monitors. So just changing the monitor address in '**ceph.conf**' and pushing the configuration to all the nodes won't help to propagate the changes.

In most cases, starting the monitor with a wrong monitor map would make the monitors commit suicide, since they would find conflicting information about themself in the mon map due to the IP address change.

There are two methods to fix this problem, the first being adding enough new monitors, let them form a quorum, and remove the faulty monitors. This doesn't need any explanation. The second and more crude way, is to edit the monitor map directly, set the new IP address, and upload the monmap back to the monitors.

This article discusses the second method, ie.. how to edit the monmap, and re-inject it back. This can be done using the '**monmap**' tool.

1\. As the first step, login to one of the monitors, and get the monitor map:

> **\# ceph mon getmap -o /tmp/monitor\_map.bin**

2\. Inspect what the monitor map contains:

> **\# monmaptool --print /tmp/monitor\_map.bin**

- An example from my cluster :

> **\# monmaptool --print monmap**
> 
> monmaptool: monmap file monmap epoch 1 fsid d978794d-5835-4ac3-8fe3-3855b18b9572 last\_changed 0.000000 created 0.000000 0: 192.168.122.73:6789/0 mon.node2

3\. Remove the node which has the wrong IP address, referring it's hostname

> **\# monmaptool --rm node2 /tmp/monitor\_map.bin**

4\. Inspect the monitor map to see if the monitor is indeed removed.

> **\# monmaptool --print /tmp/monitor\_map.bin**
> 
> monmaptool: monmap file monmap epoch 1 fsid d978794d-5835-4ac3-8fe3-3855b18b9572 last\_changed 0.000000 created 0.000000

5\. Add a new monitor (or the existing monitor with it's new IP)

> **\# monmaptool --add node3  192.168.122.76:6789  /tmp/monitor\_map.bin**
> 
> monmaptool: monmap file monmap monmaptool: writing epoch 1 to monmap (1 monitors)

6\. Check the monitor map to confirm the changes

> **\# monmaptool --print monmap**
> 
> monmaptool: monmap file monmap epoch 1 fsid d978794d-5835-4ac3-8fe3-3855b18b9572 last\_changed 0.000000 created 0.000000 0: 192.168.122.76:6789/0 mon.node3

7\. Make sure the mon processes are not running on the monitor nodes

> **\# service ceph stop mon**

8\. Upload the changes

> **\# ceph-mon -i monitor\_node --inject-monmap /tmp/mon\_map.bin**

9\. Start the mon process on each monitor

> **\# service ceph start mon**

10\. Check if the cluster has taken in the changes.

> **\# ceph -s**
