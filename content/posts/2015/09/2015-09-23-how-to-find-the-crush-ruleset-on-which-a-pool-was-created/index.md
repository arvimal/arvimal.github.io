---
title: "Custom CRUSH rulesets and pools"
date: 2015-09-23
categories:
  - "ceph"
---

Ceph supports custom rulesets via [CRUSH](http://ceph.com/papers/weil-crush-sc06.pdf), which can be used to sort hardware based on various features such as speed and other factors, set custom weights, and do a lot of other useful things.

Pools, or the buckets were the data is written to, can be created on the custom rulesets, hence positioning the pools on specific hardware as per the administrator's need.

A large Ceph cluster may have lots of pools and rulesets specific for multiple use-cases. There may be times when we'd like to understand the pool to ruleset mapping.

The default CRUSH ruleset is named ‘replicated\_ruleset’. The available CRUSH rulesets can be listed with:

> **$ ceph osd crush rule ls**

On a fresh cluster, or one without any custom rulesets, you’d find the following being printed to stdout.

> **\# ceph osd crush rule ls** \[ "replicated\_ruleset" \]

I’ve got a couple more on my cluster, and this is how it looks:

> **\# ceph osd crush rule ls** \[ "replicated\_ruleset", "replicated\_ssd", "erasure-code"\]

Since this article looks into the mapping of pools to CRUSH rulesets, it’d be good to add in how to list the pools, as a refresher.

> **\# ceph osd lspools**

On my Ceph cluster, it turned out to be:

> **\# ceph osd lspools** 0 data,1 metadata,2 rbd,21 .rgw,22 .rgw.root,23 .rgw.control,24 .rgw.gc,25 .users.uid,26 .users,27 .users.swift,28 test\_pool,

Since you have the pool name you’re interested in, let’s see how to map it to the ruleset. The command syntax is:

> **\# ceph osd pool get <pool\_name> crush\_ruleset**

I was interested to understand the ruleset on which the pool ‘test\_pool’ was created. The command to list this was:

> **\# ceph osd pool get test\_pool crush\_ruleset** crush\_ruleset: 1

Please note that the rulesets are numbered from ‘0’, and hence ‘1’ would map to the CRUSH ruleset ‘replicated\_ssd’.

We'll try to understand how a custom ruleset is created, in another article.
