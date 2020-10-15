Nagios Installation Script
##########################
:date: 2008-02-14 10:26
:author: arvimal
:category: Programming
:tags: nagios installation
:slug: nagios-installation-script
:status: published

This is a bash script which automates the installation of Nagios. There are more things to do such as setup of service monitoring, but that's for another time.

| [code language="bash"]
| #!/bin/bash
| DOWNLOAD_LOCATION='/root/Downloads/'
| NAGIOS_URL='http://jaist.dl.sourceforge.net/sourceforge/nagios/nagios-2.9.tar.gz'
| APACHE_CONF='/etc/httpd/conf/httpd.conf'
| NAGIOS_PLUGIN='http://nchc.dl.sourceforge.net/sourceforge/nagiosplug/nagios-plugins-1.4.8.tar.gz'
| NAGIOSHOME='/usr/local/nagios'
| DATE=`date +%d-%b-%Y\`
| FILE='/root/Nagios.txt'

| #################################
| # [1]   Installing nagios       #
| #################################
| nagios_download () {
| clear

| if [ \`id -u\` -ne 0 ];
| then
| echo -e "You are executing the script as $USER\n"
| echo -e "You must be root to execute this script..\n";
| echo -e "Sorry...Exiting..\n";exit 111;
| else
| if [ ! -e /root/Nagios.txt ];
| then touch /root/Nagios.txt;
| else
| mv /root/Nagios.txt /root/Nagios-$DATE.txt;
| touch /root/Nagios.txt;
| fi

| echo -e "            [@@@@@@@@@@@@@@@@@@@@@@@@@ NAGIOS INSTALL SCRIPT @@@@@@@@@@@@@@@@@@@@@@@@@]\n";sleep 1s
| echo -e "                                           ...Welcome...\n"|tee -a $FILE;sleep 1s
| echo "[Starting the Nagios Installation Process :-]"|tee -a $FILE;
| echo "---------------------------------------------"|tee -a $FILE;echo;sleep 1s
| fi

| if [ ! -e $DOWNLOAD_LOCATION ];
| then
| echo "$DOWNLOAD_LOCATION does not exist, creating......."|tee -a $FILE;sleep 1s
| mkdir -pv $DOWNLOAD_LOCATION;echo
| fi

| echo "[Downloading the nagios tar-ball to $DOWNLOAD_LOCATION :-]"|tee -a $FILE;
| echo "--------------------------------------------------------"|tee -a $FILE;echo;sleep 1s

| cd $DOWNLOAD_LOCATION && wget --progress=dot $NAGIOS_URL;echo
| echo -e "Extracting the archive....\n"|tee -a $FILE;sleep 1s
| cd $DOWNLOAD_LOCATION && tar -zxf nagios*gz && mv nagios*gz Nagios-$DATE.tar.gz;echo
| }

| nagios_usercheck () {
| echo "[Checking the existence of user/group 'nagios' :-]"|tee -a $FILE;
| echo "--------------------------------------------------"|tee -a $FILE;

| grep -q nagios /etc/group > /dev/null
| if [ $? = 0 ];then
| echo "Group 'nagios' exist"|tee -a $FILE;
| else
| echo "Adding group 'nagios'"|tee -a $FILE;
| /usr/sbin/groupadd nagios
| fi

| grep -q nagios /etc/passwd > /dev/null
| if [ $? = 0 ];then
| echo "User 'nagios' exists"|tee -a $FILE;
| else
| echo "Adding user 'nagios'"|tee -a $FILE;
| /usr/sbin/useradd -d $NAGIOSHOME -g nagios -s /bin/false -m nagios
| fi;echo

| echo "[Checking the existence of user/group 'nagcmd' :-]"|tee -a $FILE;
| echo "--------------------------------------------------"|tee -a $FILE;

| grep -q nagcmd /etc/group;
| if [ $? = 0 ];then
| echo "Group 'nagcmd' exists"|tee -a $FILE;
| else
| echo "Adding group 'nagcmd'"|tee -a $FILE;
| /usr/sbin/groupadd nagcmd;
| fi

| grep -q nagcmd /etc/passwd;
| if [ $? = 0 ];then
| echo "User 'nagcmd' exists"|tee -a $FILE;
| else
| echo "Adding user 'nagcmd'"|tee -a $FILE;
| /usr/sbin/useradd -g nagcmd -s /bin/false -m nagcmd;
| fi;
| echo
| }

| nagios_previouscheck () {
| echo "[Checking for previous installations :-]"|tee -a $FILE
| echo "----------------------------------------"|tee -a $FILE;sleep 1s

| if [ -d /usr/local/nagios ];
| then
| echo "Installation directory '/usr/local/nagios/' already exist."|tee -a $FILE
| echo "Moving '/usr/local/nagios/' to '/usr/local/Nagios-$DATE.back'"|tee -a $FILE
| mv -v /usr/local/nagios /usr/local/Nagios-$DATE.back;echo
| echo "Creating the Installation Directory for Nagios [/usr/local/nagios/]"|tee -a $FILE
| mkdir -pv /usr/local/nagios;echo
| else
| echo "Nagios installation not found at the default location of $NAGIOSHOME";
| echo "Creating the Installation Directory for Nagios [/usr/local/nagios/]"|tee -a $FILE
| mkdir -pv /usr/local/nagios;echo
| fi
| }

| nagios_ownership () {
| echo "[Setting appropriate ownership on the installation directory]"|tee -a $FILE
| echo "-------------------------------------------------------------"
| chown -v nagios.nagios /usr/local/nagios;echo;sleep 1s

| echo "[Checking the Web-Server user/group :-]"|tee -a $FILE
| echo "---------------------------------------"|tee -a $FILE;sleep 1s

| echo "Web-Server User  : \`grep "^User" $APACHE_CONF|head -n1|awk '{print $2}'`"|tee -a $FILE
| echo "Web-Server Group : \`grep "^Group" $APACHE_CONF|head -n1|awk '{print $2}'`"|tee -a $FILE;echo;sleep 1s

