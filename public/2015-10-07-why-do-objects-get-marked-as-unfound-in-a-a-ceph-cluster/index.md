# Ceph and unfound objects


In certain cases, a Ceph cluster may move away from an HEALTHY state due to “**unfound**” objects.

A “**_ceph -s_**” should show if you have any unfound objects. So, what are unfound objects? How does an object become “**unfound**”? This article tries to explain why/how “**unfound**” objects come into existence.

Let’s look into the life cycle of a write to a pool.

- The client contacts a Ceph monitor and fetches the CRUSH map, which includes:
    - MON map
    - OSD map
    - PG map
    - CRUSH map
    - MDS map

Once the client has the maps, the Ceph client-side algorithm breaks the data being written into objects (the object size depends on the client side configuration). Clients such as RBD and RGW uses a 4MB object size, but RADOS doesn’t actually have such a limitation.

Each pool has a set of **Placement Groups** (**PG**) assigned to it at the time of creation, and the client always writes to a pool. Since the client has the maps which talks about the entire cluster, it knows the placement groups within the pool which it is writing to, and the OSDs assigned for each placement group. The client talks to the OSDs directly without going over any other path, such as a monitor.

The PG map will have the **ACTING** and **UP** OSD sets for each PG. To understand the ACTING set and UP set for the PGs, as well as a plethora of other information, use :

\[code language="bash"\] # ceph pg dump \[/code\]

The ACTING set is the current active set of OSDs that stores the replica sets for that particular PG. The UP set is the set of OSDs that are currently up and running. Usually, the ACTING set and UP set are the same. When an OSD in the ACTING set is not reachable, other OSDs wait for 5 minutes (which is configurable) for it to come back online (this is checked with a hearbeat).

The said OSD is removed out of the UP set when it is not accessible. If it doesn’t come back online within the configured period, the said OSD is marked out of the ACTING set, as well as the UP set. When it comes back, it is added back to the ACTING/UP set and a peering happens where the data is synced back.

Let’s discuss the scenario where an “unfound” object came come into existence. Imagine a pool with a two replica configuration. A write that goes into the pool is split into objects and stored in the OSDs which are in the ACTIVE set of a PG.

- One OSD in the ACTING set goes down.
- The write is done on the second OSD which is UP and ACTING.
- The first OSD which went down, came back up.
- The peering process started between the first OSD (that came back), and the second OSD (that serviced the write).
    - Peering refers to the process of arriving at an understanding on the object states between the OSDs in an ACTING set, and sync up the metadata/data between them.
- Both the OSDs reach an understanding on which objects needs to be synced.
- The second OSD that had the objects ready to be synced, went down before the sync process starts or is in midway.

In this situation, the first OSD knows about the objects that was written to the second OSD, but cannot probe it. The first OSD will try to probe possible locations for copies, provided there are more replicas. If the OSD is able to find other locations, the data will be synced up.

But in case there are no other copies, and the OSD with the only copy is not coming up anytime soon (perhaps a disk crash, file system corruption etc..) the only way is to either mark the object as “lost”, or revert it back to the previous version. Reverting to a previous version may not be possible for a new object, and in such cases the only way would be to mark it as “lost” or copy from a backup.

1\. For a new object without a previous version:

\[code language="bash"\] # ceph pg {pg.num} mark\_unfound\_lost delete \[/code\]

2\. For an object which is likely to have a previous version:

\[code language="bash"\] # ceph pg {pg.num} mark\_unfound\_lost revert \[/code\]

**NOTE:** The upstream Ceph documentation has an excellent write-up about “unfound” objects [here](http://docs.ceph.com/docs/master/rados/troubleshooting/troubleshooting-pg/#unfound-objects).

I suggest reading the documentation prior taking any sort of action in a case where you see “unfound” objects in your cluster.

