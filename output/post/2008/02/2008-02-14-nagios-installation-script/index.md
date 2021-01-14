---
title: "Nagios Installation Script"
date: "2008-02-14"
categories: 
  - "programming"
tags: 
  - "nagios-installation"
---

This is a bash script which automates the installation of Nagios. There are more things to do such as setup of service monitoring, but that's for another time.

\[code language="bash"\] #!/bin/bash DOWNLOAD\_LOCATION='/root/Downloads/' NAGIOS\_URL='http://jaist.dl.sourceforge.net/sourceforge/nagios/nagios-2.9.tar.gz' APACHE\_CONF='/etc/httpd/conf/httpd.conf' NAGIOS\_PLUGIN='http://nchc.dl.sourceforge.net/sourceforge/nagiosplug/nagios-plugins-1.4.8.tar.gz' NAGIOSHOME='/usr/local/nagios' DATE=\`date +%d-%b-%Y\` FILE='/root/Nagios.txt'

################################# # \[1\]   Installing nagios       # ################################# nagios\_download () { clear

if \[ \`id -u\` -ne 0 \]; then echo -e "You are executing the script as $USER\\n" echo -e "You must be root to execute this script..\\n"; echo -e "Sorry...Exiting..\\n";exit 111; else if \[ ! -e /root/Nagios.txt \]; then touch /root/Nagios.txt; else mv /root/Nagios.txt /root/Nagios-$DATE.txt; touch /root/Nagios.txt; fi

echo -e "            \[@@@@@@@@@@@@@@@@@@@@@@@@@ NAGIOS INSTALL SCRIPT @@@@@@@@@@@@@@@@@@@@@@@@@\]\\n";sleep 1s echo -e "                                           ...Welcome...\\n"|tee -a $FILE;sleep 1s echo "\[Starting the Nagios Installation Process :-\]"|tee -a $FILE; echo "---------------------------------------------"|tee -a $FILE;echo;sleep 1s fi

if \[ ! -e $DOWNLOAD\_LOCATION \]; then echo "$DOWNLOAD\_LOCATION does not exist, creating......."|tee -a $FILE;sleep 1s mkdir -pv $DOWNLOAD\_LOCATION;echo fi

echo "\[Downloading the nagios tar-ball to $DOWNLOAD\_LOCATION :-\]"|tee -a $FILE; echo "--------------------------------------------------------"|tee -a $FILE;echo;sleep 1s

cd $DOWNLOAD\_LOCATION && wget --progress=dot $NAGIOS\_URL;echo echo -e "Extracting the archive....\\n"|tee -a $FILE;sleep 1s cd $DOWNLOAD\_LOCATION && tar -zxf nagios\*gz && mv nagios\*gz Nagios-$DATE.tar.gz;echo }

nagios\_usercheck () { echo "\[Checking the existence of user/group 'nagios' :-\]"|tee -a $FILE; echo "--------------------------------------------------"|tee -a $FILE;

grep -q nagios /etc/group > /dev/null if \[ $? = 0 \];then echo "Group 'nagios' exist"|tee -a $FILE; else echo "Adding group 'nagios'"|tee -a $FILE; /usr/sbin/groupadd nagios fi

grep -q nagios /etc/passwd > /dev/null if \[ $? = 0 \];then echo "User 'nagios' exists"|tee -a $FILE; else echo "Adding user 'nagios'"|tee -a $FILE; /usr/sbin/useradd -d $NAGIOSHOME -g nagios -s /bin/false -m nagios fi;echo

echo "\[Checking the existence of user/group 'nagcmd' :-\]"|tee -a $FILE; echo "--------------------------------------------------"|tee -a $FILE;

grep -q nagcmd /etc/group; if \[ $? = 0 \];then echo "Group 'nagcmd' exists"|tee -a $FILE; else echo "Adding group 'nagcmd'"|tee -a $FILE; /usr/sbin/groupadd nagcmd; fi

grep -q nagcmd /etc/passwd; if \[ $? = 0 \];then echo "User 'nagcmd' exists"|tee -a $FILE; else echo "Adding user 'nagcmd'"|tee -a $FILE; /usr/sbin/useradd -g nagcmd -s /bin/false -m nagcmd; fi; echo }

nagios\_previouscheck () { echo "\[Checking for previous installations :-\]"|tee -a $FILE echo "----------------------------------------"|tee -a $FILE;sleep 1s

if \[ -d /usr/local/nagios \]; then echo "Installation directory '/usr/local/nagios/' already exist."|tee -a $FILE echo "Moving '/usr/local/nagios/' to '/usr/local/Nagios-$DATE.back'"|tee -a $FILE mv -v /usr/local/nagios /usr/local/Nagios-$DATE.back;echo echo "Creating the Installation Directory for Nagios \[/usr/local/nagios/\]"|tee -a $FILE mkdir -pv /usr/local/nagios;echo else echo "Nagios installation not found at the default location of $NAGIOSHOME"; echo "Creating the Installation Directory for Nagios \[/usr/local/nagios/\]"|tee -a $FILE mkdir -pv /usr/local/nagios;echo fi }

nagios\_ownership () { echo "\[Setting appropriate ownership on the installation directory\]"|tee -a $FILE echo "-------------------------------------------------------------" chown -v nagios.nagios /usr/local/nagios;echo;sleep 1s

echo "\[Checking the Web-Server user/group :-\]"|tee -a $FILE echo "---------------------------------------"|tee -a $FILE;sleep 1s

echo "Web-Server User  : \`grep "^User" $APACHE\_CONF|head -n1|awk '{print $2}'\`"|tee -a $FILE echo "Web-Server Group : \`grep "^Group" $APACHE\_CONF|head -n1|awk '{print $2}'\`"|tee -a $FILE;echo;sleep 1s

echo "\[Adding the Web-Server/Nagios user to the 'nagcmd' group\]"|tee -a $FILE; echo "---------------------------------------------------------" /usr/sbin/usermod -G nagcmd \`grep "^User" $APACHE\_CONF|head -n1|awk '{print $2}'\` && \\ echo "Added the user \`grep "^User" $APACHE\_CONF|head -n1|awk '{print $2}'\` to the 'nagcmd' group."|tee -a $FILE sleep 1s /usr/sbin/usermod -G nagcmd nagios && echo -e "Added the user 'nagios' to the 'nagcmd' group.\\n"|tee -a $FILE;sleep 1s echo }

nagios\_configure () { echo "\[Starting the Nagios 'configure' script :-\]"|tee -a $FILE; echo "-------------------------------------------"|tee -a $FILE;sleep 4s

cd $DOWNLOAD\_LOCATION/nagios\* && ./configure --with-command-group=nagcmd && make all && make install && make install-config && make install-init && make install-commandmode echo }

################################# # \[2\] Installing Nagios Plugins # #################################

nagios\_plugins () { sleep 4s echo -e "           \[@@@@@@@@@@@@@@@@@@@@@@@@@ NAGIOS PLUGIN SETUP @@@@@@@@@@@@@@@@@@@@@@@@@\]\\n"|tee -a $FILE;sleep 2s

echo "\[Downloading the 'nagios-plugins' tarball :-\]"|tee -a $FILE; echo "---------------------------------------------";sleep 3s cd $DOWNLOAD\_LOCATION && wget --progress=dot $NAGIOS\_PLUGIN;echo echo "\[Extracting the plugins archive :-\]"|tee -a $FILE; echo "-----------------------------------";sleep 1s cd $DOWNLOAD\_LOCATION && tar -zxf nagios-plugins\*gz && mv nagios-plugins\*gz Nagios-plugins-$DATE.tar.gz;echo echo "\[Configuring and compiling nagios-plugins :-\]"|tee -a $FILE; echo "---------------------------------------------"|tee -a $FILE;sleep 1s cd $DOWNLOAD\_LOCATION && cd nagios-plugins\* && ./configure && make && make install && echo && echo -e "\[Nagios Plugin Setup Finished.\]\\n" } echo;echo;sleep 3s

################################# # \[3\]  Configuring Nagios       # ################################# nagios\_conf\_files () { echo "\[Creating the minimal configuration files :-\]"; echo "---------------------------------------------";sleep 2s cp -apv $NAGIOSHOME/etc/nagios.cfg-sample $NAGIOSHOME/etc/nagios.cfg cp -apv $NAGIOSHOME/etc/commands.cfg-sample $NAGIOSHOME/etc/commands.cfg cp -apv $NAGIOSHOME/etc/resource.cfg-sample $NAGIOSHOME/etc/resource.cfg cp -apv $NAGIOSHOME/etc/localhost.cfg-sample $NAGIOSHOME/etc/localhost.cfg cp -apv $NAGIOSHOME/etc/cgi.cfg-sample $NAGIOSHOME/etc/cgi.cfg;echo

echo "\[Setting administrative rights for 'nagiosadmin'\]" echo "-------------------------------------------------";sleep 2s;echo echo "" >> $NAGIOSHOME/etc/cgi.cfg echo -e "#Setting administrative rights for 'nagiosadmin'\\n" >> $NAGIOSHOME/etc/cgi.cfg

echo "authorized\_for\_system\_information=nagiosadmin authorized\_for\_configuration\_information=nagiosadmin authorized\_for\_system\_commands=nagiosadmin authorized\_for\_all\_services=nagiosadmin authorized\_for\_all\_hosts=nagiosadmin authorized\_for\_all\_service\_commands=nagiosadmin authorized\_for\_all\_host\_commands=nagiosadmin" >> $NAGIOSHOME/etc/cgi.cfg

echo "\[Creating additional configuration files :-\]"; echo "--------------------------------------------";sleep 2s touch $NAGIOSHOME/etc/hosts.cfg; if \[ $? -eq 0 \];then echo "Created $NAGIOSHOME/etc/hosts.cfg";else echo "Failed creating $NAGIOSHOME/etc/hosts.cfg";fi touch $NAGIOSHOME/etc/hostgroups.cfg; if \[ $? -eq 0 \];then echo "Created $NAGIOSHOME/etc/hostgroups.cfg";else echo "Failed creating $NAGIOSHOME/etc/hostgroups.cfg";fi touch $NAGIOSHOME/etc/contacts.cfg; if \[ $? -eq 0 \];then echo "Created $NAGIOSHOME/etc/contacts.cfg";else echo "Failed creating $NAGIOSHOME/etc/contacts.cfg";fi touch $NAGIOSHOME/etc/contactgroups.cfg; if \[ $? -eq 0 \];then echo "Created $NAGIOSHOME/etc/contactgroups.cfg";else echo "Failed creating $NAGIOSHOME/etc/contactgroups.cfg";fi touch $NAGIOSHOME/etc/services.cfg; if \[ $? -eq 0 \];then echo "Created $NAGIOSHOME/etc/services.cfg";else echo "Failed creating $NAGIOSHOME/etc/services.cfg";fi touch $NAGIOSHOME/etc/timeperiods.cfg; if \[ $? -eq 0 \];then echo "Created $NAGIOSHOME/etc/timeperiods.cfg";else echo "Failed creating $NAGIOSHOME/etc/timeperiods.cfg";fi; echo

echo "\[Changing the ownership of newly created files :-\]"; echo "--------------------------------------------------";sleep 2s chown -Rv nagios.nagios $NAGIOSHOME/etc/\* echo

echo "" >> $NAGIOSHOME/etc/nagios.cfg echo "\[Setting config: file paths in $NAGIOSHOME/etc/nagios.cfg :-\]"; echo "------------------------------------------------------------------";echo;sleep 2s echo -e "#Setting configuration file paths.\\n" >> $NAGIOSHOME/etc/nagios.cfg echo "cfg\_file=/usr/local/nagios/etc/hosts.cfg cfg\_file=/usr/local/nagios/etc/hostgroups.cfg cfg\_file=/usr/local/nagios/etc/services.cfg cfg\_file=/usr/local/nagios/etc/contacts.cfg cfg\_file=/usr/local/nagios/etc/contactgroups.cfg cfg\_file=/usr/local/nagios/etc/timeperiods.cfg" >> $NAGIOSHOME/etc/nagios.cfg

echo echo "\[Running the Nagios Syntax Check :-\]"; echo "------------------------------------";sleep 1s $NAGIOSHOME/bin/nagios -v $NAGIOSHOME/etc/nagios.cfg;echo }

################################# # \[4\]   Setting Up Apache       # #################################

nagios\_apache () { echo "\[Setting up Apache Web-Interface :-\]" echo "------------------------------------"

grep -q "### Nagios Script Alias ###" $APACHE\_CONF;

if \[ $? -eq 0 \];then echo -e "ScriptAlias for nagios already exists in $APACHE\_CONF\\n" /etc/init.d/httpd restart > /dev/null else

echo "" >> $APACHE\_CONF echo -e "### Nagios Script Alias ###\\n" >> $APACHE\_CONF;

echo -e "ScriptAlias /nagios/cgi-bin /usr/local/nagios/sbin \\n

Options ExecCGI AllowOverride None Order allow,deny Allow from all AuthName \\"Nagios Access\\" AuthType Basic AuthUserFile /usr/local/nagios/etc/htpasswd.users Require valid-user    \\n" >> $APACHE\_CONF

echo -e "Alias /nagios /usr/local/nagios/share  \\n

Options None AllowOverride None Order allow,deny Allow from all AuthName \\"Nagios Access\\" AuthType Basic AuthUserFile /usr/local/nagios/etc/htpasswd.users Require valid-user    \\n" >> $APACHE\_CONF

echo "Added the needed Alias configurations in $APACHE\_CONF"

echo -e "Restarting the Web-Server...please wait..\\n" /etc/init.d/httpd restart; fi }

nagios\_htpasswd () { echo "\[Creating the login credentials for the nagios URL :-\]" echo "------------------------------------------------------"; echo "Username    : nagiosadmin" htpasswd -c $NAGIOSHOME/etc/htpasswd.users nagiosadmin;echo echo -e "Login to the Nagios Interface is now restricted to user 'nagiosadmin'.\\n" }

nagios\_download && nagios\_usercheck && nagios\_previouscheck && nagios\_ownership && nagios\_configure && nagios\_plugins && nagios\_conf\_files && nagios\_apache && nagios\_htpasswd \[/code\]
