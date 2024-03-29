---
title: "List RBD images, snapshots, and clones in Ceph pools"
date: 2015-10-15
categories:
  - "ceph"
---
<!--more-->
This is a crude bash one-liner I did to get the details of all the RBD images, as well as the information on snapshots and clones created from them.

\[code language="bash"\] # for pool in \`rados lspools\`; do echo "POOL :" $pool; rbd ls -l $pool; echo "-----"; done \[/code\]

This will print an output similar to the following:

\[code language="bash"\] POOL : rbd NAME                             SIZE        PARENT  FMT PROT LOCK test\_img                        10240M                    1 test\_img2                      1024M                      2 test\_img2@snap2      1024M                      2                    yes ----- POOL : .rgw.root ----- POOL : .rgw.control ----- POOL : .rgw ----- POOL : .rgw.gc ----- POOL : .users.uid ----- POOL : .users ----- POOL : .users.swift ----- POOL : .users.email ----- POOL : .rgw.buckets.index ----- POOL : images NAME           SIZE      PARENT                               FMT PROT LOCK clone1           1024M  rbd/test\_img2@snap2             2 ----- \[/code\]
