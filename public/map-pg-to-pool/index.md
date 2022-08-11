# Mapping Placement Groups and Pools

<!--more-->
Understanding the mapping of Pools and Placement Groups can be very useful while troubleshooting Ceph problems.

A direct method is to dump information on the PGs via :

> \# ceph pg dump

This command should output something like the following:

> pg\_stat    objects    mip    degr    unf    bytes    log    disklog   state 5.7a           0                0         0          0        0            0       0            active+clean

The output will have more information, and I've omitted it for the sake of explanation.

The first field is the PG ID, which are two values separated by a single dot (.). The left side value is the POOL ID, while the right side value is the actual PG number. It means that a specific PG can only be present under a specific pool, ie.. no PGs can be shared across pools. But please note that OSDs can be shared across multiple PGs.

To get the pools and associated numbers, use:

> \# ceph osd lspools
>
> 0 data,1 metadata,2 rbd,5 ssdtest,6 ec\_pool,

So, the PG 5.7a belongs to the pool numbered '5', ie.. 'ssdtest', and the PG number is '7a'.

The output of 'ceph pg dump' also shows various important informations such as the Acting OSD set, the primary OSD, the last time the PG was reported, the state of the PG, the time at which a normal scrub as well as a deep-scrub was run etc..

