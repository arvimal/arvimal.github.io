---
title: "FSCache and the on-disk structure of the cached data"
date: 2014-11-12
categories:
  - "techno"
tags:
  - "cachefilesd"
  - "cachefs"
  - "fscache"
---

The 'cachefilesd' kernel module will create two directories at the location specified in /etc/cachefilesd.conf. By default it's /var/cache/fscache/.

> **\[root@montypython ~\]# lsmod |grep -i cache** cachefiles             40871  1 fscache                62354  3 nfs,cachefiles,nfsv4

Those are _/var/cache/fscache/cache_ and _/var/cache/fscache/graveyard_.

The cache structure is maintained inside '/var/cache/fscache/cache/', while anything that is retired or culled is moved to 'graveyard'. The 'cachefilesd' daemon monitors 'graveyard' using 'dnotify' and will delete anything that is in there.

We'll try an example. Consider an NFS share mounted with fscache support. The share contains the following files, with some random text.

> **\# ls /vol1** files1.txt  files2.txt  files3.txt  files4.txt

a) Configure 'cachefiles' by editing '/etc/cachefilesd.conf', and start the 'cachefilesd' daemon.

> **\# systemctl start cachefilesd**

b) Mount the NFS share on the client with the 'fsc' mount option, to enable 'fscache' support.

> **\# sudo mount localhost:/vol1 /vol1-backup/ -o fsc**

d) Access the data from the mount point, and fscache will create the backed caching index at the location specified in _/etc/cachefilesd.conf_. By default, its _/var/cache/fscache/_

e) Once the files are accessed on the client side, fscache builds an index as following:

NOTE: The index structure is **dependent** on the netfs (NFS in our case). The netfs driver can structure the cache index as it seems fit.

Explanation of the caching structure:

> \# tree /var/cache/fscache/ /var/cache/fscache/cache/ └── @4a └── I03nfs ├── @22 │   └── Jo00000008400000000000000000000000400 │      └── @59 │           └── J110000000000000000w080000000000000000000000 │               ├── @53 │               │   └── EE0g00sgwB-90600000000ww000000000000000 │               ├── @5e │               │   └── EE0g00sgwB-90600000000ww000000000000000 │               ├── @61 │               │   └── EE0g00sgwB-90600000000ww000000000000000 │               ├── @62 │               │   └── EE0g00sgwB-90600000000ww000000000000000 │               ├── @70 │               │   └── EE0g00sgwB-90600000000ww000000000000000 │               ├── @7c │               │   └── EE0g00sgwB-90600000000ww000000000000000 │               └── @e8 │                   └── EE0g00sgwB-90600000000ww0000000000000000 └── @42 └── Jc000000000000EggDj00 └── @0a

a) The '**cache**' directory under _/var/cache/fscache/_ is a special index and can be seen as the root of the entire cache index structure.

b) Data objects (actual cached files) are represented as files if they have no children, or folders if they have. If represented as a directory, data objects will have a file inside named 'data' which holds the data.

c) The '**cachefiles**' kernel module represents :

i)   '**index**' objects as '**directories**', starting with either '**I**' or '**J**'.

ii)  Data objects are represented with filenames, beginning with '**D**' or '**E**'.

iii) Special objects are similar to data objects, and start with '**S**' or '**T**'.

In general, any object would be represented as a folder, if that object has children.

g) In the directory hierarchy, immediately between the parent object and its child object, are directories named with \***hash values**\* of the immediate child object keys, starting with an '**@**'.

The child objects are placed inside this directory.These child objects would be folders, if it has child objects, or files if its the cached data itself. This can go on till the end of the path and reaches the file where the cached data is.

Representation of the object indexes (For NFS, in this case)

> INDEX     INDEX      INDEX                             DATA FILES ========= ========== ================================= ================ cache/@4a/I03nfs/@30/Ji000000000000000--fHg8hi8400 cache/@4a/I03nfs/@30/Ji000000000000000--fHg8hi8400/@75/Es0g000w...DB1ry cache/@4a/I03nfs/@30/Ji000000000000000--fHg8hi8400/@75/Es0g000w...N22ry cache/@4a/I03nfs/@30/Ji000000000000000--fHg8hi8400/@75/Es0g000w...FP1ry
