---
title: "\"Error: open /tmp/docker-import-123456789/repo/bin/json: no such file or directory\""
date: 2014-08-16
categories:
  - "techno"
---
<!--more-->
I've been trying to create a minimal docker image for RHEL versions, for one of my projects. The following were the steps I followed:

a) Installed a RHEL6.5 server with 'Minimal Installation'.

b) Registered it to the local satellite.

c) Created a tar-ball of the filesystem with the command below:

```bash

\# tar --numeric-owner --exclude=/proc --exclude=/sys --exclude=/mnt --exclude=/var/cache

\--exclude=/usr/share/doc --exclude=/tmp --exclude=/var/log -zcvf /mnt/rhel6.5-base.tar.gz /

```

d) Load the tar.gz image using 'docker load' (as per the man page of 'docker load')

```bash

\# docker load -i rhel6.5-base.tar.gz

```

This is where it erred with the message:

```bash

2014/08/16 20:37:42 Error: open /tmp/docker-import-123456789/repo/bin/json: no such file or directory

```

After a bit of searching and testing, I found that 'docker load -i' doesn't work as expected. The workaround is to cat and pipe the tar.gz file, as shown below:

```bash

\# cat rhel6.5-base.tar.gz | docker import - rhel6/6.5

```

This ends up with the image showing up in 'docker images'

```bash

\# docker images

REPOSITORY   TAG    IMAGE ID           CREATED                  VIRTUAL SIZE rhel6/6.1           latest  32b4b345454a  About a minute ago 1.251 GB

```

Update: 'docker load -i <image-file>' would only work if the image is created as a layered docker image. If the <image-file> is a tar ball created from a root filesystem, you would need to use 'cat <image-file> | docker import <name>'
