---
title: "Calculate a PG id from the hex values in Ceph OSD debug logs"
date: 2015-08-30
categories:
  - "ceph"
  - "programming"
  - "python"
tags:
  - "ceph"
  - "pg"
  - "python"
---

Recently, I had an incident where the OSDs were crashing at the time of startup. Obviously, the next step was to enable debug logs for the OSDs and understand where they were crashing.

Enabled OSD debug logs dynamically by injecting it with:

> \# ceph tell osd.\* injectargs --debug-osd 20 --debug-ms 1

_NOTE: This command can be run from the MON nodes._

Once this was done, the OSDs were started manually (since it were crashing and not running) and watched out for the next crash. It crashed with the following logs :

> \*read\_log 107487'1 (0'0) modify f6b07b93/rbd\_data.hash/head//12 by client.version date, time \*osd/PGLog.cc: In function 'static bool PGLog::read\_log(ObjectStore\*, coll\_t, hobject\_t, const pg\_info\_t&amp;, std::mapeversion\_t, hobject\_t&amp;, PGLog::IndexedLog&amp;, pg\_missing\_t&amp;, std::ostringstream&amp;, std::setstd::basic\_stringchar \*)' thread thread time date, time \*osd/PGLog.cc: 809: FAILED assert(last\_e.version.version e.version.version)ceph version version-details
>
> 1: (PGLog::read\_log(ObjectStore\*, coll\_t, hobject\_t, pg\_info\_t const&amp;, std::mapeversion\_t, hobject\_t, std::lesseversion\_t, std::allocatorstd::paireversion\_t const,hobject\_t , PGLog::IndexedLog&amp;, pg\_missing\_t&amp;, std::basic\_ostringstreamchar, std::char\_traitschar, std::allocatorchar, std::setstd::string, std::lessstd:string, std::allocatorstd::string \*)+0x13ee) \[0x6efcae\] 2: (PG::read\_state(ObjectStore\*, ceph::buffer::list&amp;)+0x315) \[0x7692f5\] 3: (OSD::load\_pgs()+0xfff) \[0x639f8f\] 4: (OSD::init()+0x7bd) \[0x63c10d\] 5: (main()+0x2613) \[0x5ecd43\] 6: (\_\_libc\_start\_main()+0xf5) \[0x7fdc338f9af5\] 7: /usr/bin/ceph-osd() \[0x5f0f69\]

The above is a log snippet at which the OSD process was crashing. The ceph-osd process was reading through the log areas of each PG in the OSD, and once it reached the problematic PG it crashed due to failing an assert condition.

Checking the source at 'osd/PGLog.cc', we see that this error is logged from 'PGLog::read\_log'.

> void PGLog::read\_log(ObjectStore \*store, coll\_t pg\_coll, coll\_t log\_coll, ghobject\_t log\_oid, const pg\_info\_tinfo, mapeversion\_t, hobject\_tdivergent\_priors, IndexedLoglog, pg\_missing\_tmissing, ostringstreamoss, setstring \*log\_keys\_debug) { ... if (!log.log.empty()) { pg\_log\_entry\_t last\_e(log.log.back()); assert(last\_e.version.version e.version.version);    == The assert condition at which read\_log is failing for a particular PG assert(last\_e.version.epoch = e.version.epoch);

In order to make the OSD start, we needed to move this PG to a different location using the 'ceph\_objectstore\_tool' so that the ceph-osd can bypass the problematic PG. To understand the PG where it was crashing, we had to do some calculations based on the logs.

The 'read\_log' line in the debug logs contain a hex value after the string "modify" and that is the hash of the PG number. The last number in that series is the pool id (12 in our case). The following python code will help to calculate the PG id based on the arguments passed to it.

This program accepts three arguments, the first being the hex value we talked about, the second being the pg\_num of the pool, and the third one being the pool id.

\[code language="python"\]

#!/usr/bin/env python # Calculate the PG ID from the object hash # vimal@redhat.com import sys

def pg\_id\_calc(\*args): if any(\[len(args) == 0, len(args) > 3, len(args) < 3\]): help() else: hash\_hex = args\[0\] pg\_num = int(args\[1\]) pool\_id = int(args\[2\]) hash\_dec = int(hash\_hex, 16) id\_dec = hash\_dec % pg\_num id = hex(id\_dec) pg\_id = str(pool\_id) + "." + str(id)\[2:\] print("\\nThe PG ID is %s\\n" % pg\_id)

def help(): print("Usage:") print("This script expects the hash (in Hex), pg\_num of the pool, and the pool id as arguments, in order") print("\\nExample:") print("./pg\_id\_calc.py 0x8e2fe5d7 2048 12") sys.exit()

if \_\_name\_\_ == '\_\_main\_\_': pg\_id\_calc(\*sys.argv\[1:\])

\[/code\]

An example of the program in action:

> \# python pg\_id\_calc.py 0xf6b07b93 2048 12 The PG ID is 12.393

Once we get the PG ID, we can proceed using 'ceph\_objectstore\_tool' to move the PG to a different location altogether. More on how to use 'ceph\_objectstore\_tool' in an upcoming journal.
