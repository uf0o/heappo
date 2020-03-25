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
2020-03-25 09:23:48.954000, VirtualAlloc(0x0L , 0x2800000L , 0x2000L , 0x4L) = 0x510000 - From: 0x401034
2020-03-25 09:24:52.166000, VirtualAlloc(0x0L , 0xa00000L , 0x1000L , 0x4L) = 0x2d10000 - From: 0x40104b
```

```
0:014> !py c:\users\matteo\desktop\heappo.py 0x40 log=on
2020-03-25 09:26:11.463000, RtlAllocateHeap(0x5c0000L , 0x0L , 0x40L) = 0x6435c8 - From: 0x7124b36e
2020-03-25 09:26:14.224000, RtlAllocateHeap(0x5c0000L , 0x0L , 0x40L) = 0x6435c8 - From: 0x7124b36e
2020-03-25 09:26:17.048000, RtlAllocateHeap(0x5c0000L , 0x0L , 0x40L) = 0x6435c8 - From: 0x7124b36e
2020-03-25 09:26:17.048000, RtlAllocateHeap(0x5c0000L , 0x0L , 0x40L) = 0x6435c8 - From: 0x7124b36e
2020-03-25 09:26:27.204000, RtlAllocateHeap(0x5c0000L , 0x0L , 0x40L) = 0x642a40 - From: 0x761c0636
```
   
## Credits

Greatly inspired by Sam Brown [project](https://labs.f-secure.com/archive/heap-tracing-with-windbg-and-python)
