---
title: "DNS Zone file sanity check"
date: 2008-02-14
categories:
  - "programming"
---
<!--more-->
This bash script does a sanity check for the DNS domains defined inside /var/named.

\[code language="bash"\] #!/bin/bash A=\`ls -l /var/named/\*.db | awk '{print $9}' | cut -f4 -d "/" | sed 's/.db$//'\` #domain names

for i in $A; do named-checkzone $i /var/named/$i.db;done \[/code\]
