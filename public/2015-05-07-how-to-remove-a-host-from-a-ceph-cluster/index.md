# How to remove a host from a Ceph cluster?


I'm still studying Ceph, and recently faced a scenario in which one of my Ceph nodes went down due to hardware failure. Even though my data was safe due to the replication factor, I was not able to remove the node from the cluster.

I could remove the OSDs on the node, but I didn't find a way to remove the node being listed in 'ceph osd tree'. I ended up editing the CRUSH map by hand, to remove the host, and uploaded it back. This worked as expected. Following are the steps I did to achieve this.

a) This was the state just after the node went down:

\[sourcecode language="bash" gutter="false"\]

\# ceph osd tree

\# id     weight    type     name                up/down        reweight -10        .08997    root     default -20        .01999            host hp-m300-5 00        .009995            osd.0                up             1 40        .009995            osd.4                up             1 -30        .009995            host hp-m300-9 10        .009995            osd.1                 down         0 -40        .05998            host hp-m300-4 20        .04999            osd.2                up             1 30        .009995            osd.3                up             1

\[/sourcecode\]

\[sourcecode language="bash" gutter="false"\]

\# ceph -w

    cluster 62a6a880-fb65-490c-bc98-d689b4d1a3cb     health HEALTH\_WARN 64 pgs degraded; 64 pgs stuck unclean; recovery 261/785 objects degraded (33.248%)     monmap e1: 1 mons at {hp-m300-4=10.65.200.88:6789/0}, election epoch 1, quorum 0 hp-m300-4     osdmap e130: 5 osds: 4 up, 4 in     pgmap v8465: 196 pgs, 4 pools, 1001 MB data, 262 objects         7672 MB used, 74192 MB / 81865 MB avail         261/785 objects degraded (33.248%)         64 active+degraded         132 active+clean \[/sourcecode\]

I started with marking the OSDs on the node out, and removing them. Note that I don't need to stop the OSD (osd.1) since the node carrying osd.1 is down and not accessible.

b) If not, you would've to stop the OSD using:

\[sourcecode language="bash" gutter="false"\] # sudo service osd stop osd.1 \[/sourcecode\]

c) Mark the OSD out, this is not ideally needed in this case since the node is already out.

\[sourcecode language="bash" gutter="false"\] # ceph osd out osd.1 \[/sourcecode\]

d) Remove the OSD from the CRUSH map, so that it does not receive any data. You can also get the crushmap, de-compile it, remove the OSD, re-compile, and upload it back.

Remove item id 1 with the name 'osd.1' from the CRUSH map.

\[sourcecode language="bash" gutter="false"\] # ceph osd crush remove osd.1 \[/sourcecode\]

e) Remove the OSD authentication key

\[sourcecode language="bash" gutter="false"\] # ceph auth del osd.1 \[/sourcecode\]

f) At this stage, I had to remove the OSD host from the listing but was not able to find a way to do so. The 'ceph-deploy' didn't have any tools to do this, other than 'purge', and 'uninstall'. Since the node was not f) accessible, these won't work anyways. A 'ceph-deploy purge' failed with the following errors, which is expected since the node is not accessible.

\[sourcecode language="bash" gutter="false"\] # ceph-deploy purge hp-m300-9

\[ceph\_deploy.conf\]\[DEBUG \] found configuration file at: /root/.cephdeploy.conf \[ceph\_deploy.cli\]\[INFO  \] Invoked (1.5.22-rc1): /usr/bin/ceph-deploy purge hp-m300-9 \[ceph\_deploy.install\]\[INFO  \] note that some dependencies \*will not\* be removed because they can cause issues with qemu-kvm \[ceph\_deploy.install\]\[INFO  \] like: librbd1 and librados2 \[ceph\_deploy.install\]\[DEBUG \] Purging from cluster ceph hosts hp-m300-9 \[ceph\_deploy.install\]\[DEBUG \] Detecting platform for host hp-m300-9 ... ssh: connect to host hp-m300-9 port 22: No route to host \[ceph\_deploy\]\[ERROR \] RuntimeError: connecting to host: hp-m300-9 resulted in errors: HostNotFound hp-m300-9

\[/sourcecode\]

I ended up fetching the CRUSH map, removing the OSD host from it, and uploading it back.

g) Get the CRUSH map

\[sourcecode language="bash" gutter="false"\] # ceph osd getcrushmap -o /tmp/crushmap \[/sourcecode\]

h) De-compile the CRUSH map

\[sourcecode language="bash" gutter="false"\] # crushtool -d /tmp/crushmap -o crush\_map \[/sourcecode\]

i) I had to remove the entries pertaining to the host-to-be-removed from the following sections:

a) devices b) types c) And from the 'root' default section as well.

j) Once I had the entries removed, I went ahead compiling the map, and inserted it back.

\[sourcecode language="bash" gutter="false"\] # crushtool -c crush\_map -o /tmp/crushmap # ceph osd setcrushmap -i /tmp/crushmap \[/sourcecode\]

k) A 'ceph osd tree' looks much cleaner now :)

\[sourcecode language="bash" gutter="false"\] # ceph osd tree

\# id         weight             type         name                up/down        reweight -1             0.07999            root         default -2            0.01999                        host hp-m300-5 0            0.009995                    osd.0                down        0 4            0.009995                    osd.4                 down         0 -4            0.06                        host hp-m300-4 2            0.04999                        osd.2                 up             1 3            0.009995                    osd.3                 up             1 \[/sourcecode\]

There may be a more direct method to remove the OSD host from the listing. I'm not aware of anything relevant, based on my limited knowledge. Perhaps I'll come across something as I progress with Ceph. Comments welcome.

