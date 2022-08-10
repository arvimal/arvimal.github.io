# What is data scrubbing?


Data Scrubbing is an error checking and correction method or routine check to ensure that the data on file systems are in pristine condition, and has no errors. Data integrity is of primary concern in today's conditions, given the humongous amounts of data being read and written daily.

A simple example for a scrubbing, is a file system check done on file systems with tools like 'e2fsck' in EXT2/3/4, or 'xfs\_repair' in XFS. Ceph also includes a daily scrubbing as well as weekly scrubbing, which we will talk about in detail in another article.

This feature is available on most hardware RAID controllers, backup tools, as well as softwares that emulate RAID such as MD-RAID.

Btrfs is one of the file systems that can schedule a internal scrubbing automatically, to ensure that corruptions are detected and preventive measures taken automatically. Since Btrfs can maintain multiple copies of data, once it finds an error in the primary copy, it can check for a good copy (if mirroring is used) and replace it.

We will be looking more into scrubbing, especially how it is implemented in Ceph, and the various tunables, in an upcoming post.

