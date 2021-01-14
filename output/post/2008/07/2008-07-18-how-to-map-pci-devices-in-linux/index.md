---
title: "How to map PCI devices in Linux ?"
date: "2008-07-18"
categories: 
  - "techno"
---

From the output of the command 'lspci -n' (The number after the colon, here '1679' from the below snip)

0a:04.0 0200: 14e4:1679 (rev a3) Subsystem: 103c:703c Control: I/O- Mem+ BusMaster+ SpecCycle- MemWINV- VGASnoop- ParErr+ Stepping- SERR+ FastB2B- Status: Cap+ 66MHz+ UDF- FastB2B+ ParErr- DEVSEL=medium Latency: 64 (16000ns min), Cache Line Size: 64 bytes Interrupt: pin A routed to IRQ 138 Region 0: Memory at fdef0000 (64-bit, non-prefetchable) \[size=64K\] Region 2: Memory at fdee0000 (64-bit, non-prefetchable) \[size=64K\]

IMPORTANT: -------------------

In the above line "14e4:1679", '14e4' is the UID of the manufacturer and '1679' is the card model or hardware ID.

The actual way to proceed is to open the pci.ids file ('/usr/share/hwdata/pci.ids' and '/lib/modules/\`uname -r\`/modules.pcimap') and check for the manufacturer UID, like '14e4' which is the 'Broadcom Corporation'. The file /lib/modules/\`uname -r\`/modules.pcimap would be more reliable since it is from the modules of the loaded kernel.

Under that, check the card model, like '1679' which is 'NetXtreme BCM5715S Gigabit Ethernet'.

Under that you can also have subdivisions, so in order to pin-point a particular card you will have to use the 'Subsystem' value from 'lspci'.

In this example, 'Subsystem' is 103c:703c, which turns out to be 'NC326i PCIe Dual Port Gigabit Server Adapter'
