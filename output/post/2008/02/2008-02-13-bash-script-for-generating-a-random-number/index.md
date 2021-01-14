---
title: "A random number generator in Bash"
date: "2008-02-13"
categories: 
  - "programming"
tags: 
  - "bash"
  - "random-number-generator"
---

The bash environment variable 'RANDOM' is a pseudo-random number generator built in bash, and it can generate random numbers in the range of 0 - 32767.

Using the command \`echo $RANDOM\`, we can generate a random number. Building a random number generator which emits a sequence of random numbers is pretty easy.

\[code language="bash"\] #!/bin/bash for i in \`seq 1 10\`: do echo $RANDOM; sleep 1s; done \[/code\]

The 'seq' or the 'sequential' can be used to generate a sequence of numbers.
