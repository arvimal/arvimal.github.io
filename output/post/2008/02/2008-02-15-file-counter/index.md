---
title: "Recursive file counter in bash"
date: "2008-02-15"
categories: 
  - "programming"
tags: 
  - "file-counter"
---

Most of the scripts presented in this journal have been created while learning bash and having nothing much to do...

I think its usual to get crazy ideas and work trying to implement them, especially while learning any type of coding.  This  'File Counter' script came as such a  crazy idea. It was working at the time of its creation, but have not checked it recently.. should work..

This script counts the entire number of files irrespective the folders under the main directory you specify for this script to work on. ie.. It recursively  counts the files under a directory tree.

\[code language="bash"\] #!/bin/bash

#  Counts the number of files recursively inside a directory    # # echo ; clear echo -e "Please enter the directory location where you want the files to be counted...\\n" ; echo

read dir ; echo ;  if \[ ! -d $dir \] ; then echo -e "The location you specified doesn't exist.\\n" ; exit 0; else cd $dir ; echo -e "Please wait for the files to be counted.....\\n" ; echo ; fi

X=\`ls -l | wc -l\` Y=\`ls -l | grep ^d | awk '{print $9}'\` B=\`ls -l $Y | awk '{print $9}' | grep . | wc -l \` A=\`expr $X + $B\`

echo -e "There are a total of $A files inside the directory $dir...\\n"

C=\`ls -Rl | grep -v ./ | grep -v total | grep . | awk '{print $8}'\`

echo -e "Do you want to scan the directory for the file types?\\n" echo -e "Y/N\\n" ; read choice; if \[ $choice = Y \] ; then cd $dir ; file $C | awk '{print $1,"=======>>", $2}' > $HOME/Filetype.txt;echo -e "Output saved in file Filetype.txt.\\n" elif \[ $choice = N \] ; then echo -e "Thankyou $USER, Take care....\\n" else echo ; echo -e "Invalid choice buddy...\\n" ; echo -e "Exiting.....Bye..\\n" ;  fi \[/code\]
