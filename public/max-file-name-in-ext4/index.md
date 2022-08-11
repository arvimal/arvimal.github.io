# Max file-name length in an EXT4 file system.

<!--more-->
_**A**_ recent discussion at work brought up the question "What can be the length of a file name in EXT4". Or in other words, what would be the maximum character length of the name for a file in EXT4?

[Wikipedia](https://en.wikipedia.org/wiki/Comparison_of_file_systems) states that it's _**255 Bytes**_, but how does that come to be? Is it 255 Bytes or 255 characters?

In the kernel source for the 2.6 kernel series (the question was for a RHEL6/EXT4 combination), in  [fs/ext4/ext4.h](https://access.redhat.com/labs/psb/versions/kernel-2.6.32-573.el6/fs/ext4/ext4.h), we'd be able to see the following:

\[code language="c"\]

#define EXT4\_NAME\_LEN 255

struct ext4\_dir\_entry { \_\_le32 inode; /\* Inode number \*/ \_\_le16 rec\_len; /\* Directory entry length \*/ \_\_le16 name\_len; /\* Name length \*/ char name\[EXT4\_NAME\_LEN\]; /\* File name \*/ };

/\* \* The new version of the directory entry. Since EXT4 structures are \* stored in intel byte order, and the name\_len field could never be \* bigger than 255 chars, it's safe to reclaim the extra byte for the \* file\_type field. \*/

struct ext4\_dir\_entry\_2 { \_\_le32 inode; /\* Inode number \*/ \_\_le16 rec\_len; /\* Directory entry length \*/ \_\_u8 name\_len; /\* Name length \*/ \_\_u8 file\_type; char name\[EXT4\_NAME\_LEN\]; /\* File name \*/ }; \[/code\] This shows that there are two versions of the directory entry structure, ie.. `ext4_dir_entry` and `ext4_dir_entry_2`

A directory entry structure carries the file/folder name and the corresponding inode number under every directory.

Both structs use an element named `name_len` to denote the length of the file/folder name.

If the EXT filesystem feature `filetype` is **not** set, the directory entry structure falls to the first method `ext4_dir_entry`, else it's the second, ie.. `ext4_dir_entry_2`.

By default, the file system feature `filetype` is set, hence the directory entry structure is `ext4_dir_entry_2` . As seen above, in this case, the `name_len` field is set to 8 bits.

`__u8` represents an unsigned 8-bit integer in C, and can store values from 0 to 255.

ie.. _**2^8 = 255 (0 t0 255 == 256)**_

`ext4_dir_entry` has a `name_len` of `__le16`, but it seems that the file-name length can only go to a max of 256.

### Observations:

1. The maximum name length is 255 characters on Linux machines.
2. The actual name length of a file/folder is stored in `name_len` in each directory entry, under its parent folder. So if the file name length is 5 characters, 5 would be the value set for `name_len` for that particular file. ie.. the actual length.
3. A character will consume a byte of storage, so the number of characters in a file name will map to the respective number bytes. If so, a file with a `name_len` of 5 will be using 5 bytes of memory to store the name.

Hence, `name_len` denotes the **number** of characters that a file can have. Since U8 is 8-bits, `name_len` can store a file name with upto 255 chars.

Now the actual memory being consumed for storing these characters **is not** denoted by `name_len`. Since the size of a character translates to a byte, the maximum size wrt memory that a file name can have is 255 Bytes.

### NOTE:

The initial dir entry structure `ext4_dir_entry` had `__le16` for `name_len`, it was later re-sized to `__u8` in `ext4_dir_entry_2` , by culling 8 bits from the existing 16 bits of `name_len`.

The remaining free space culled from `name_len` was assigned to store the file type, in `ext4_dir_entry_2`. It was named `file_type` with size `__u8`.

`file_type` helps to identity the file types such as regular files, sockets, character devices, block devices etc..

### References:

1. [RHEL6 kernel-2.6.32-573.el6 EXT4 header file (ext4.h)](https://access.redhat.com/labs/psb/versions/kernel-2.6.32-573.el6/fs/ext4/ext4.h)
2. [EXT4 Wiki - Disk layout](https://ext4.wiki.kernel.org/index.php/Ext4_Disk_Layout)
3. [http://unix.stackexchange.com/questions/32795/what-is-the-maximum-allowed-filename-and-folder-size-with-ecryptfs](http://unix.stackexchange.com/questions/32795/what-is-the-maximum-allowed-filename-and-folder-size-with-ecryptfs)

