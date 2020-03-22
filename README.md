# Heappo

**Heappo** is a PyKD based extensions for WinDBG which aids Heap Exploitation by logging the followings:

## Features

### Tracing:
  * RtlAllocateHeap
  * RtlReAllocateHeap
  * RtlFreeHeap

### Paramenters
  * Custom allocation size
  * External log file

## Requirements 

* Python2.7 OR Python3.6 x64 
* PyKD x64/32
* WinDbg :)


## Installation and Setup 

From within WinDBG
     
     .load pykd
     !py heappy <heapsize> log=<on/off> 
     
     # Example
     !py heappo 0x40 log=on
   
