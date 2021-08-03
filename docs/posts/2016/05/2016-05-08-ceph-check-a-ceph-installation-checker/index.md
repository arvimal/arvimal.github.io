---
title: "`ceph-check` - A Ceph installation checker"
date: 2016-05-08
categories:
  - "ceph"
  - "programming"
  - "python"
---

Many a user wants to know if a Ceph cluster installation has been done to a specific suggested guideline.

Technologies like RAID is better avoided in Ceph due to an additional layer, which Ceph already takes care of.

I've started writing a tool which can be run from the Admin node, and it aims to check various such points.

The code can be seen at [https://github.com/arvimal/ceph\_check](https://github.com/arvimal/ceph_check)

The work is slow, really slow, due to my daily work, procrastination, and what not, even though I intend to finish this fast.
