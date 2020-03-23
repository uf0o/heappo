# Heappo

**Heappo** 🦛 is a PyKD based extensions for WinDBG which aids Heap Exploitation by logging the followings:

## Features

Runs on both Py2/Py3 and x86/x64

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
     !py heappo.py <heapsize> log=<on/off> 
     
     # Example
     !py heappo.py 0x40 log=on
   
   
## Credits

Greatly inspired by Sam Brown [project](https://labs.f-secure.com/archive/heap-tracing-with-windbg-and-python)
