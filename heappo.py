# .load pykd
# !py c:\users\matteo\desktop\heappo.py 0x40 log=on

# to do:
# Group functions by same usr-ptr (and same return pointer?)
# Log file in mona format (need to check the specs)

import pykd
from os.path import expanduser

home = expanduser("~")
return_reg = "rax"
stack_pointer = "rsp"
arch_bits = 64
log = None

# we need to remove the tick char in case we deal with x64 addr
def format64(address):
    address64 = address.replace('`','')
    return address64

def get_address(localAddr):
    res = pykd.dbgCommand("x " + localAddr)
    result_count = res.count("\n")
    if result_count == 0:
        print(localAddr + " not found.")
        return None
    if result_count > 1:
        print("[-] Warning, more than one result for", localAddr)    
    return res.split()[0]

#RtlAllocateHeap(
# IN PVOID                HeapHandle,
# IN ULONG                Flags,
# IN ULONG                Size );
class handle_allocate_heap(pykd.eventHandler):
    def __init__(self):
        addr = format64(get_address("ntdll!RtlAllocateHeap"))
        if addr == None:
            return
        self.bp_init = pykd.setBp(int(addr, 16), self.enter_call_back)
        
    def enter_call_back(self):
        self.condition = False
        current_alloc_size = (hex(pykd.ptrMWord(pykd.reg("esp") + 0xC))).replace('L','')        
        if (current_alloc_size == alloc_size) or "null" in alloc_size: 
            self.condition = True
            self.out = "RtlAllocateHeap(" 
            if arch_bits == 32:
                esp = pykd.reg("esp")
                self.out += hex(pykd.ptrPtr(esp + 4)) + " , "
                self.out += hex(pykd.ptrMWord(esp + 0x8)) + " , "
                self.out += hex(pykd.ptrMWord(esp + 0xC)) + ") = "
            else:
                self.out += hex(pykd.reg("rcx")) + " , "
                self.out += hex(pykd.reg("rdx")) + " , " 
                self.out += hex(pykd.reg("r8"))  +  ") = "
            if self.condition:
                disas = pykd.dbgCommand("uf ntdll!RtlAllocateHeap").split('\n')
                for i in disas:
                    if 'ret' in i:
                        self.ret_addr = format64(i.split()[0])
                        break
                self.bp_end = pykd.setBp(int(self.ret_addr, 16), self.return_call_back)
        return False
    
    def return_call_back(self):
        if self.condition:
            esp = pykd.reg(stack_pointer)
            self.out += hex(pykd.reg(return_reg))
            self.out += " - From: " + (hex(pykd.ptrPtr(esp))).replace('L','') 
            print(self.out) 
            if logging:
                log.write(self.out + "\n")
            return False
         
#RtlFreeHeap(
#IN PVOID                HeapHandle,
#IN ULONG                Flags OPTIONAL,
#IN PVOID                MemoryPointer );
class handle_free_heap(pykd.eventHandler):
    def __init__(self):
        addr = format64(get_address("ntdll!RtlFreeHeap"))
        if addr == None:
            return
        self.bp_init = pykd.setBp(int(addr, 16), self.enter_call_back)
        self.bp_end = None
        
    def enter_call_back(self):
        self.condition = False
        current_free_size = (hex(pykd.ptrMWord(pykd.reg("esp") + 0xC))).replace('L','')
        # logging everything except Free[0] 
        if (current_free_size != "0x0"):
            self.condition = True
            self.out = "RtlFreeHeap("
            if arch_bits == 32:
                esp = pykd.reg(stack_pointer)
                self.out += hex(pykd.ptrPtr(esp + 4)) + " , "
                self.out += hex(pykd.ptrMWord(esp + 0x8)) + " , "
                self.out += hex(pykd.ptrPtr(esp + 0xC)) + ") = "
            else:
                self.out += hex(pykd.reg("rcx")) + " , "
                self.out += hex(pykd.reg("rdx")) + " , "
                self.out += hex(pykd.reg("r8")) + ") = "
            if self.bp_end == None:
                disas = pykd.dbgCommand("uf ntdll!RtlFreeHeap").split('\n')
                for i in disas:
                    if 'ret' in i:
                        self.ret_addr = format64(i.split()[0])
                        break
                self.bp_end = pykd.setBp(int(self.ret_addr, 16), self.return_call_back)
        return False
        
    def return_call_back(self):
        #returns a BOOLEAN which is a byte under the hood
        if self.condition:
            esp = pykd.reg(stack_pointer)
            ret_val = hex(pykd.reg("al"))
            self.out += ret_val
            self.out += " - From: " + (hex(pykd.ptrPtr(esp))).replace('L','')  
            print(self.out)
            if logging:
                log.write(self.out + "\n")
            return False
          
