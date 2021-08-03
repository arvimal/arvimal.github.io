---
title: "OSD information in a scriptable format"
date: 2015-09-18
categories:
  - "ceph"
tags:
  - "ceph"
  - "osd"
---

In case you are trying to get the OSD ID and the corresponding node IP address mappings in a script-able format, use the following command:

> \# ceph osd find <OSD-num>

This will print the OSD number, the IP address, the host name, and the default root in the CRUSH map, as a python dictionary.

> \# ceph osd find 2 { "osd": 2, "ip": "192.168.122.112:6800\\/5311", "crush\_location": { "host": "node4", "root": "default"}}

The output is in json format, which has a key:value format. This can be parsed using awk/sed, or any programming languages that support json. All recent ones do.

For a listing of all the OSDs and related information, get the number of OSDs in the cluster, and then use that number to probe the OSDs.

> \# for i in \`seq 0 $(ceph osd stat | awk {'print $3'})\`; do
>
> ceph osd find $i; echo; done

This should output:

> { "osd": 0, "ip": "192.168.122.244:6805\\/2579", "crush\_location": { "host": "node3", "root": "ssd"}} { "osd": 1, "ip": "192.168.122.244:6800\\/955", "crush\_location": { "host": "node3", "root": "ssd"}} { "osd": 2, "ip": "192.168.122.112:6800\\/5311", "crush\_location": { "host": "node4", "root": "default"}} { "osd": 3, "ip": "192.168.122.112:6805\\/5626", "crush\_location": { "host": "node4", "root": "default"}} { "osd": 4, "ip": "192.168.122.82:6800\\/4194", "crush\_location": { "host": "node5", "root": "default"}} { "osd": 5, "ip": "192.168.122.82:6805\\/4521", "crush\_location": { "host": "node5", "root": "default"}} { "osd": 6, "ip": "192.168.122.73:6801\\/5614", "crush\_location": { "host": "node2", "root": "ssd"}} { "osd": 7, "ip": "192.168.122.73:6800\\/1719", "crush\_location": { "host": "node2", "root": "ssd"}} { "osd": 8, "ip": "192.168.122.10:6805\\/5842", "crush\_location": { "host": "node6", "root": "default"}} { "osd": 9, "ip": "192.168.122.10:6800\\/4356", "crush\_location": { "host": "node6", "root": "default"}} { "osd": 10, "ip": "192.168.122.109:6800\\/4517", "crush\_location": { "host": "node7", "root": "default"}} { "osd": 11, "ip": "192.168.122.109:6805\\/4821", "crush\_location": { "host": "node7", "root": "default"}}
