---
title: "CHKROOTKIT install script (with functions)"
date: 2008-02-14
categories:
  - "programming"
tags:
  - "functions"
---
<!--more-->
This is an extension or a rebuild of the previous chkrootkit install script, just used functions so its somewhat simplified.... ( Or is it ..? :) )

\[code language="bash"\]

#!/bin/bash

DOWNLOAD\_LOCATION='/root/Downloads' CHKROOTKIT\_WGET='ftp://ftp.pangeia.com.br/pub/seg/pac/chkrootkit.tar.gz' RESULT\_FILE='/root/Server-Test.txt'

clear;echo chkrootkit-install () {

while true; do echo -e "@@@@@@@@@@@@@@@@@@ CHK-ROOTKIT INSTALL/CHECK SCRIPT @@@@@@@@@@@@@@@@@@@@\\n" echo -e "Do you want to download and compile CHK-ROOTKIT \[yes/no\] ? : \\c" | tee -a $RESULT\_FILE; read answer; echo $answer >> $RESULT\_FILE;

case $answer in yes|YES) echo if \[ ! -e $DOWNLOAD\_LOCATION \]; then echo -e "$DOWNLOAD\_LOCATION does not exist, creating.......\\n";sleep 1s mkdir -p $DOWNLOAD\_LOCATION; fi rm -rf $DOWNLOAD\_LOCATION/chkrootkit\* > /dev/null; echo -e "Downloading CHK-ROOTKIT....\\n" | tee -a $RESULT\_FILE;sleep 1s cd $DOWNLOAD\_LOCATION && wget --progress=dot $CHKROOTKIT\_WGET; if \[ $? -eq 0 \] ; then echo -e "Download finished..\\n"; else echo -e "Sorry...Download Failed..!!!\\n";exit;fi;echo echo -e "Unpacking and compiling CHK-ROOTKIT..........\\n";sleep 2s cd $DOWNLOAD\_LOCATION && tar -xvf chkrootkit\*; mv $DOWNLOAD\_LOCATION/chkrootkit\*gz $DOWNLOAD\_LOCATION/1-chkrootkit.tar.gz;sleep 2s cd $DOWNLOAD\_LOCATION/chkrootki\* && make sense > /dev/null; if \[ $? -eq 0 \] ; then echo -e "CHK-ROOTKIT compiled successfully..\\n"| tee -a $RESULT\_FILE; break else echo -e "CHK-ROOTKIT compilation failed, Quiting....\\n" | tee -a $RESULT\_FILE; exit fi ;; no|NO) echo echo -e "Ok..As you wish....Aborting.\\n"|tee -a $RESULT\_FILE; exit ;; \*) echo echo -e "Please enter either 'yes' OR 'no'..: \\c" ;; esac done }

chkrootkit-run () { if \[ -d $DOWNLOAD\_LOCATION/chkrootki\* \]; then while true; do echo -e "Do you want to run CHK-ROOTKIT now \[yes/no\] ? : \\c" | tee -a $RESULT\_FILE; read reply echo $reply >> $RESULT\_FILE;

case $reply in yes|YES) echo echo -e "Starting CHK-ROOTKIT....\\n" | tee -a $RESULT\_FILE;sleep 2s;echo echo -e "----------------CHK-ROOTKIT SCAN RESULT-----------------\\n" $DOWNLOAD\_LOCATION/chkrootk\*/chkrootkit | tee -a $RESULT\_FILE;sleep 1s echo;echo -e "CHK-ROOTKIT check finished......\\n";echo exit ;; no|NO) echo echo -e "DON'T FORGET TO RUN CHK-ROOTKIT PERIODICALLY.\\n" exit ;; \*) echo echo -e "Please enter either 'yes' OR 'no'..: \\c" ;; esac done

else echo -e "Chkrootkit not found in $DOWNLOAD\_LOCATION, exiting..\\n" fi

}

chkrootkit-install && chkrootkit-run; echo -e "The result is saved in $RESULT\_FILE for reference.\\n" \[/code\]
