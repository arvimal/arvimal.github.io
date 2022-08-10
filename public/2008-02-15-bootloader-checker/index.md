# Bootloader checker


A bash code snippet that helps to check if the installed bootloader is Grub or LILO.

\[code language="bash"\] #!/bin/bash

A=\`mount | awk '{print $1}' | grep -n /dev/ | grep "1:" | cut -f2 -d ":" | cut -c 1-8\` B=\`mount | awk '{print $1}' | grep -n /dev/ | grep "1:" | cut -f2 -d ":"\`

echo ; echo -e " / mounted on $B \\n"; dd if=$A bs=512 count=1 2>&1 | grep GRUB > /dev/null; if \[ $? = 0 \] ; then echo -e "The installed bootloader is GRUB.\\n" ; fi

dd if=$A bs=512 count=1 2>&1 | grep LILO > /dev/null; if \[ $? = 0 \] ; then echo -e "The installed bootloader is LILO.\\n" ; fi \[/code\]

