FS-Cache and CacheFS, what are the differences?
###############################################
:date: 2014-09-14 15:49
:author: arvimal
:category: Techno
:tags: cachefs, fs-cache
:slug: fs-cache-and-cachefs-what-are-the-differences
:status: published

FS-Cache and CacheFS. Are there any differences between these two? Initially, I thought both were same. But no, it's not.

CacheFS is the backend implementation which caches the data onto the disk and mainpulates it, while FS-Cache is an interface which talks to CacheFS.

So why do we need two levels here?

FS-Cache was introduced as an API or front-end for CacheFS, which can be used by any file system driver. The file system driver talks with the FS-Cache API which inturn talks with CacheFS in the back-end. Hence, FS-Cache acts as a common interface for the file system drivers without the need to understand the backend CacheFS complexities, and how its implemented.

The only drawback is the additional code that needs to go into each file system driver which needs to use FS-Cache. ie.. Every file system driver that needs to talk with FS-Cache, has to be patched with the support to do so. Moreover, the cache structure differs slightly between file systems using it, and thus lacks a standard. This unfortunately, prevents FS-Cache from being used by every network filesystem out there.

The data flow would be as:

**VFS <-> File system driver (NFS/CIFS etc..) <-> FS-Cache <-> CacheFS <-> Cached data**

CacheFS need not cache every file in its entirety, it can also cache files partially. This partial caching mechanism is possible since FS-Cache caches 'pages' rather than an entire file. Pages are smaller fixed-size segments of data, and these are cached depending on how much the files are read initially.

FS-Cache does not require an open file to be loaded in the cache, prior being accessed. This is a nice feature as far as I understand, and the reasons are:

a) Not every open file in the remote file system can be loaded into cache, due to size limits. In such a case, only certain parts (pages) may be loaded. And the rest of the file should be accessed normally over the network.

b) The cache won't necessarily be large enough to hold all the open files on the remote system.

c) Even if the cache is not populated properly, the file should be accessible. ie.. the cache should be able to be bypassed totally.

This hopefully clears the differences between FS-Cache and CacheFS.
