Sharding the Ceph RADOS Gateway bucket index
############################################
:date: 2016-06-30 15:25
:author: arvimal
:category: Ceph
:tags: ceph, rados, Rados Gateway, RGW, rgw index, sharding
:slug: sharding-the-ceph-rados-gateway-bucket-index
:status: published

**S**\ harding is the process of breaking down data onto multiple locations so as to increase parallelism, as well as distribute load. This is a common feature used in databases. Read more on this at \ `Wikipedia <https://en.wikipedia.org/wiki/Shard_(database_architecture)>`__.

The concept of sharding is used in Ceph, for splitting the bucket index in a RADOS Gateway.

RGW or RADOS Gateway keeps an index for all the objects in its buckets for faster and easier lookup. For each RGW bucket created in a pool, the corresponding index is created in the ``XX.index`` pool.

For example, for each of the buckets created in ``.rgw`` pool, the bucket index is created in ``.rgw.buckets.index`` pool. For each bucket, the index is stored in a single RADOS object.

When the number of objects increases, the size of the RADOS object increases as well. Two problems arise due to the increased index size.

#. RADOS does not work good with large objects since it's not designed as such. Operations such as recovery, scrubbing etc.. work on a single object. If the object size increases, OSDs may start hitting timeouts because reading a large object may take a long time. This is one of the reason that all RADOS client interfaces such as RBD, RGW, CephFS use a standard 4MB object size.
#. Since the index is stored in a single RADOS object, only a single operation can be done on it at any given time. When the number of objects increases, the index stored in the RADOS object grows. Since a single index is handling a large number of objects, and there is a chance the number of operations also increase, parallelism is not possible which can end up being a bottleneck. Multiple operations will need to wait in a queue since a single operation is possible at a time.

In order to work around these problems, the bucket index is sharded into multiple parts. Each shard is kept on a separate RADOS object within the index pool.

Sharding is configured with the tunable ``bucket_index_max_shards`` . By default, this tunable is set to ``0`` which means that there are no shards.

How to check if Sharding is set?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. List the buckets
   [code language="bash"]
   # radosgw-admin metadata bucket list
   [
   "my-new-bucket"
   ]
   [/code]
#. Get information on the bucket in question[code language="bash"]

   | # radosgw-admin metadata get bucket:my-new-bucket
   | {
   | "key": "bucket:my-new-bucket",
   | "ver": {
   | "tag": "_bGZAVUgayKVwGNgNvI0328G",
   | "ver": 1
   | },
   | "mtime": 1458940225,
   | "data": {
   | "bucket": {
   | "name": "my-new-bucket",
   | "pool": ".rgw.buckets",
   | "data_extra_pool": ".rgw.buckets.extra",
   | "index_pool": ".rgw.buckets.index",
   | "marker": "default.2670570.1",
   | "bucket_id": "default.2670570.1"
   | },
   | "owner": "rgw_user",
   | "creation_time": 1458940225,
   | "linked": "true",
   | "has_bucket_info": "false"
   | }
   | }

   [/code]

#. Use the bucket ID to get more information, including the number of shards.

| [code language="bash"]
| radosgw-admin metadata get bucket.instance:my-new-bucket:default.2670570.1
| {
| "key": "bucket.instance:my-new-bucket:default.2670570.1",
| "ver": {
| "tag": "_xILkVKbfQD7reDFSOB4a5VU",
| "ver": 1
| },
| "mtime": 1458940225,
| "data": {
| "bucket_info": {
| "bucket": {
| "name": "my-new-bucket",
| "pool": ".rgw.buckets",
| "data_extra_pool": ".rgw.buckets.extra",
| "index_pool": ".rgw.buckets.index",
| "marker": "default.2670570.1",
| "bucket_id": "default.2670570.1"
| },
| "creation_time": 1458940225,
| "owner": "rgw_user",
| "flags": 0,
| "region": "default",
| "placement_rule": "default-placement",
| "has_instance_obj": "true",
| "quota": {
| "enabled": false,
| "max_size_kb": -1,
| "max_objects": -1
| },
| "num_shards": 0,
| "bi_shard_hash_type": 0
| },
| "attrs": [
| {
| "key": "user.rgw.acl",
| "val": "AgKPAAAAAgIaAAAACAAAAHJnd191c2VyCgAAAEZpcnN0IFVzZXIDA2kAAAABAQAAAAgAAAByZ3dfdXNlcg8AAAABAAAACAAAAHJnd191c2VyAwM6AAAAAgIEAAAAAAAAAAgAAAByZ3dfdXNlcgAAAAAAAAAAAgIEAAAADwAAAAoAAABGaXJzdCBVc2VyAAAAAAAAAAA="
| },
| {
| "key": "user.rgw.idtag",
| "val": ""
| },
| {
| "key": "user.rgw.manifest",
| "val": ""
| }
| ]
| }
| }

| [/code]
| Note that \`num_shards\` is set to 0, which means that sharding is not enabled.

How to configure Sharding?
~~~~~~~~~~~~~~~~~~~~~~~~~~

To configure sharding, we need to first dump the region info.

**NOTE:** By default, RGW has a region named ``default`` even if regions are not configured.

| [code language="bash"]
| # radosgw-admin region get > /tmp/region.txt

| # cat /tmp/region.txt
| {
| "name": "default",
| "api_name": "",
| "is_master": "true",
| "endpoints": [],
| "hostnames": [],
| "master_zone": "",
| "zones": [
| {
| "name": "default",
| "endpoints": [],
| "log_meta": "false",
| "log_data": "false",
| "bucket_index_max_shards": 0
| }
| ],
| "placement_targets": [
| {
| "name": "default-placement",
| "tags": []
| }
| ],
| "default_placement": "default-placement"
| }

| [/code]
| Edit the file /tmp/region.txt, change the value for \`bucket_index_max_shards\` to the needed shard value (we're setting it to 8 in this example), and inject it back to the region.

| [code language="bash"]
| # radosgw-admin region set < /tmp/region.txt
| {
| "name": "default",
| "api_name": "",
| "is_master": "true",
| "endpoints": [],
| "hostnames": [],
| "master_zone": "",
| "zones": [
| {
| "name": "default",
| "endpoints": [],
| "log_meta": "false",
| "log_data": "false",
| "bucket_index_max_shards": 8
| }
| ],
| "placement_targets": [
| {
| "name": "default-placement",
| "tags": []
| }
| ],
| "default_placement": "default-placement"
| }
| [/code]
| Reference:

#. `Red Hat Ceph Storage 1.3 Rados Gateway documentation <https://access.redhat.com/documentation/en/red-hat-ceph-storage/version-1.3/red-hat-ceph-storage-13-ceph-object-gateway-for-rhel-x86-64/#configure-bucket-sharding>`__
#. https://en.wikipedia.org/wiki/Shard_(database_architecture)
