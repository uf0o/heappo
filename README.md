# Heappo

**Heappo** 🦛 is a PyKD based extensions for WinDBG which aids Heap Exploitation by logging the followings:

## Features

Runs on both Py2/Py3 and x86/x64
Timestamps :)

### Tracing:
  * RtlAllocateHeap
  * RtlReAllocateHeap
  * RtlFreeHeap
  * VirtualAlloc

### Paramenters
  * Custom allocation size
  * External log file

### To do:
* ~~Add VirtualAlloc~~
* Group functions by same usr-ptr (and possibly same return pointer/caller)
* Log file in mona.py format 

## Requirements 
* Python2.7 OR Python3.6 x64 
* PyKD x64/32
* WinDbg :)


## Installation and Setup 
From within WinDBG
     
     .load pykd
     !py heappo.py <heap_alloc_size> log=<on/off> 
     
     # Example
     !py heappo.py 0x40 log=on
   
   
## Sample Outputs

```
0:001> !py c:\users\matteo\desktop\heappo.py null log=on
VirtualAlloc(0x0L , 0x2800000L , 0x2000L , 0x4L) = 0x7e0000 - From: 0x401034
VirtualAlloc(0x0L , 0xa00000L , 0x1000L , 0x4L) = 0x2fe0000 - From: 0x40104b
```

```
0:014> !py c:\users\matteo\desktop\heappo.py null log=on
RtlReAllocateHeap(0x3aa0000L , 0x0L , 0x3aa0a80L , 0x4L) = 0x3aa0a80 - From: 0x72a81e71
RtlReAllocateHeap(0x3aa0000L , 0x0L , 0x3aa0a90L , 0x4L) = 0x3aa0a90 - From: 0x72a81e71
RtlReAllocateHeap(0x3aa0000L , 0x0L , 0x3aa0a80L , 0x0L) = 0x3aa0a80 - From: 0x72a81e71
RtlReAllocateHeap(0x3aa0000L , 0x0L , 0x3aa0a90L , 0x0L) = 0x3aa0a90 - From: 0x72a81e71
RtlAllocateHeap(0x510000L , 0x0L , 0xf8L) = 0x5c6c30 - From: 0x6f8bc595
RtlAllocateHeap(0x510000L , 0x8L , 0x30L) = 0x449c348 - From: 0x6f853ee4
RtlAllocateHeap(0x510000L , 0x0L , 0xf8L) = 0x5c7430 - From: 0x6f8bc595
RtlAllocateHeap(0x510000L , 0x8L , 0x18L) = 0x44f20f8 - From: 0x6f855762
RtlFreeHeap(0x510000L , 0x0L , 0x44f20f8L) = 0x1 - From: 0x75fa14dd
RtlFreeHeap(0x510000L , 0x0L , 0x5c7430L) = 0x1 - From: 0x75fa14dd
RtlFreeHeap(0x510000L , 0x0L , 0x449c348L) = 0x1 - From: 0x75fa14dd
```
   
## Credits

Greatly inspired by Sam Brown [project](https://labs.f-secure.com/archive/heap-tracing-with-windbg-and-python)
