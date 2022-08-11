---
title: "Ceph Rados Block Device (RBD) and TRIM"
date: 2015-10-07
categories:
  - "ceph"
tags:
  - "ceph"
  - "discard"
  - "fstrim"
  - "objects"
  - "rados"
  - "rados-block-device"
  - "rbd"
  - "trim"
---
<!--more-->
I recently came across a scenario where the objects in a RADOS pool used for an RBD block device doesn’t get removed, even if the files created through the mount point were removed.

I had an RBD image from an RHCS1.3 cluster mapped to a RHEL7.1 client machine, with an XFS filesystem created on it, and mounted locally. Created a 5GB file, and I could see the objects being created in the rbd pool in the ceph cluster.

1.RBD block device information

\[code language="bash"\] # rbd info rbd\_img rbd image 'rbd\_img': size 10240 MB in 2560 objects order 22 (4096 kB objects) block\_name\_prefix: rb.0.1fcbe.2ae8944a format: 1 \[/code\]

An XFS file system was created on this block device, and mounted at **/test.**

2.Write a file onto the RBD mapped mount point. Used ‘**dd**’ to write a 5GB file.

\[code language="bash"\] # dd if=/dev/zero of=/mnt/rbd\_image.img bs=1G count=5 5+0 records in 5+0 records out 5368709120 bytes (5.4 GB) copied, 8.28731 s, 648 MB/s \[/code\]

3.Check the objects in the backend RBD pool

\[code language="bash"\] # rados -p rbd ls | wc -l &lt; Total number of objects in the 'rbd' pool&gt; \[/code\]

4.Delete the file from the mount point.

\[code language="bash"\] # rm /test/rbd\_image.img -f # ls /test/ --NO FILES LISTED-- \[/code\]

5.List the objects in the RBD pool

\[code language="bash"\] # rados -p rbd ls | wc -l < Total number of objects in the 'rbd' pool > \[/code\]

The number of objects doesn’t go down as we expect, after the file deletion. It remains the same, wrt to step 3.

Why does this happen? This is due to the fact that traditional file systems do not delete the underlying data blocks even if the files are deleted.

The process of writing a file onto a file system involves several steps like finding free blocks and allocating them for the new file, creating an entry in the directory entry structure of the parent folder, setting the name and inode number in the directory entry structure, setting pointers from the inode to the data blocks allocated for the file etc..

When data is written to the file, the data blocks are used to store the data. Additional information such as the file size, access times etc.. are updated in the inode after the writes.

Deleting a file involves removing the pointers from the inode to the corresponding data blocks, and also clearing the name<->inode mapping from the directory entry structure of the parent folder. But, the underlying data blocks are not cleared off, since that is a high I/O intensive operation. So, the data remains on the disk, even if the file is not present. A new write will make the allocator take these blocks for the new data, since they are marked as not-in-use.

This applies for the files created on an RBD device as well. The files created on top of the RBD-mapped mount point will ultimately be mapped to objects in the RADOS cluster. When the file is deleted from the mount point, since the entry is removed, it doesn’t show up in the mount point.

But, since the file system doesn’t clear off the underlying block device, the objects remain in the **RADOS** pool. These would be normally over-written when a new file is created via the mount point.

But this has a catch though. Since the pool contains the objects even if the files are deleted, it consumes space in the rados pool (even if they'll be overwritten). An administrator won't be able to get a clear understanding on the space usage, if the pool is used heavily, and multiple writes are coming in.

In order to clear up the underlying blocks, or actually remove them, we can rely on the **TRIM** support most modern disks offer. Read more about **TRIM** at [Wikipedia](https://en.wikipedia.org/wiki/Trim_%28computing%29).

**TRIM** is a set of commands supported by HDD/SSDs which allow the operating systems to let the disk know about the locations which are not currently being used. Upon receiving a confirmation from the file system layer, the disk can go ahead and mark the blocks as not used.

For the TRIM commands to work, the disks and the file system has to have the support. All the modern file systems have built-in support for **TRIM**. Mount the file system with the '**discard**' option, and you're good to go.

\[code language="bash"\] # mount -o discard /dev/rbd{X}{Y} /{mount-point} \[/code\]
