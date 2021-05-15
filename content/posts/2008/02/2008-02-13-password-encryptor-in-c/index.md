---
title: "Password Encryptor in C"
date: 2008-02-13
categories:
  - "programming"
tags:
  - "password-encrypt"
---

Some time back, I had to implement a password encryption section in one of my bash programs. It seemed easy to use a C snippet rather than doing it in bash. This was something I got after searching a while.

\[code language="C"\]

#include stdlib.h #include unistd.h #include stdio.h #include crack.h #define DICTIONARY /usr/lib/cracklib\_dict

int main(int argc, char \*argv\[\]) {

char \*password; char \*problem;

int status = 0; printf(\\nEnter an empty password or Ctrl-D to quit.\\n); while ((password = getpass(\\nPassword: )) != NULL \*password ) { if ((problem = FascistCheck(password, DICTIONARY)) != NULL) { printf(Bad password: %s.\\n, problem); status = 1; } else { printf(Good password!\\n); } } exit(status); } \[/code\]

Compile the code using the GNU C compiler.

> \# gcc filename.c -lcrack -o cracktest'
