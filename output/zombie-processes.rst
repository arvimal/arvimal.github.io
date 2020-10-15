Zombie processes
################
:date: 2008-01-01 17:56
:author: arvimal
:category: Techno
:tags: runaway process, zombie
:slug: zombie-processes
:status: published

**Why can't I kill a process with the signal 9?**

A process can be sleeping in kernel code. Usually that's because of faulty hardware or a badly written driver- or maybe a little of both. A device that isn't set to the interrupt the driver thinks it is can cause this, for example- the driver is waiting for something its never going to get. The process doesn't ignore your signal- it just never gets it.

A zombie process doesn't react to signals because it's not really a process at all- it's just what's left over after it died. What's supposed to happen is that its parent process was to issue a "wait()" to collect the information about its exit. If the parent doesn't (programming error or just bad programming), you get a zombie. The zombie will go away if its parent dies- it will be "adopted" by init which will do the wait()- so if you see one hanging about, check its parent; if it is init, it will be gone soon, if not the only recourse is to kill the parent..which you may or may not want to do.

Finally, a process that is being traced (by a debugger, for example) won't react to the KILL either then you do a ps, processes that have a status of Z are called "zombies". When people see a zombie process, the first thing they try to do is to kill the zombie, using kill or (horrors!) kill -9. This won't work, however: you can't kill a zombie, it's already dead.

When a process has already terminated ("died") by receiving a signal to do so, it can stick around for a bit to finish up a few last tasks. These include closing open files and shutting down any allocated resources (memory, swap space, that sort of thing). These "housekeeping" tasks are supposed to happen very quickly. Once they're completed, the final thing that a process has to do before dying is to report its exit status to its parent. This is generally where things go wrong.

Each process is assigned a unique Process ID (PID). Each process also has an associated parent process ID (PPID), which identifies the process that spawned it (or PPID of 1, meaning that the process has been inherited bythe init process, if the parent has already terminated). While the parent is still running, it can remember the PID's of all the children it has spawned. These PID's can not be re-used by other (new) processes until the parent knows that the child process is done.

When a child terminates and has completed its housekeeping tasks, it sends a one-byte status code to its parent. If this status code never gets sent, the PID is kept alive (in "zombie" status) in order to reserve its PID ... the parent is waiting for the status code, and until it gets it, it doesn't want any new processes to try and reuse that PID number for themselves.

To get rid of a zombie, you can try killing its parent, which will temporarily orphan the zombie. The init process will inherent the zombie, and this might allow the process to finish terminating since the init process is always in a wait() state (ready to receive exit status reports of children).

Generally, though, zombies clean themselves up. Whatever the process was waiting for eventually occurs and the process can report its exit status to its parent and all is well.

If a zombie is already owned by init, though, and it's still sticking around (like zombies are wont to do), then the process is almost certainly stuck in a device driver close routine, and will likely remain that way forever. You can reboot to clear out the zombies, but fixing the device driver is the only permanent solution. Killing the parent (init in this case) is highly unrecommended, since init is an extremely important process to keeping your system running..