| echo "[Adding the Web-Server/Nagios user to the 'nagcmd' group]"|tee -a $FILE;
| echo "---------------------------------------------------------"
| /usr/sbin/usermod -G nagcmd \`grep "^User" $APACHE_CONF|head -n1|awk '{print $2}'\` && \\
| echo "Added the user \`grep "^User" $APACHE_CONF|head -n1|awk '{print $2}'\` to the 'nagcmd' group."|tee -a $FILE
| sleep 1s
| /usr/sbin/usermod -G nagcmd nagios && echo -e "Added the user 'nagios' to the 'nagcmd' group.\n"|tee -a $FILE;sleep 1s
| echo
| }

| nagios_configure () {
| echo "[Starting the Nagios 'configure' script :-]"|tee -a $FILE;
| echo "-------------------------------------------"|tee -a $FILE;sleep 4s

| cd $DOWNLOAD_LOCATION/nagios\* && ./configure --with-command-group=nagcmd && make all && make install && make install-config && make install-init && make install-commandmode
| echo
| }

| #################################
| # [2] Installing Nagios Plugins #
| #################################

| nagios_plugins () {
| sleep 4s
| echo -e "           [@@@@@@@@@@@@@@@@@@@@@@@@@ NAGIOS PLUGIN SETUP @@@@@@@@@@@@@@@@@@@@@@@@@]\n"|tee -a $FILE;sleep 2s

| echo "[Downloading the 'nagios-plugins' tarball :-]"|tee -a $FILE;
| echo "---------------------------------------------";sleep 3s
| cd $DOWNLOAD_LOCATION && wget --progress=dot $NAGIOS_PLUGIN;echo
| echo "[Extracting the plugins archive :-]"|tee -a $FILE;
| echo "-----------------------------------";sleep 1s
| cd $DOWNLOAD_LOCATION && tar -zxf nagios-plugins*gz && mv nagios-plugins*gz Nagios-plugins-$DATE.tar.gz;echo
| echo "[Configuring and compiling nagios-plugins :-]"|tee -a $FILE;
| echo "---------------------------------------------"|tee -a $FILE;sleep 1s
| cd $DOWNLOAD_LOCATION && cd nagios-plugins\* && ./configure && make && make install && echo && echo -e "[Nagios Plugin Setup Finished.]\n"
| }
| echo;echo;sleep 3s

| #################################
| # [3]  Configuring Nagios       #
| #################################
| nagios_conf_files () {
| echo "[Creating the minimal configuration files :-]";
| echo "---------------------------------------------";sleep 2s
| cp -apv $NAGIOSHOME/etc/nagios.cfg-sample $NAGIOSHOME/etc/nagios.cfg
| cp -apv $NAGIOSHOME/etc/commands.cfg-sample $NAGIOSHOME/etc/commands.cfg
| cp -apv $NAGIOSHOME/etc/resource.cfg-sample $NAGIOSHOME/etc/resource.cfg
| cp -apv $NAGIOSHOME/etc/localhost.cfg-sample $NAGIOSHOME/etc/localhost.cfg
| cp -apv $NAGIOSHOME/etc/cgi.cfg-sample $NAGIOSHOME/etc/cgi.cfg;echo

| echo "[Setting administrative rights for 'nagiosadmin']"
| echo "-------------------------------------------------";sleep 2s;echo
| echo "" >> $NAGIOSHOME/etc/cgi.cfg
| echo -e "#Setting administrative rights for 'nagiosadmin'\n" >> $NAGIOSHOME/etc/cgi.cfg

| echo "authorized_for_system_information=nagiosadmin
| authorized_for_configuration_information=nagiosadmin
| authorized_for_system_commands=nagiosadmin
| authorized_for_all_services=nagiosadmin
| authorized_for_all_hosts=nagiosadmin
| authorized_for_all_service_commands=nagiosadmin
| authorized_for_all_host_commands=nagiosadmin" >> $NAGIOSHOME/etc/cgi.cfg

| echo "[Creating additional configuration files :-]";
| echo "--------------------------------------------";sleep 2s
| touch $NAGIOSHOME/etc/hosts.cfg;
| if [ $? -eq 0 ];then echo "Created $NAGIOSHOME/etc/hosts.cfg";else echo "Failed creating $NAGIOSHOME/etc/hosts.cfg";fi
| touch $NAGIOSHOME/etc/hostgroups.cfg;
| if [ $? -eq 0 ];then echo "Created $NAGIOSHOME/etc/hostgroups.cfg";else echo "Failed creating $NAGIOSHOME/etc/hostgroups.cfg";fi
| touch $NAGIOSHOME/etc/contacts.cfg;
| if [ $? -eq 0 ];then echo "Created $NAGIOSHOME/etc/contacts.cfg";else echo "Failed creating $NAGIOSHOME/etc/contacts.cfg";fi
| touch $NAGIOSHOME/etc/contactgroups.cfg;
| if [ $? -eq 0 ];then echo "Created $NAGIOSHOME/etc/contactgroups.cfg";else echo "Failed creating $NAGIOSHOME/etc/contactgroups.cfg";fi
| touch $NAGIOSHOME/etc/services.cfg;
| if [ $? -eq 0 ];then echo "Created $NAGIOSHOME/etc/services.cfg";else echo "Failed creating $NAGIOSHOME/etc/services.cfg";fi
| touch $NAGIOSHOME/etc/timeperiods.cfg;
| if [ $? -eq 0 ];then echo "Created $NAGIOSHOME/etc/timeperiods.cfg";else echo "Failed creating $NAGIOSHOME/etc/timeperiods.cfg";fi;
| echo

| echo "[Changing the ownership of newly created files :-]";
| echo "--------------------------------------------------";sleep 2s
| chown -Rv nagios.nagios $NAGIOSHOME/etc/\*
| echo

| echo "" >> $NAGIOSHOME/etc/nagios.cfg
| echo "[Setting config: file paths in $NAGIOSHOME/etc/nagios.cfg :-]";
| echo "------------------------------------------------------------------";echo;sleep 2s
| echo -e "#Setting configuration file paths.\n" >> $NAGIOSHOME/etc/nagios.cfg
| echo "cfg_file=/usr/local/nagios/etc/hosts.cfg
| cfg_file=/usr/local/nagios/etc/hostgroups.cfg
| cfg_file=/usr/local/nagios/etc/services.cfg
| cfg_file=/usr/local/nagios/etc/contacts.cfg
| cfg_file=/usr/local/nagios/etc/contactgroups.cfg
| cfg_file=/usr/local/nagios/etc/timeperiods.cfg" >> $NAGIOSHOME/etc/nagios.cfg

| echo
| echo "[Running the Nagios Syntax Check :-]";
| echo "------------------------------------";sleep 1s
| $NAGIOSHOME/bin/nagios -v $NAGIOSHOME/etc/nagios.cfg;echo
| }

| #################################
| # [4]   Setting Up Apache       #
| #################################

| nagios_apache () {
| echo "[Setting up Apache Web-Interface :-]"
| echo "------------------------------------"

grep -q "### Nagios Script Alias ###" $APACHE_CONF;

| if [ $? -eq 0 ];then
| echo -e "ScriptAlias for nagios already exists in $APACHE_CONF\n"
| /etc/init.d/httpd restart > /dev/null
| else

| echo "" >> $APACHE_CONF
| echo -e "### Nagios Script Alias ###\n" >> $APACHE_CONF;

echo -e "ScriptAlias /nagios/cgi-bin /usr/local/nagios/sbin \\n

| Options ExecCGI
| AllowOverride None
| Order allow,deny
| Allow from all
| AuthName \\"Nagios Access\"
| AuthType Basic
| AuthUserFile /usr/local/nagios/etc/htpasswd.users
| Require valid-user
|    \\n" >> $APACHE_CONF

echo -e "Alias /nagios /usr/local/nagios/share  \\n

| Options None
| AllowOverride None
| Order allow,deny
| Allow from all
| AuthName \\"Nagios Access\"
| AuthType Basic
| AuthUserFile /usr/local/nagios/etc/htpasswd.users
| Require valid-user
|    \\n" >> $APACHE_CONF

echo "Added the needed Alias configurations in $APACHE_CONF"

| echo -e "Restarting the Web-Server...please wait..\n"
| /etc/init.d/httpd restart;
| fi
| }

| nagios_htpasswd () {
| echo "[Creating the login credentials for the nagios URL :-]"
| echo "------------------------------------------------------";
| echo "Username    : nagiosadmin"
| htpasswd -c $NAGIOSHOME/etc/htpasswd.users nagiosadmin;echo
| echo -e "Login to the Nagios Interface is now restricted to user 'nagiosadmin'.\n"
| }

| nagios_download && nagios_usercheck && nagios_previouscheck && nagios_ownership && nagios_configure && nagios_plugins && nagios_conf_files && nagios_apache && nagios_htpasswd
| [/code]

 
