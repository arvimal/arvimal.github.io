# Compacting a Ceph monitor store

<!--more-->
The Ceph monitor store growing to a big size is a common occurrence in a busy Ceph cluster.

If a '_**ceph -s**_' takes considerable time to return information, one of the possibility is the monitor database being large.

Other reasons included network lags between the client and the monitor, the monitor not responding properly due to the system load, firewall settings on the client or monitor etc..

The best way to deal with a large monitor database is to compact the monitor store. The monitor store is a [leveldb](http://leveldb.org/) store which stores key/value pairs.

There are two ways to compact a levelDB store, either on the fly or at the monitor process startup.

To compact the store dynamically, use :

> \# ceph tell mon.\[ID\] compact

To compact the levelDB store every time the monitor process starts, add the following in /etc/ceph/ceph.conf under the \[mon\] section:

> mon compact on start = true

The second option would compact the levelDB store each and every time the monitor process starts.

The monitor database is stored at _/var/lib/ceph/mon/<hostname>/store.db/_ as files with the extension '**.sst**', which is the synonym for '**Sorted String Table**'

To read more on levelDB, please refer:

[https://en.wikipedia.org/wiki/LevelDB](https://en.wikipedia.org/wiki/LevelDB)

[http://leveldb.googlecode.com/svn/trunk/doc/impl.html](http://leveldb.googlecode.com/svn/trunk/doc/impl.html)

[http://google-opensource.blogspot.in/2011/07/leveldb-fast-persistent-key-value-store.html](http://google-opensource.blogspot.in/2011/07/leveldb-fast-persistent-key-value-store.html)