#RtlReAllocateHeap(
#IN PVOID                HeapHandle,
#IN ULONG                Flags,
# IN PVOID                MemoryPointer,
# IN ULONG                Size );
        
class handle_realloc_heap(pykd.eventHandler):
    def __init__(self):
        addr = format64(get_address("ntdll!RtlReAllocateHeap"))
        if addr == None:
            return
        self.bp_init = pykd.setBp(int(addr, 16), self.enter_call_back)
        self.bp_end = None
        
    def enter_call_back(self):
        self.condition = False
        current_alloc_size = (hex(pykd.ptrMWord(pykd.reg("esp") + 0x10))).replace('L','')        
        if (current_alloc_size == alloc_size) or "null" in alloc_size: 
            self.condition = True
            self.out = "RtlReAllocateHeap("
            if arch_bits == 32:
                esp = pykd.reg(stack_pointer)
                self.out += hex(pykd.ptrPtr(esp + 4)) + " , "
                self.out += hex(pykd.ptrMWord(esp + 0x8)) + " , "
                self.out += hex(pykd.ptrPtr(esp + 0xC)) + " , " 
                self.out += hex(pykd.ptrMWord(esp + 0x10)) + ") = "
            else:
                self.out += hex(pykd.reg("rcx")) + " , "
                self.out += hex(pykd.reg("rdx")) + " , " 
                self.out += hex(pykd.reg("r8")) + " , " 
                self.out += hex(pykd.reg("r9")) + ") = "
            if self.bp_end == None:
                disas = pykd.dbgCommand("uf ntdll!RtlReAllocateHeap").split('\n')
                for i in disas:
                    if 'ret' in i:
                        self.ret_addr = format64(i.split()[0])
                        break
                self.bp_end = pykd.setBp(int(self.ret_addr, 16), self.return_call_back)
            return False
            
    def return_call_back(self):
        if self.condition:
            esp = pykd.reg(stack_pointer)
            self.out += hex(pykd.reg(return_reg))
            self.out += " - From: " + (hex(pykd.ptrPtr(esp))).replace('L','')
            print(self.out)
            if logging:
                log.write(self.out + "\n")
            return False

#VirtualAlloc(
#    LPVOID lpAddress,
#    SIZE_T dwSize,
#    DWORD flAllocationType,
#    DWORD flProtect
#    );
        
class handle_virtual_alloc(pykd.eventHandler):
    def __init__(self):
        addr = format64(get_address("kernel32!VirtualAlloc"))
        if addr == None:
            return
        self.bp_init = pykd.setBp(int(addr, 16), self.enter_call_back)
        self.bp_end = None
        
    def enter_call_back(self):
        self.out = "VirtualAlloc("
        if arch_bits == 32:
            esp = pykd.reg(stack_pointer)
            self.out += hex(pykd.ptrPtr(esp + 4)) + " , "
            self.out += hex(pykd.ptrMWord(esp + 0x8)) + " , "
            self.out += hex(pykd.ptrMWord(esp + 0xC)) + " , " 
            self.out += hex(pykd.ptrMWord(esp + 0x10)) + ") = "
        else:
            self.out += hex(pykd.reg("rcx")) + " , "
            self.out += hex(pykd.reg("rdx")) + " , " 
            self.out += hex(pykd.reg("r8")) + " , " 
            self.out += hex(pykd.reg("r9")) + ") = "
        if self.bp_end == None:
            disas = pykd.dbgCommand("uf kernelbase!VirtualAlloc").split('\n')
            for i in disas:
                if 'ret' in i:
                    self.ret_addr = format64(i.split()[0])
                    break
            self.bp_end = pykd.setBp(int(self.ret_addr, 16), self.return_call_back)
        return False
            
    def return_call_back(self):
        esp = pykd.reg(stack_pointer)
        self.out += hex(pykd.reg(return_reg))
        self.out += " - From: " + (hex(pykd.ptrPtr(esp))).replace('L','')
        print(self.out)
        if logging:
            log.write(self.out + "\n")
        return False

def usage():
    print("(*) # from withing WinDBG #")
    print("(*) .load pykd")
    print("(*) !py heappo <heapsize/\"null\"> log=<on/off> \n\n")
    print("(*) Example:\n")
    print("(*) !py heappo 0x40 log=on")

if len(sys.argv) < 3:
    usage()
    sys.exit()

log = open(home + "\log.log","w+") 
logging = False
alloc_size = sys.argv[1]
log_var    = sys.argv[2]

if "on" in log_var:
    logging = True
       
try:
    pykd.reg("rax")
except:
    arch_bits = 32
    return_reg = "eax"
    stack_pointer = "esp"

handle_allocate_heap()
handle_free_heap()
handle_realloc_heap()
handle_virtual_alloc()
pykd.go()
    
