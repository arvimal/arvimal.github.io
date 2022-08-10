# How to list all the configuration settings in a Ceph cluster monitor?


It can be really helpful to have a single command to list all the configuration settings in a monitor node, in a Ceph cluster.

This is possible by interacting directly with the monitor's unix socket file. This can be found under /var/run/ceph/. By default, the admin socket for the monitor will be in the path /var/run/ceph/ceph-mon.<hostname-s>.asok.

The default location can vary in case you have defined it to be a different one, at the time of the installation. To know the actual socket path, use the following command:

\[sourcecode language="bash" gutter="false"\]

\# ceph-conf --name mon.$(hostname -s) --show-config-value admin\_socket

\[/sourcecode\]

This should print the location of the admin socket. In most cases, it should be something like /var/run/ceph/ceph-mon.$(hostname -s).asok

Once you have the monitor admin socket, use that location to show the various configuration settings with:

\[sourcecode language="bash" gutter="false"\]

\# ceph daemon /var/run/ceph/ceph-mon.\*.asok config show

\[/sourcecode\]

The output would be long, and won't fit in a single screen. You can either pipe it to 'less' or grep for a specific value in case you know what you are looking for.

For example, if I need to look at the ratio at which the OSD would be considered full, I'll be using:

\[sourcecode language="bash" gutter="false"\]

#  ceph daemon /var/run/ceph/ceph-mon.\*.asok config show | grep mon\_osd\_full\_ratio

\[/sourcecode\]

