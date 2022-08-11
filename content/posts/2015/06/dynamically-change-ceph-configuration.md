---
title: "Another method to dynamically change a Ceph configuration"
date: 2015-06-03
categories:
  - "ceph"
tags:
  - "ceph"
---
<!--more-->
In a previous post, we saw how to dynamically change a tunable on a running Ceph cluster dynamically. Unfortunately, such a change is not permanent, and will revert back to the previous setting once ceph is restarted.

Rather than using the command '_**ceph tell**_', I recently came upon another way to change configuration values.

We'll try changing the tunable '**mon\_osd\_full\_ratio**' once again.

1\. Get the current setting

> **\# ceph daemon osd.1 config get mon\_osd\_full\_ratio** { "mon\_osd\_full\_ratio": "0.75"}

2\. Change the configuration value using 'ceph daemon'.

> **\# ceph daemon osd.1 config set mon\_osd\_full\_ratio 0.85** { "success": "mon\_osd\_full\_ratio = '0.85' "}

3\. Check if the change has been introduced.

> **\# ceph daemon osd.1 config get mon\_osd\_full\_ratio** { "mon\_osd\_full\_ratio": "0.85"}

4\. Restart the 'ceph' service

> **\# service ceph restart**

5\. Check the status

> **\# ceph daemon osd.1 config get mon\_osd\_full\_ratio** { "mon\_osd\_full\_ratio": "0.75"}

NOTE: Please note that the changes introduced with 'ceph tell' as well as 'ceph daemon' is not persistent across process restarts.
