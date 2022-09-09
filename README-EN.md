# x64dbg Automation control plug-in

<br>
<div align=center>
	<img width="150" src="https://cdn.lyshark.com/archive/LyScript/lyscript_png.jpg" />
<!--
  <img width="100" src="https://cdn.lyshark.com/archive/LyScript/bug_black.png"/><tr>
    <img width="100" src="https://cdn.lyshark.com/archive/LyScript/python.png"/>
-->
 <br><br>
  
  [简体中文](README.md) | [ENGLISH](README-EN.md) | [русский язык ](README-RU.md)

  <br>
  
[![Build status](https://cdn.lyshark.com/archive/LyScript/build.svg)](https://github.com/lyshark/LyScript) [![Open Source Helpers](https://cdn.lyshark.com/archive/LyScript/users.svg)](https://github.com/lyshark/LyScript) [![Crowdin](https://cdn.lyshark.com/archive/LyScript/email.svg)](mailto:me@lyshark.com) [![Download x64dbg](https://cdn.lyshark.com/archive/LyScript/x64dbg.svg)](https://github.com/lyshark/LyScript/releases/tag/LyScript) [![OSCS Status](https://www.oscs1024.com/platform/badge/lyshark/LyScript.svg?size=small)](https://www.oscs1024.com/project/lyshark/LyScript?ref=badge_small)

[![python3](https://cdn.lyshark.com/archive/LyScript/python3.svg)](https://github.com/lyshark/LyScript) [![platform](https://cdn.lyshark.com/archive/LyScript/platform.svg)](https://github.com/lyshark/LyScript) [![lyscriptver](https://cdn.lyshark.com/archive/LyScript/lyscript_version.svg)](https://github.com/lyshark/LyScript)

<br><br>
An x64dbg automation control plug-in, which controls the behavior of x64dbg through python, realizes remote dynamic debugging, solves the problems of reverse workers analyzing programs, anti-virus personnel shelling, vulnerability analysts looking for instruction fragments, and native scripts not strong enough. By combining with Python, it makes use of the flexibility of Python syntax and its rich third-party libraries to accelerate the development of vulnerability exploitation programs, Assist in vulnerability mining and malware analysis.
  
</div>
<br>

Please install the python package with the same version as the plug-in. Execute the PIP command on the CMD command line to install it. It is recommended to install both packages.

 - Install standard package：`pip install LyScript32` OR `pip install LyScript64`
 - Install expansion pack：`pip install LyScriptTools32` OR `pip install LyScriptTools64`

Secondly, you need to manually download the driver file corresponding to `x64dbg` version and put it in the specified `plugins` directory.

 - Plug in download：<a href="https://github.com/lyshark/LyScript/raw/master/plugins/LyScript32-1.0.13.zip">LyScript32-1.0.13 (32bit)</a> OR <a href="https://github.com/lyshark/LyScript/raw/master/plugins/LyScript64-1.0.13.zip">LyScript64-1.0.13 (64bit)</a>

After downloading the plug-in, please copy the plug-in to the plugins directory of x64dbg. The plug-in will be loaded automatically after the program runs.

![image](https://user-images.githubusercontent.com/52789403/185293618-68102ea6-8c37-493e-8be3-ca46eca0f0b5.png)

After the plug-in is successfully loaded, you will see the specific binding information and output debugging in the log location. The plug-in will not be displayed in the plug-in bar.

![image](https://user-images.githubusercontent.com/52789403/161062658-0452fe0c-3e11-4df4-a83b-b026f74884d0.png)

If you need remote debugging, you only need to pass in the opposite IP address when initializing the `mydebug()` class. If you don't fill in the parameters, the `127.0.0.1` address will be used by default. Please make sure that the opposite side releases the `6589` port, otherwise you can't connect.

![image](https://user-images.githubusercontent.com/52789403/161062393-df04aabb-2d70-4434-80b9-a46974bccf8a.png)

Run the x64dbg program and manually load the executable file that needs to be analyzed. Then we can connect to the debugger through the `connect()` method. After connecting, a persistent session will be created until the python script ends, and the connection will be forcibly disconnected. During this period, we can call `is_connect()` check whether the link still exists. The specific code is as follows.
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    # initialization
    dbg = MyDebug()

    # Connect to debugger
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    # Check whether the socket is still in use
    ref = dbg.is_connect()
    print("Whether to connect: ", ref)

    dbg.close()
```
<br><br>

### Register family function

**get_register():** This function is mainly used for obtaining a specific register. The user needs to input the name of the register to be obtained.

 - Parameter1: incoming register string

Available range："DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI","ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP", "CIP", "CSP", "CAX", "CBX", "CCX", "CDX", "CDI", "CSI", "CBP", "CFLAGS"

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eax = dbg.get_register("eax")
    ebx = dbg.get_register("ebx")

    print("eax = {}".format(hex(eax)))
    print("ebx = {}".format(hex(ebx)))

    dbg.close()
```
If you are using a 64 bit plug-in, the supported range of registers will be e series plus R series.

Available range extension："DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI", "ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP", "RAX", "RBX", "RCX", "RDX", "RSI", "SIL", "RDI", "DIL", "RBP", "BPL", "RSP", "SPL", "RIP", "R8", "R8D", "R8W", "R8B", "R9", "R9D", "R9W", "R9B", "R10", "R10D", "R10W", "R10B", "R11", "R11D", "R11W", "R11B", "R12", "R12D", "R12W", "R12B", "R13", "R13D", "R13W", "R13B", "R14", "R14D", "R14W", "R14B", "R15", "R15D", "R15W", "R15B"

```Python
from LyScript64 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    rax = dbg.get_register("rax")
    eax = dbg.get_register("eax")
    ax = dbg.get_register("ax")

    print("rax = {} eax = {} ax ={}".format(hex(rax),hex(eax),hex(ax)))

    r8 = dbg.get_register("r8")
    print("Get R series register: {}".format(hex(r8)))

    dbg.close()
```

**set_register():** This function implements the setting of the specified register parameters. Similarly, 64 bits will support parameter modification of more registers.

 - Parameter1：Incoming register string
 - Parameter2：Decimal value

Available range："DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI", "ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP"

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eax = dbg.get_register("eax")
    
    dbg.set_register("eax",100)

    print("eax = {}".format(hex(eax)))

    dbg.close()
```

**get_flag_register():** It is used to obtain a flag bit parameter, and the return value is only true or false.

 - Parameter1：Register string

Available register range："ZF", "OF", "CF", "PF", "SF", "TF", "AF", "DF", "IF" 

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    cf = dbg.get_flag_register("cf")
    print("flag: {}".format(cf))
    
    dbg.close()
```

**set_flag_register():** Used to set a flag bit parameter. The return value can only be true or false.
 
 - Parameter1：Register string
 - Parameter2：[ Set to true True] / [Set to false False]

Available register range："ZF", "OF", "CF", "PF", "SF", "TF", "AF", "DF", "IF" 

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    zf = dbg.get_flag_register("zf")
    print(zf)

    dbg.set_flag_register("zf",False)

    zf = dbg.get_flag_register("zf")
    print(zf)

    dbg.close()
```
<br>

### Debug series functions

**set_debug():** It is used to influence the debugger, such as going forward once, going back once, pausing debugging, terminating, etc.

 - Parameter1: Input the action to be executed

Available action range: [Pause] [Run] [StepIn]  [StepOut] [StepOver] [Stop] [Wait]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    while True:
        dbg.set_debug("StepIn")
        
        eax = dbg.get_register("eax")
        
        if eax == 0:
            print("eureka")
            break
        
    dbg.close()
```

**set_debug_count():** This function is `set_debug()` function is a continuation of the function, which is used to execute the number of automatic steps.

 - Parameter1：Input the action to be executed
 - Parameter2：Number of execution repetitions

Available action range：[Pause] [Run] [StepIn]  [StepOut] [StepOver] [Stop] [Wait]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    dbg.set_debug_count("StepIn",10)

    dbg.close()
```

**is_debugger()/is_running()/is_run_locked():** Functions `is_ Debugger` can be used to verify whether the current debugger is in debugging state, `is_Running` is used to verify whether it is `running_ run_ Locked()`used to check whether the debugger is locked (paused).

- No parameter transfer

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.is_debugger()
    print(ref)

    ref = dbg.is_running()
    print(ref)

    ref = dbg.is_run_locked()
    print(ref)

    dbg.close()
```

**set_breakpoint():** Breakpoint setting and breakpoint canceling are separated. Setting breakpoints only requires passing in decimal memory addresses.

 - Parameter1：Incoming memory address (decimal)
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    ref = dbg.set_breakpoint(eip)

    print("Setting status: {}".format(ref))
    dbg.close()
```

**delete_breakpoint():** This function passes in a memory address to cancel a memory breakpoint.

 - Parameter1：Incoming memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    ref = dbg.set_breakpoint(eip)
    print("Setting status: {}".format(ref))

    del_ref = dbg.delete_breakpoint(eip)
    print("Cancel status: {}".format(del_ref))

    dbg.close()
```

**check_breakpoint():** It is used to check whether the next breakpoint is hit. If it is hit, it returns true; otherwise, it returns false.

 - Parameter1：Incoming memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    ref = dbg.set_breakpoint(eip)
    print("Setting status: {}".format(ref))

    is_check = dbg.check_breakpoint(4134331)
    print("Hit: {}".format(is_check))

    dbg.close()
```

**get_all_breakpoint():** It is used to obtain all the breakpoint information in the current debugging program, including whether it is enabled, hit times, etc.

 - No parameter transfer

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    ref = dbg.get_all_breakpoint()
    print(ref)
    dbg.close()
```

**set_hardware_breakpoint():** It is used to set a hardware breakpoint, which can be set up to 4 in a 32-bit system.

 - Parameter1：Memory address (decimal)
 - Parameter2：Breakpoint Type

Breakpoint type available range：[type 0 = HardwareAccess / 1 = HardwareWrite / 2 = HardwareExecute]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug(address="127.0.0.1",port=6666)
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")

    ref = dbg.set_hardware_breakpoint(eip,2)
    print(ref)

    dbg.close()
```

**delete_hardware_breakpoint():** It is used to delete a hardware breakpoint. It only needs to pass in an address, not a type.

 - Parameter1：Memory address (decimal)

Breakpoint type available range：[type 0 = HardwareAccess / 1 = HardwareWrite / 2 = HardwareExecute]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug(address="127.0.0.1",port=6666)
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")

    ref = dbg.set_hardware_breakpoint(eip,2)
    print(ref)

    # Remove Breakpoint
    ref = dbg.delete_hardware_breakpoint(eip)
    print(ref)

    dbg.close()
```

**is_bp_disable():** This function is used to verify whether the BP breakpoint at the specified address is disabled.

 - Parameter1：Memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    is_false = dbg.is_bp_disable(eip)
    print("BP breakpoint status: {}".format(is_false))

    dbg.close()
```

**get_xref_count_at():** Gets the cross reference count at the specified memory address location.

 - Parameter1：Memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    types = dbg.get_xref_count_at(eip)
    print("Reference count: {}".format(types))

    dbg.close()
```

**get_function_type_at():** Gets the function type at the specified memory address location, which is the `functype` enumeration type.

 - Parameter1：Memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    types = dbg.get_function_type_at(eip)
    print("Function type: {}".format(types))

    if(types == 0):
        print("FUNC_NONE")
    elif(types == 1):
        print("FUNC_BEGIN")
    elif(types == 2):
        print("FUNC_MIDDLE")
    elif(types == 3):
        print("FUNC_END")
    elif(types == 4):
        print("FUNC_SINGLE")
    else:
        print("error")

    dbg.close()
```

**get_bpx_type_at():** Gets the BP breakpoint type at the specified address, which is an `bpxtype` enumeration.

 - Parameter1：Memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    types = dbg.get_bpx_type_at(eip)
    print("BPXtype: {}".format(types))

    if(types == 0):
        print("bp_none")
    elif(types == 1):
        print("bp_normal")
    elif(types == 2):
        print("bp_hardware")
    elif(types == 4):
        print("bp_memory")
    elif(types == 8):
        print("bp_dll")
    elif(types == 16):
        print("bp_exception")
    else:
        print("error")

    dbg.close()
```

**get_xref_type_at():** Get the cross reference type at the specified memory address location and enumerate the `xreftype` type.

 - Parameter1：Memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    types = dbg.get_xref_type_at(eip)
    print("reference type: {}".format(types))

    if(types == 0):
        print("XREF_NONE")
    elif(types == 1):
        print("XREF_DATA")
    elif(types == 2):
        print("XREF_JMP")
    elif(types == 3):
        print("XREF_CALL")
    else:
        print("error")

    dbg.close()
```
<br>

### Module family function

**get_module_base():** This function can be used to obtain the base address of a specified module loaded by the program.

 - Parameter1：Module name string

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    
    user32_base = dbg.get_module_base("user32.dll")
    print(user32_base)

    dbg.close()
```

**get_all_module():** It is used to output all module information of the current loader and return it in the form of a dictionary.

 - Parameters: no parameters

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_all_module()

    for i in ref:
        print(i)

    print(ref[0])
    print(ref[1].get("name"))
    print(ref[1].get("path"))

    dbg.close()
```

**get_local_():** Obtain the base address, length, and memory attributes of the module where the current EIP is located. This function no parameter transfer obtains the data of the module to which the current EIP points.

 - dbg.get_local_base()    Get module base address
 - dbg.get_local_size()    Get module length
 - dbg.get_local_protect() Get module protection properties

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_local_base()
    print(hex(ref))

    ref2 = dbg.get_local_size()
    print(hex(ref2))

    ref3 = dbg.get_local_protect()
    print(ref3)

    dbg.close()
```

**get_module_from_function():** Gets the memory address of the specified function in the specified module, which can be used to verify the virtual address of the specified function in the memory of the current program.

 - Parameter1：Module name
 - Parameter2：Function name

Address returned successfully, false returned in case of failure

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_module_from_function("user32.dll","MessageBoxW")
    print(hex(ref))

    ref2 = dbg.get_module_from_function("kernel32.dll","test")
    print(ref2)

    dbg.close()
```

**get_module_from_import():** Obtain the import table information of the specified module in the current program, and output it as a list nested dictionary.

 - Parameter1：Incoming module name

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_module_from_import("ucrtbase.dll")
    print(ref)

    ref1 = dbg.get_module_from_import("win32project1.exe")

    for i in ref1:
        print(i.get("name"))

    dbg.close()
```

**get_module_from_export():** This function is used to obtain the export table information in the current loader.

 - Parameter1：Incoming module name

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_module_from_export("msvcr120d.dll")

    for i in ref:
        print(i.get("name"), hex(i.get("va")))

    dbg.close()
```

**get_section():** This function is used to output section table information in the main program.

 - No parameter transfer

 ```Python
 from LyScript32 import MyDebug
 
if __name__ == "__main__":
    dbg = MyDebug(address="127.0.0.1",port=6666)
    connect_flag = dbg.connect()

    ref = dbg.get_section()
    print(ref)

    dbg.close()
```

**get_base_from_address():** Get the first address of the module according to the incoming memory address.

 - Parameter1：Incoming memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    eip = dbg.get_register("eip")

    ref = dbg.get_base_from_address(eip)
    print("Module first address: {}".format(hex(ref)))
```

**get_base_from_name():** Get the first memory address of the module according to the passed in module name.

 - Parameter1：Incoming module name

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    eip = dbg.get_register("eip")

    ref_base = dbg.get_base_from_name("win32project.exe")
    print("Module first address: {}".format(hex(ref_base)))

    dbg.close()
```

**get_oep_from_name():** Obtain the actual loading OEP location of the module according to the passed in module name.

 - Parameter1：Incoming module name

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    oep = dbg.get_oep_from_name("win32project.exe")
    print(hex(oep))

    dbg.close()
```

**get_oep_from_address():** Obtain the OEP location of the address module according to the incoming memory address.

 - Parameter1：Incoming memory address

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    eip = dbg.get_register("eip")

    oep = dbg.get_oep_from_address(eip)
    print(hex(oep))

    dbg.close()
```

**get_section_from_module_name():** The user can input the name of the currently loaded module, and directly take out the section table information of the specified module.

 - Parameter1：Module name (string)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    section_user32 = dbg.get_section_from_module_name("user32.dll")
    print(section_user32)

    section_ntdll = dbg.get_section_from_module_name("ntdll.dll")
    print(section_ntdll)

    dbg.close()
```

**size_from_address():** Pass in the base address of a module to get the total size occupied by the module.

 - Parameter1：Module address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    base = dbg.get_local_base()
    print(": {}".format(hex(base)))

    size = dbg.size_from_address(base)
    print("Module length: {}".format(size))

    dbg.close()
```

**size_from_name():** The total size occupied by the module is obtained by passing in the module name.

 - Parameter1：Module name (string)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    size = dbg.size_from_name("win32.exe")
    print("size: {}".format(size))

    dbg.close()
```

**section_count_from_name():** Pass in the module name to get how many sections there are in the module.

 - Parameter1：Module name (string)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    size = dbg.section_count_from_name("win32.exe")
    print("Number of sections: {}".format(size))

    dbg.close()
```

**section_count_from_address():** Pass in the module base address to get how many sections there are in the module.

 - Parameter1：Base address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    base = dbg.get_local_base()
    print("Module base address: {}".format(hex(base)))

    size = dbg.section_count_from_address(base)
    print("Number of sections: {}".format(size))

    dbg.close()
```

**path_from_name():** Pass in the module name and get the module path.

 - Parameter1：Module name (string)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    size = dbg.path_from_name("win32.exe")
    print("Module path: {}".format(size))

    dbg.close()
```

**path_from_address():** The module path is obtained by passing in the module address.

 - Parameter1：Module address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    base = dbg.get_local_base()
    print("Module base address: {}".format(hex(base)))

    path = dbg.path_from_address(base)
    print("Module path: {}".format(path))

    dbg.close()
```

**name_from_address():** The module name is obtained by passing in the module address.

 - Parameter1：Module address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    base = dbg.get_local_base()
    print("Module base address: {}".format(hex(base)))

    path = dbg.name_from_address(base)
    print("Module name: {}".format(path))

    dbg.close()
```

**get_window_handle():** Take out the handle of its own process module.

 - Parameter：No parameter transfer

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    base = dbg.get_window_handle()
    print("process handle: {}".format(base))

    dbg.close()
```

**get_module_at():** Obtain the module name at the specified memory address. The module name obtained here has no suffix.

 - Parameter1：Module address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    ref = dbg.get_module_at(eip)
    print("Module name: {}".format(ref))

    dbg.close()
```

**get_local_module():** This series of functions can be used to obtain the detailed information of the module where the current loader stays in the EIP.

 - get_local_module_size() Gets the size of the current program
 - get_local_module_section_Count() Get the number of self sections
 - get_local_module_path() Get the full path of the debugged program
 - get_local_module_name() Get its own module name
 - get_local_module_entry() Get its own module entry
 - get_local_module_base() Get its own module base address

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    print("Program size: {}".format( dbg.get_local_module_size()))
    print("Number of sections: {}".format(dbg.get_local_module_section_Count()))
    print("Full path: {}".format(dbg.get_local_module_path()))
    print("Module name: {}".format(dbg.get_local_module_name()))
    print("Module entry: {}".format(dbg.get_local_module_entry()))
    print("Module base address: {}".format(dbg.get_local_module_base()))

    dbg.close()
```
<br>

### Memory series function

**read_memory_():** Read memory series functions, including readbyte, readword and readdword formats. Qword is supported only in 64 bit mode

 - Parameter1：Memory address to be read (decimal)

Currently supported:

 - read_memory_byte() Read bytes
 - read_memory_word() Read word
 - read_memory_dword() Read dword
 - read_memory_qword() Read qword （only 64bit）
 - read_memory_ptr() Read Ptr

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")

    ref = dbg.read_memory_byte(eip)
    print(hex(ref))

    ref2 = dbg.read_memory_word(eip)
    print(hex(ref2))

    ref3 = dbg.read_memory_dword(eip)
    print(hex(ref3))

    ref4 = dbg.read_memory_ptr(eip)
    print(hex(ref4))

    dbg.close()
```

**write_memory_():** Write memory series functions, writebyte, writeword, writedword, writeqword

 - Parameter1：Memory to be written
 - Parameter2：Bytes to be written

Currently supported:

 - write_memory_byte() Write byte
 - write_memory_word() Write word
 - write_memory_dword() Write dword
 - write_memory_qword() Write qword （only 64bit）
 - write_memory_ptr() Write Ptr

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    addr = dbg.create_alloc(1024)
    print(hex(addr))

    ref = dbg.write_memory_byte(addr,10)

    print(ref)

    dbg.close()
```

**scan_memory_one():** Memory scanning is realized, and when the first qualified feature is scanned, it is automatically output.

 - Parameter1：

This function needs to be noted that if our x64dbg tool stops in the system airspace, it will search the features under the system airspace by default. If you want to search the data in the program airspace, you need to switch the EIP to operate first.
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    ref = dbg.scan_memory_one("ff 25")
    print(ref)
    dbg.close()
```

**scan_memory_all():** It realizes scanning all qualified feature fields, and returns a list after finding them.

 - Parameter1：Signature field

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.scan_memory_all("ff 25")

    for index in ref:
        print(hex(index))

    dbg.close()
```

**scan_memory_any():** This function can scan down the feature field of a specific length for a specific position.

 - Parameter1：Scan start address (decimal)
 - Parameter2：Scan length (decimal)
 - Parameter3：Signature field

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    # Arbitrary address scanning
    eip = dbg.get_register("eip")
    ref = dbg.scan_memory_any(eip,1024,"8b 50 04 8b fe")
    print("Get scan results: {}".format(hex(ref)))

    dbg.close()
```

**get_local_protect():** Get the memory attribute and transfer the value. This function updates. It eliminates the need to get only the memory attribute of the location indicated by the EIP. The user can detect it at will.

 - Parameter1：Memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    print(eip)

    ref = dbg.get_local_protect(eip)
    print(ref)
```

**set_local_protect():** Add the function of setting memory properties, pass in the EIP memory address, set the property 32, and set the memory length 1024.

 - Parameter1：Memory address (decimal)
 - Parameter2：Permission type（32=e/r 30=e 2=r/w）
 - Parameter3：Attribute length (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    
    eip = dbg.get_register("eip")
    print(eip)

    b = dbg.set_local_protect(eip,32,1024)
    print("Set attribute status: {}".format(b))

    dbg.close()
```

**get_local_page_size():** Used to obtain the PageSize of memory in the location indicated by the current EIP.

 - No parameter transfer

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    size = dbg.get_local_page_size()
    print("pagesize = {}".format(size))

    dbg.close()
```

**get_memory_section():** This function is mainly used to obtain the memory section table data of the current debugger in the memory image.

 - No parameter transfer
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_memory_section()
    print(ref)
    dbg.close()
```

**is_jmp_going_to_execute():** Determine whether the memory address jumps to the executable memory block.

 - Parameter1：Memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    flag = dbg.is_jmp_going_to_execute(eip)
    print("Jump (executable): {}".format(flag))

    dbg.close()
```

**mem_find_base_addr():** Returns the memory module base address and size at a specific location in the form of a dictionary.

 - Parameter1：Memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    dic = dbg.mem_find_base_addr(eip)

    print("Memory base address: {}".format(hex(dic.get("base"))))
    print("Memory size: {}".format(dic.get("size")))

    dbg.close()
```

**mem_get_page_size():** Gets the length of the memory page at the specified location.

 - Parameter1：Memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    addr = dbg.mem_get_page_size(eip)

    print("Memory page length: {}".format(hex(addr)))

    dbg.close()
```

**mem_is_valid():** Verify that the memory address at the specified location is readable.

 - Parameter1：Memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    is_read = dbg.mem_is_valid(eip)
    print("Memory address attribute: {}".format(is_read))

    dbg.close()
```
<br>

### Stack series functions

**create_alloc():** function`create_alloc()`A heap space can be opened remotely, and the first address of memory can be returned successfully.

 - Parameter1：Open heap length (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.create_alloc(1024)
    print("Open heap length: ", hex(ref))

    dbg.close()
```

**delete_alloc():** function`delete_alloc()`Used to destroy a remote heap space.

 - Parameter1：Pass in the memory address of the heap space to be deleted

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.create_alloc(1024)
    print("Opening address: ", hex(ref))

    flag = dbg.delete_alloc(ref)
    print("deleted state: ",flag)

    dbg.close()
```

**push_stack():** Push a decimal number into the stack, which is at the top of the stack by default.

 - Parameter1：Decimal data

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.push_stack(10)

    print(ref)

    dbg.close()
```

**pop_stack():** The pop function is used to push an element from the stack, which is popped from the top of the stack by default.

 - No parameter transfer

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    tt = dbg.pop_stack()
    print(tt)

    dbg.close()
```

**peek_stack():** Peek is used to check the parameters in the stack. The offset value can be set. If it is not set, the first one, that is, the top of the stack, will be checked by default.

 - Parameter1：Decimal offset

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    # No parameter check
    check = dbg.peek_stack()
    print(check)

    # Carry parameter check
    check_1 = dbg.peek_stack(2)
    print(check_1)

    dbg.close()
```
<br>

### Process thread series functions

**get_thread_list():** This function can output the information of all running threads of the current process.

 - No parameter transfer

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_thread_list()
    print(ref[0])
    print(ref[1])

    dbg.close()
```

**get_process_handle():** Used to obtain the handle information of the current process.

 - No parameter transfer

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_process_handle()
    print(ref)

    dbg.close()
```

**get_process_id():** Used to get the PID of the current loader.

 - No parameter transfer

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_process_id()
    print(ref)

    dbg.close()
```

**get_teb_address() / get_peb_address():** It is used to get the current process environment block, and the thread environment is fast.

 - get_teb_address()  The parameter passed in is the thread ID
 - get_peb_address()  The parameter passed in is the process ID

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_teb_address(6128)
    print(ref)

    ref = dbg.get_peb_address(9012)
    print(ref)

    dbg.close()
```
<br>

### Disassembly series functions

**get_disasm_code():** This function is mainly used to disassemble a specific memory address, passing in two parameters.

 - Parameter1：Address to be disassembled (decimal)
 - Parameter2：The length that needs to be disassembled downward

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    # Get the EIP location
    eip = dbg.get_register("eip")

    # First 100 lines of disassembly
    disasm_dict = dbg.get_disasm_code(eip,100)

    for ds in disasm_dict:
        print("Address: {} disassembly: {}".format(hex(ds.get("addr")),ds.get("opcode")))

    dbg.close()
```

**get_disasm_one_code():** Read an assembly instruction at the position specified by the user, and the user can judge it according to needs.
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    print("EIP = {}".format(eip))

    disasm = dbg.get_disasm_one_code(eip)
    print("Disassembly one: {}".format(disasm))

    dbg.close()
```

**get_disasm_operand_code():** It is used to obtain the operands in assembly instructions. For example, 'JMP 0x0401000' has an operand of '0x0401000'.

 - Parameter1：Incoming memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    print("EIP = {}".format(eip))

    opcode = dbg.get_disasm_operand_code(eip)
    print("Operands: {}".format(hex(opcode)))

    dbg.close()
```

**get_disasm_operand_size():** Used to obtain the machine code length of the assembly code under the current memory address.

 - Parameter1：Memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    print("EIP = {}".format(eip))

    opcode = dbg.get_disasm_operand_size(eip)

    print("Machine code length: {}".format(hex(opcode)))

    dbg.close()
```

**assemble_write_memory():** It realizes that the user inputs a correct assembly instruction, and the program automatically converts the instruction into machine code and writes it to the specified location.

 - Parameter1：Write Memory address (decimal)
 - Parameter2：Write assembly instructions

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    print(eip)

    ref = dbg.assemble_write_memory(eip,"mov eax,1")
    print("Whether to write: {}".format(ref))

    dbg.close()
```

**assemble_code_size():** This function realizes the automatic calculation of how many bytes the instruction occupies when the user inputs an assembly instruction.

 - Parameter1：like OPCODE

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.assemble_code_size("sub esp, 0x324")
    print(ref)

    dbg.close()
```

**get_branch_destination():** Get the jump address of call or JX jump instruction.

 - Parameter1：get Memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    print("Current EIP address: {}".format(hex(eip)))

    value = dbg.get_branch_destination(eip)
    print("Operands: {}".format(hex(value)))

    dbg.close()
```

**get_disassembly():** Disassemble an instruction. This function directly outputs what you see in debugging, including symbols.

 - Parameter1：get Memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    print("Current EIP address: {}".format(hex(eip)))

    dasm = dbg.get_disassembly(eip)
    print("Disassembly one: {}".format(dasm))

    dbg.close()
```

**assemble_at():** An assembly series of functions, passing in an assembly instruction, directly writes the instruction to memory.

 - Parameter1：get Memory address (decimal)
 - Parameter2：Assembly instruction (string)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    print("Current EIP address: {}".format(hex(eip)))

    ref = dbg.assemble_at(eip,"nop")
    print("Write status: {}".format(ref))

    dbg.close()
```

**disasm_fast_at():** This function also disassembles one line and returns the dictionary, but it can get more valid parameters.

 - Parameter1：get Memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    print("Current EIP address: {}".format(hex(eip)))

    dasm = dbg.disasm_fast_at(eip)
    print("address: {}".format(hex(dasm.get("addr"))))
    print("Assembly instruction: {}".format(dasm.get("disasm")))
    print("Assembly length: {}".format(dasm.get("size")))
    print("Branch: {}".format(dasm.get("is_branch")))
    print("whethercall: {}".format(dasm.get("is_call")))
    print("type: {}".format(dasm.get("type")))

    dbg.close()
```
<br>

### Other series functions

**set_comment_notes():** Add a comment to the code at the specified location. The following shows how to add a comment at the EIP location.

 - Parameter1：Comment memory address
 - Parameter2：Note Content

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    ref = dbg.set_comment_notes(eip,"hello lyshark")
    print(ref)

    dbg.close()
```

**run_command_exec():** Execute built-in commands, such as BP, dump, etc.

 - Parameter1：Command statement

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.run_command_exec("bp MessageBoxA")
    print(ref)

    dbg.close()
```

**set_loger_output():** Log output is particularly important. This module provides a custom log output function, which can output specified logs to x64dbg log locations.

 - Parameter1：Log content

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    for i in range(0,100):
        ref = dbg.set_loger_output("hello lyshark -> {} \n".format(i))
        print(ref)

    dbg.close()
```

**run_command_exe_ref():** This function is`run_command_exec()`It mainly adds the function of transferring out parameter. At present, integer types can be transferred out.

 - Parameter1：Command statement

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    ref = dbg.run_command_exe_ref("mod.base(eip)")
    print("ret Parameter: {}".format(hex(ref)))

    dbg.close()
```

**set_status_bar_message():** This function can output a string passed in by the user on the status bar at the bottom of x64dbg.

 - Parameter1：Output string
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    dbg.set_status_bar_message("EIP => {}".format(hex(eip)))

    dbg.close()
```

**script_loader():** This function receives the path of the built-in script passed in by the user and loads the script into x64dbg.

 - Parameter1：Script path:

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    flag = dbg.script_loader("d://x64dbg_script.txt")
    print("ret: {}".format(flag))

    dbg.close()
```

**script_unloader():** This function is used to close open scripts in x64dbg.

 - Parameter：No parameter transfer

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    flag = dbg.script_loader("d://x64dbg_script.txt")
    print("ret: {}".format(flag))
    
    dbg.script_unloader()

    dbg.close()
```

**script_run():** This function is used to run a script that has been loaded into x64dbg.

 - Parameter1：Number of running records (can be blank)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    flag = dbg.script_loader("d://x64dbg_script.txt")
    print("ret: {}".format(flag))

    dbg.script_run()

    dbg.close()
```

**script_set_ip():** This function is used to specify the line from which to run the script.

 - Parameter1：Run subscript

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    flag = dbg.script_loader("d://x64dbg_script.txt")
    print("ret: {}".format(flag))

    dbg.script_set_ip(3)

    dbg.close()
```

**open_debug():** This function is used to open a debugged program on the disk.

 - Parameter1：Full path of the opened program

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    flag = dbg.open_debug("d://win32.exe")

    dbg.close()
```

**close_debug():** This function is used to close the currently open debugger without closing the debugger.

 - Parameter：No parameter transfer

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    flag = dbg.open_debug("d://win32.exe")
    
    if flag == True:
        dbg.close_debug()
    
    dbg.close()
```

**detach_debug():** This function is used to detach the debugger from the process and the process will be run.

 - Parameter：No parameter transfer

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    flag = dbg.open_debug("d://win32.exe")

    if flag == True:
        dbg.detach_debug()

    dbg.close()
```

**message_box():** This function provides three dialog boxes, one for inputting text, one for judging whether it is selected or not, and the other is a common pop-up window.

 - Parameter1：Pop up prompt

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    conn = dbg.connect()

    # Pop up input box
    flag = dbg.input_string_box("Please enter the disassembly entry address?")
    print("User input: {}".format(flag))

    # Pop up yes / no box
    flag = dbg.message_box_yes_no("Continue shelling?")
    if flag == True:
        print("Shelling")
    else:
        print("exit")

    # prompt box
    flag = dbg.message_box("This is the {} Times, abnormal".format(1))
    print("flag: {}".format(flag))

    dbg.close()
```

**set_argument_brackets():** This function can add parentheses at the comment.

 - Parameter1：Start position (decimal)
 - Parameter2：End position (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    ref = dbg.set_argument_brackets(eip, eip +100)
    print("Add note: {}".format(ref))
    
    dbg.close()
```

**del_argument_brackets():** This function clears the`set_argument_brackets`Set parentheses.

 - Parameter1：Start position (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    
    dbg.del_argument_brackets(eip)

    dbg.close()
```

**set_function_brackets():** This function can add parentheses to the machine code position.

 - Parameter1：Start position (decimal)
 - Parameter2：End position (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    flag = dbg.set_function_brackets(eip,eip+10)

    dbg.close()
```

**del_function_brackets():** This function clears `set_function_brackets` parentheses set by.

 - Parameter1：Start position (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    
    dbg.del_function_brackets(eip)

    dbg.close()
```

**set_loop_brackets():** This function can add parentheses at the disassembly position.

 - Parameter1：Start position (decimal)
 - Parameter2：End position (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    ref = dbg.set_loop_brackets(eip,eip + 10)
    print("Setting status: {}".format(ref))

    dbg.close()
```

**del_loop_brackets():** This function clears the`set_loop_brackets`Set parentheses.

 - Parameter1：Clear hierarchy (default 1)
 - Parameter2：Start position (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    ref = dbg.del_loop_brackets(1,eip)
    print("erase status: {}".format(ref))

    dbg.close()
```

**set_label_at():** This function can set a label at a specific location.

 - Parameter1：Set the address of the label (decimal)
 - Parameter2：Tag name (string)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    
    dbg.set_label_at(eip,"test1")
    dbg.set_label_at(eip+10,"test2")

    dbg.close()
```

**location_label_at():** This function can locate the location through the existing tag and return the memory address.

 - Parameter1：Tag name (string)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    
    lab_addr = dbg.location_label_at("test2")
    print("Memory of label: {}".format(hex(lab_addr)))

    dbg.close()
```

**clear_label():** This function is used to clear all tags in the current program.

 - Parameter：No parameter transfer

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    ref = dbg.clear_label()

    dbg.close()
```

**update_all_view():** Refresh attempt function, with switching CPU location.

 - Parameter：No parameter transfer
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("Connection status: {}".format(connect_flag))

    # Refresh attempt
    dbg.update_all_view()
    
    # Switch to CPU window
    dbg.switch_cpu()
    
    # Clear all logs
    dbg.clear_log()

    dbg.close()
```
<br>
<b>Russian is incomplete. For complete comments, please read the Chinese version.</b>
