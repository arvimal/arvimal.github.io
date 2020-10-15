Resetting Calamari password
###########################
:date: 2015-07-13 17:57
:author: arvimal
:category: Ceph
:tags: calamari, ceph
:slug: how-can-we-resetchange-the-calamari-interface-password
:status: published

'**Calamari**' is the monitoring interface for a Ceph cluster.

The Calamari interface password can be reset/changed using the 'calamari-ctl' command.

   # calamari-ctl change_password --password {password} {user-name}

**calamari-ctl** can also be used to add a user, as well as disable, enable, and rename the user account. A '--help' should print out all the available ones.

   # calamari-ctl --help
