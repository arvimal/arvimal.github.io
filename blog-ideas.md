# Blog Ideas

100 post ideas drawn from the SRE Notes wiki. Mark `[x]` when published.
One post per week = ~2 years of content.

Posts marked `[x]` are published. Posts marked `[-]` are skipped (topic already covered by an older post).

---

## Python Internals

- [x] The /proc Filesystem: What It Actually Is and How It Works *(2026-05-01)*
- [ ] Why `257 is 257` returns False: CPython's small integer cache
- [ ] String interning: how Python makes attribute lookups O(1)
- [ ] UnboundLocalError before the assignment: how Python decides locals at compile time
- [ ] The GIL: what it actually protects, what it doesn't, and what free-threaded Python changes
- [ ] Generators: lazy evaluation and the `__next__` protocol under the hood
- [ ] Context managers: what `__enter__` and `__exit__` actually do
- [ ] The descriptor protocol: how `obj.method` resolves in CPython
- [ ] `__slots__`: trading `__dict__` flexibility for memory
- [ ] Reading CPython assembly with `dis`: what bytecode tells you
- [ ] Closures and `nonlocal`: the counter pattern and why it works
- [ ] Weak references: breaking reference cycles without waiting for the GC
- [ ] `sys.getrefcount` and how reference counting drives CPython's memory model

---

## Linux Internals

- [ ] ELF binaries: what's inside your executable beyond the code
- [ ] PLT/GOT: how dynamic linking works — and what LD_PRELOAD exploits
- [ ] The Linux boot sequence: BIOS/UEFI to login prompt, step by step
- [ ] fork() and exec(): how every process is born
- [ ] What happens when you type a command in bash
- [ ] Why D-state processes can't be killed (and what to do about them)
- [ ] Linux namespaces: the six primitives that make containers possible
- [ ] cgroups v2: resource control from first principles
- [ ] File descriptor inheritance across fork and exec
- [ ] Shell I/O redirection: why the order of `2>&1` matters
- [ ] strace: what every system call tells you about a misbehaving process
- [ ] eBPF: the programmable kernel — how it works and why it's replacing half of Linux tooling

---

## Networking

- [ ] TCP three-way handshake: every field, every state
- [ ] TIME_WAIT: why it exists and why disabling it is dangerous
- [ ] TCP slow start: why your first request is always the slowest
- [ ] How DNS resolution actually works: root servers, recursion, and caching
- [ ] ndots:5 in Kubernetes: the hidden DNS query amplification
- [ ] How iptables works: tables, chains, and the Netfilter packet walk
- [ ] NAT and connection tracking: how your response packets find their way home
- [ ] mTLS: more than just TLS both ways
- [ ] HTTP/2 multiplexing: why it helps and when head-of-line blocking returns
- [ ] QUIC: why building HTTP/3 on UDP was the right call
- [ ] BGP in plain terms: how the internet routes packets between autonomous systems
- [ ] Anycast: the same IP address in many places simultaneously
- [ ] What traceroute actually measures (and what it misses)

---

## Kubernetes

- [ ] How a Pod gets scheduled: Filter, Score, Bind
- [ ] kube-proxy and how Services actually work under the hood
- [ ] etcd: why Kubernetes needs a consensus database
- [ ] The PLEG: what kubelet does all day
- [ ] Admission controllers: the pipeline every API call walks
- [ ] CrashLoopBackOff: the exponential backoff sequence explained
- [ ] Pod eviction: QoS classes and who gets killed first
- [ ] The HPA formula: how autoscaling decisions are actually made
- [ ] PodDisruptionBudgets: preventing self-inflicted outages during node drains
- [ ] How Kubernetes persistent volumes attach and mount to a pod
- [ ] Network policies: AND vs OR selector semantics and why it matters
- [ ] ConfigMaps as env vars vs volume mounts: why one updates live and one doesn't
- [ ] EndpointSlices: why Kubernetes replaced Endpoints
- [ ] Kubernetes RBAC: why wildcard permissions are a security hole
- [ ] The Kubernetes informer pattern: how controllers watch without polling

---

## Observability

- [ ] Prometheus data model: why cardinality kills your metrics store
- [ ] Histogram vs Summary: which to use and the key tradeoff
- [ ] PromQL `rate()` vs `irate()`: when each gives the wrong answer
- [ ] Designing alerts that don't cry wolf: symptom vs cause
- [ ] The four golden signals: choosing the right metrics for any service
- [ ] What distributed tracing actually is and why logs and metrics aren't enough
- [ ] Loki label design: why high-cardinality labels break log search
- [ ] The Prometheus WAL: how metrics survive a crash
- [ ] Multi-window burn rate alerting: the SRE Book algorithm explained

---

## Storage and Filesystems

- [ ] What happens when you delete a file in Linux
- [ ] Why `df` and `du` disagree (and when each is right)
- [ ] How LVM works: physical extents, volume groups, and logical volumes
- [ ] How ext4 and XFS handle a full filesystem differently
- [ ] NFS stale file handles: what causes them and how to recover
- [ ] CRUSH: how Ceph places data without a central lookup table
- [ ] RAID 5 is dead: write hole, URE probability math, and when to use RAID 6
- [ ] SSD write amplification: why your drive wears faster than the spec suggests
- [ ] Copy-on-write: how LVM snapshots and Btrfs subvolumes share data
- [ ] XFS delayed logging: why the CIL makes XFS fast under metadata pressure

---

## SRE Concepts

- [ ] SLI, SLO, SLA: the three levels and how to operationalize them
- [ ] Error budgets: from concept to weekly team ritual
- [ ] Toil: what counts, what doesn't, and the 50% rule
- [ ] Blameless postmortems: avoiding the five-why trap
- [ ] Canary releases: gating a deployment on Prometheus metrics
- [ ] Feature flags: lifecycle, cleanup, and what happens when you skip it
- [ ] Capacity planning with queuing theory: the M/M/1 model in practice
- [ ] Tail latency: why p99 matters more than average, and fan-out amplification
- [ ] The thundering herd problem: stampeding retries and the role of jitter
- [ ] On-call health: alert volume targets and sustainable rotation design

---

## Security

- [ ] Linux capabilities: dropping root without losing what you need
- [ ] seccomp: filtering system calls in containers
- [ ] SELinux contexts in five minutes: types, labels, and `audit2allow`
- [ ] How umask works: the subtraction model and the permission math
- [ ] SUID binaries: how privilege escalation works at the kernel level
- [ ] mTLS certificate lifecycle: rotation, revocation, and SPIFFE identity
- [ ] Supply chain security: signing container images with Sigstore and cosign

---

## Distributed Systems

- [ ] Consistent hashing: why it solves cache rebalancing without a full reshuffle
- [ ] CAP theorem: what it actually says, and what the P really means
- [ ] Raft consensus: leader election without a single point of failure
- [ ] Two-phase commit: why it blocks and what Saga fixes
- [ ] Gossip protocols: how distributed systems detect failures (SWIM)
- [ ] Event sourcing: the append-only log as a source of truth
- [ ] Distributed rate limiting: why per-replica counters give the wrong answer

---

## Performance and Low-Level

- [ ] CPU cache lines and false sharing: the invisible contention
- [ ] NUMA: why memory location matters on multi-socket servers
- [ ] The Linux OOM killer: how it scores processes and who it kills
- [ ] Page cache: why Linux uses all your RAM (and why that's correct behaviour)
