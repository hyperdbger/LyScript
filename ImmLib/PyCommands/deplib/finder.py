"""
Two main functions are defined here: dothesearch and dothesearchHash.

Hash searching is very fast and it provides EXACT results. You model what you need by changing the dep.sea.regs state machine registers.

The state machine provides a set of registers, flags and memory variables that you can use to interact between them almost as natural python variables (but remember they are SMT 32bits variables).

So, if you need a stack pivot for EAX you could try something like:
dep.sea.regs["ESP"]=dep.sea.regs["EAX"]                    #Emulate something like MOV ESP,EAX or the important half in XCHG EAX,ESP
dep.sea.EIP = dep.sea.readMemory(dep.sea.regs["ESP"], 4)   #Emulate a RETN
dep.sea.regs["ESP"]+=4                                     #This would be for a clean RETN, other possibilities are +8 = RETN 4, etc etc. Remember that this type of search is EXACT, so it would find what you search for.

If you need to assign a constant to a register, use this:
dep.sea.regs["EBX"]=dep.sea.solver.constExpr(0x12345678)

Results are logged in the ID Log window.

The other search method is heuristical and works by providing hints of what you need from the gadget.
This hints are modeled by telling DEPLIB what registers modify a given register.
ex: in ADD EAX, EBX
EAX is being modified by EBX
MOV EAX, 12345678
EAX is modified by a CONST
and you can mix registers providing a tuple instead of a string:
ADD EAX, EBX
SUB EAX, EDX
EAX is modified by EBX AND EDX. regs["EAX"]=("EBX","EDX")

Also you can model that some register is modified by memory indexed by some register:
OR EAX, [EDX]
EAX is modified by memory pointed by EDX. regs["EAX"]=(, "EDX")   [the comma is on purpose, is the second element that you must use to model memory indexes]

besides registers and CONST you can use the special word FLAGS, meaning the the value of some register is tainted by some flag:
SBB EAX, EDX
regs["EAX"]=("EDX","FLAGS")

"""

from deplib20 import DeplibFinder
from immlib import *

def mymain():
    dep=DeplibFinder({"stackpage":4, "dbname":"gadgets.sq3", "modules":"msvcr71.dll"})
    
    ##### DEFINE YOUR SEARCHING CONSTRAINS HERE #######
    #for x in xrange(790,890):
    #    dep.sea.regs["ESP"]-=x
    #    dothesearchHash(dep)
    
    
    #typical stack pivot to EAX
    regs={}
    regs["ESP"]=("EAX")
    regs["EIP"]=((),"EAX")
    dothesearch(dep, regs)
    

def dothesearch(dep, regs):
    imm=Debugger()
    props=dep.gdb.translate_properties(regs)
    imm.log(repr(props))
    gen=dep.gdb.search_by_properties(props, dep.props)
    for info in gen:
        imm.log("modid=%d, offset=0x%x, complexity=%d"%(info[0], info[1], info[2]), dep.bases[info[0]]+info[1])

def dothesearchHash(dep):
    imm=Debugger()
    
    hashes=dep.sea.hashState()
    gen=dep.gdb.search_by_hashes(hashes, dep.hashes)
    for info in gen:
        imm.log("modid=%d, offset=0x%x, complexity=%d"%(info[0], info[1], info[2]), dep.bases[info[0]]+info[1])
    
    dep.cleanSearch()

mymain()
