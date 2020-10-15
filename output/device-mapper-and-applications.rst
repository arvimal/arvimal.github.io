Device Mapper and applications
##############################
:date: 2010-12-23 05:11
:author: arvimal
:category: Techno
:slug: device-mapper-and-applications
:status: published

What is\ \ `device-mapper <http://en.wikipedia.org/wiki/Device_mapper>`__\ \ ?

**D**\ evice mapper is a modular driver for the `linux kernel 2.6 <http://www.kernel.org/>`__. It can be said as a framework which helps to create or map logical sectors of a pseudo `block device <http://en.wikipedia.org/wiki/Device_file>`__ to an underlying physical block device. So what device-mapper do is keep a table of mappings which equate the logical block devices to the physical block devices.

Applications such as LVM2, `EVMS <http://evms.sourceforge.net/>`__, software raid aka dmraid, multipathing, block encryption mechanisms such as cryptsetup etc... use device-mapper to work. All these applications excluding EVMS use the libdevmapper library to communicate with device-mapper.

The applications communicate with device-mapper's `API <http://en.wikipedia.org/wiki/Application_programming_interface>`__ to create the mapping. Due to this feature, device-mapper does not need to know what `LVM <http://en.wikipedia.org/wiki/Logical_Volume_Manager_%28Linux%29>`__ or dmraid is, how it works, what LVM metadata is, etc... It is upto the application to create the pseudo devices pointing to the physical volumes using one of device-mapper's targets and then update the mapper table.

The device-mapper mapping table :

The mapping table used by device-mapper doesn't take too much space and is a list created using a 'btree'. A btree or a '`Binary Search Tree <http://en.wikipedia.org/wiki/Binary_search_tree>`__' is a data-structure from which data can be added, removed or queried.

In order to know more on what a btree is and the concept behind it, read :

http://en.wikipedia.org/wiki/Binary_search_tree

http://en.wikipedia.org/wiki/B-tree

Types of device-mapper targets :

Applications which use device-mapper actually use one or more of its target methods to achieve their purpose. Targets can be said as a method or type of mapping used by device-mapper. The general mapping targets are :

a) Linear - Used by linear logical volumes, ie.. the default data layout method used by LVM2.

b) Striped - Used by striped logical volumes as well as software `RAID0 <http://en.wikipedia.org/wiki/Standard_RAID_levels>`__.

c) Mirror - Used by software RAID1 and LVM mirroring.

d) Crypt - Used by disk encryption utilties.

e) Snapshot - Used to take online snapshots of block devices, an example is LVM snapshot.

f) `Multipath <http://en.wikipedia.org/wiki/Multipath_I/O>`__ - Used by device-mapper-multipath.

g) RAID45 - `Software raid <http://en.wikipedia.org/wiki/RAID>`__ using device-mapper, ie.. dmraid

h) Error - Sectors of the pseudo device mapped with this target causes the I/O to fail.

There are a few more mappings such as 'flaky' which is not used much.

I'll write on how device-mapper works in LVM, in the next post...
