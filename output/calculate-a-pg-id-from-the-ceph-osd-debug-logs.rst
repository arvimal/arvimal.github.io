Calculate a PG id from the hex values in Ceph OSD debug logs
############################################################
:date: 2015-08-30 19:35
:author: arvimal
:category: Ceph, Programming, Python
:tags: ceph, pg, python
:slug: calculate-a-pg-id-from-the-ceph-osd-debug-logs
:status: published

Recently, I had an incident where the OSDs were crashing at the time of startup. Obviously, the next step was to enable debug logs for the OSDs and understand where they were crashing.

Enabled OSD debug logs dynamically by injecting it with:

   # ceph tell osd.\* injectargs --debug-osd 20 --debug-ms 1

*NOTE: This command can be run from the MON nodes.*

Once this was done, the OSDs were started manually (since it were crashing and not running) and watched out for the next crash. It crashed with the following logs :

   | \*read_log 107487'1 (0'0) modify f6b07b93/rbd_data.hash/head//12 by client.version date, time
   | \*osd/PGLog.cc: In function 'static bool PGLog::read_log(ObjectStore*, coll_t, hobject_t, const pg_info_t&amp;,
   | std::mapeversion_t, hobject_t&amp;, PGLog::IndexedLog&amp;, pg_missing_t&amp;, std::ostringstream&amp;,
   | std::setstd::basic_stringchar \*)' thread thread time date, time
   | \*osd/PGLog.cc: 809: FAILED assert(last_e.version.version e.version.version)ceph version version-details

   | 1: (PGLog::read_log(ObjectStore*, coll_t, hobject_t, pg_info_t const&amp;, std::mapeversion_t, hobject_t,
   | std::lesseversion_t, std::allocatorstd::paireversion_t const,hobject_t , PGLog::IndexedLog&amp;,
   | pg_missing_t&amp;, std::basic_ostringstreamchar, std::char_traitschar, std::allocatorchar,
   | std::setstd::string, std::lessstd:string, std::allocatorstd::string \*)+0x13ee) [0x6efcae]
   | 2: (PG::read_state(ObjectStore*, ceph::buffer::list&amp;)+0x315) [0x7692f5]
   | 3: (OSD::load_pgs()+0xfff) [0x639f8f]
   | 4: (OSD::init()+0x7bd) [0x63c10d]
   | 5: (main()+0x2613) [0x5ecd43]
   | 6: (__libc_start_main()+0xf5) [0x7fdc338f9af5]
   | 7: /usr/bin/ceph-osd() [0x5f0f69]

The above is a log snippet at which the OSD process was crashing. The ceph-osd process was reading through the log areas of each PG in the OSD, and once it reached the problematic PG it crashed due to failing an assert condition.

Checking the source at 'osd/PGLog.cc', we see that this error is logged from 'PGLog::read_log'.

   | void PGLog::read_log(ObjectStore \*store, coll_t pg_coll,
   | coll_t log_coll,
   | ghobject_t log_oid,
   | const pg_info_tinfo,
   | mapeversion_t, hobject_tdivergent_priors,
   | IndexedLoglog,
   | pg_missing_tmissing,
   | ostringstreamoss,
   | setstring \*log_keys_debug)
   | {
   | ...
   | if (!log.log.empty()) {
   | pg_log_entry_t last_e(log.log.back());
   | assert(last_e.version.version e.version.version);    == The assert condition at which read_log is failing for a particular PG
   | assert(last_e.version.epoch = e.version.epoch);

In order to make the OSD start, we needed to move this PG to a different location using the 'ceph_objectstore_tool' so that the ceph-osd can bypass the problematic PG. To understand the PG where it was crashing, we had to do some calculations based on the logs.

The 'read_log' line in the debug logs contain a hex value after the string "modify" and that is the hash of the PG number. The last number in that series is the pool id (12 in our case). The following python code will help to calculate the PG id based on the arguments passed to it.

This program accepts three arguments, the first being the hex value we talked about, the second being the pg_num of the pool, and the third one being the pool id.

[code language="python"]

| #!/usr/bin/env python
| # Calculate the PG ID from the object hash
| # vimal@redhat.com
| import sys

| def pg_id_calc(*args):
| if any([len(args) == 0, len(args) > 3, len(args) < 3]):
| help()
| else:
| hash_hex = args[0]
| pg_num = int(args[1])
| pool_id = int(args[2])
| hash_dec = int(hash_hex, 16)
| id_dec = hash_dec % pg_num
| id = hex(id_dec)
| pg_id = str(pool_id) + "." + str(id)[2:]
| print("\nThe PG ID is %s\n" % pg_id)

| def help():
| print("Usage:")
| print("This script expects the hash (in Hex), pg_num of the pool, and the pool id as arguments, in order")
| print("\nExample:")
| print("./pg_id_calc.py 0x8e2fe5d7 2048 12")
| sys.exit()

| if \__name_\_ == '__main__':
| pg_id_calc(*sys.argv[1:])

[/code]

An example of the program in action:

   | # python pg_id_calc.py 0xf6b07b93 2048 12
   | The PG ID is 12.393

Once we get the PG ID, we can proceed using 'ceph_objectstore_tool' to move the PG to a different location altogether. More on how to use 'ceph_objectstore_tool' in an upcoming journal.
