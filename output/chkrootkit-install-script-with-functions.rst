CHKROOTKIT install script (with functions)
##########################################
:date: 2008-02-14 10:21
:author: arvimal
:category: Programming
:tags: functions
:slug: chkrootkit-install-script-with-functions
:status: published

This is an extension or a rebuild of the previous chkrootkit install script, just used functions so its somewhat simplified.... ( Or is it ..? :) )

[code language="bash"]

#!/bin/bash

| DOWNLOAD_LOCATION='/root/Downloads'
| CHKROOTKIT_WGET='ftp://ftp.pangeia.com.br/pub/seg/pac/chkrootkit.tar.gz'
| RESULT_FILE='/root/Server-Test.txt'

| clear;echo
| chkrootkit-install () {

| while true; do
| echo -e "@@@@@@@@@@@@@@@@@@ CHK-ROOTKIT INSTALL/CHECK SCRIPT @@@@@@@@@@@@@@@@@@@@\n"
| echo -e "Do you want to download and compile CHK-ROOTKIT [yes/no] ? : \\c" \| tee -a $RESULT_FILE;
| read answer;
| echo $answer >> $RESULT_FILE;

| case $answer in
| yes|YES)
| echo
| if [ ! -e $DOWNLOAD_LOCATION ]; then
| echo -e "$DOWNLOAD_LOCATION does not exist, creating.......\n";sleep 1s
| mkdir -p $DOWNLOAD_LOCATION;
| fi
| rm -rf $DOWNLOAD_LOCATION/chkrootkit\* > /dev/null;
| echo -e "Downloading CHK-ROOTKIT....\n" \| tee -a $RESULT_FILE;sleep 1s
| cd $DOWNLOAD_LOCATION && wget --progress=dot $CHKROOTKIT_WGET;
| if [ $? -eq 0 ] ; then echo -e "Download finished..\n";
| else echo -e "Sorry...Download Failed..!!!\n";exit;fi;echo
| echo -e "Unpacking and compiling CHK-ROOTKIT..........\n";sleep 2s
| cd $DOWNLOAD_LOCATION && tar -xvf chkrootkit*;
| mv $DOWNLOAD_LOCATION/chkrootkit*gz $DOWNLOAD_LOCATION/1-chkrootkit.tar.gz;sleep 2s
| cd $DOWNLOAD_LOCATION/chkrootki\* && make sense > /dev/null;
| if [ $? -eq 0 ] ; then echo -e "CHK-ROOTKIT compiled successfully..\n"\| tee -a $RESULT_FILE;
| break
| else echo -e "CHK-ROOTKIT compilation failed, Quiting....\n" \| tee -a $RESULT_FILE;
| exit
| fi
| ;;
| no|NO)
| echo
| echo -e "Ok..As you wish....Aborting.\n"|tee -a $RESULT_FILE;
| exit
| ;;
| \*)
| echo
| echo -e "Please enter either 'yes' OR 'no'..: \\c"
| ;;
| esac
| done
| }

| chkrootkit-run () {
| if [ -d $DOWNLOAD_LOCATION/chkrootki\* ]; then
| while true; do
| echo -e "Do you want to run CHK-ROOTKIT now [yes/no] ? : \\c" \| tee -a $RESULT_FILE;
| read reply
| echo $reply >> $RESULT_FILE;

| case $reply in
| yes|YES)
| echo
| echo -e "Starting CHK-ROOTKIT....\n" \| tee -a $RESULT_FILE;sleep 2s;echo
| echo -e "----------------CHK-ROOTKIT SCAN RESULT-----------------\n"
| $DOWNLOAD_LOCATION/chkrootk*/chkrootkit \| tee -a $RESULT_FILE;sleep 1s
| echo;echo -e "CHK-ROOTKIT check finished......\n";echo
| exit
| ;;
| no|NO)
| echo
| echo -e "DON'T FORGET TO RUN CHK-ROOTKIT PERIODICALLY.\n"
| exit
| ;;
| \*)
| echo
| echo -e "Please enter either 'yes' OR 'no'..: \\c"
| ;;
| esac
| done

| else echo -e "Chkrootkit not found in $DOWNLOAD_LOCATION, exiting..\n"
| fi

}

| chkrootkit-install && chkrootkit-run;
| echo -e "The result is saved in $RESULT_FILE for reference.\n"
| [/code]

 
