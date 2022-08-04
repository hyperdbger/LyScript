# x64dbg Automation control plug-in

<br>
<div align=center>
  <img width="100" src="https://cdn.lyshark.com/archive/LyScript/bug_black.png"/><tr>
    <img width="100" src="https://cdn.lyshark.com/archive/LyScript/python.png"/>
 <br><br><br>
  
  [简体中文](README.md) | [ENGLISH](README-EN.md) | [русский язык ](README-RU.md)

  <br>
  
[![Build status](https://cdn.lyshark.com/archive/LyScript/build.svg)](https://github.com/lyshark/LyScript) [![Open Source Helpers](https://cdn.lyshark.com/archive/LyScript/users.svg)](https://github.com/lyshark/LyScript) [![Crowdin](https://cdn.lyshark.com/archive/LyScript/email.svg)](mailto:me@lyshark.com) [![Download x64dbg](https://cdn.lyshark.com/archive/LyScript/x64dbg.svg)](https://github.com/lyshark/LyScript/releases/tag/LyScript) [![OSCS Status](https://www.oscs1024.com/platform/badge/lyshark/LyScript.svg?size=small)](https://www.oscs1024.com/project/lyshark/LyScript?ref=badge_small)

[![python3](https://cdn.lyshark.com/archive/LyScript/python3.svg)](https://github.com/lyshark/LyScript) [![platform](https://cdn.lyshark.com/archive/LyScript/platform.svg)](https://github.com/lyshark/LyScript)

<br><br>
An x64dbg automation control plug-in, which controls x64dbg through python, realizes remote dynamic debugging, solves the problems that reverse workers analyze vulnerabilities, find instruction fragments, and the native script is not powerful enough. By combining with Python, it uses the flexibility of Python syntax and rich third-party libraries to improve analysis efficiency and realize automatic code analysis.
  
</div>
<br>

 - Install Python package：`pip install LyScript32` or `pip install LyScript64`
 - PluginDownload：<a href="https://cdn.lyshark.com/software/LyScript32.zip">LyScript32 (32bit)</a> or <a href="https://cdn.lyshark.com/software/LyScript64.zip">LyScript64 (64bit)</a>

After downloading the plug-in, please copy the plug-in to the plugins directory under the x64dbg directory, and the plug-in file will be loaded automatically after the program runs.

![](https://img2022.cnblogs.com/blog/1379525/202203/1379525-20220327190905044-1815692787.png)

After the plug-in is loaded successfully, you will see the specific binding information and output debugging in the log position, and the plug-in will not be displayed in the plug-in bar.

![image](https://user-images.githubusercontent.com/52789403/161062658-0452fe0c-3e11-4df4-a83b-b026f74884d0.png)

If remote debugging is required, you only need to input the IP address of the opposite end when initializing the `mydebug()` class. If you do not fill in the parameters, the `127.0.0.1` address is used by default. Please ensure that the opposite end releases the `6589` port, otherwise you cannot connect.

![image](https://user-images.githubusercontent.com/52789403/161062393-df04aabb-2d70-4434-80b9-a46974bccf8a.png)

Run the x64dbg program and manually load the executable file to be analyzed. Then we can connect to the debugger through the `connect()` method. After connecting, a persistent session will be created until the python script ends, and the connection will be forcibly disconnected. During this period, ` is_connect() ` check whether the link still exists. The specific code is as follows.
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    # 初始化
    dbg = MyDebug()

    # 连接到调试器
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 检测套接字是否还在
    ref = dbg.is_connect()
    print("是否在连接: ", ref)

    dbg.close()
```
<br>

### Register class

**get_register():** This function is mainly used to obtain a specific register. The user needs to pass in the name of the register to be obtained.

 - Parameter 1：Incoming register string

Available range："DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI", "ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP"

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eax = dbg.get_register("eax")
    ebx = dbg.get_register("ebx")

    print("eax = {}".format(hex(eax)))
    print("ebx = {}".format(hex(ebx)))

    dbg.close()
```
If you are using a 64 bit plug-in, the support range of registers will be wider.

Available range extension： "DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI", "ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP", "RAX", "RBX", "RCX", "RDX", "RSI", "SIL", "RDI", "DIL", "RBP", "BPL", "RSP", "SPL", "RIP", "R8", "R8D", "R8W", "R8B", "R9", "R9D", "R9W", "R9B", "R10", "R10D", "R10W", "R10B", "R11", "R11D", "R11W", "R11B", "R12", "R12D", "R12W", "R12B", "R13", "R13D", "R13W", "R13B", "R14", "R14D", "R14W", "R14B", "R15", "R15D", "R15W", "R15B"

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
    print("获取R系列寄存器: {}".format(hex(r8)))

    dbg.close()
```

**set_register():** This function sets the parameters of the specified register. Similarly, 64 bit will support the parameter modification of more registers.

 - Parameter 1：Incoming register string
 - Parameter 2：Decimal value

Available range："DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI", "ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP"

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eax = dbg.get_register("eax")
    
    dbg.set_register("eax",100)

    print("eax = {}".format(hex(eax)))

    dbg.close()
```

**get_flag_register():** Used to obtain a flag bit parameter. The return value is only true or false.

 - Parameter 1：Register string

Available register range："ZF", "OF", "CF", "PF", "SF", "TF", "AF", "DF", "IF" 

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    cf = dbg.get_flag_register("cf")
    print("标志: {}".format(cf))
    
    dbg.close()
```

**set_flag_register():** Used to set a flag bit parameter. The return value is only true or false.
 
 - Parameter 1：Register string
 - Parameter 2：[ Set to true True] / [Set to false False]

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

### Debugging class

**set_debug():** Used to affect the debugger, such as forward once, backward once, pause debugging, terminate, etc.

 - Parameter 1: Pass in the action to be performed

Available action range：[pause] [run] [step in] [step out] [step over] [stop] [wait]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    while True:
        dbg.set_debug("StepIn")
        
        eax = dbg.get_register("eax")
        
        if eax == 0:
            print("找到了")
            break
        
    dbg.close()
```

**set_debug_count():** This function is ` set_ Debug() ` the continuation of the function. The purpose is to execute the number of automatic steps.

 - Parameter 1：Pass in the action to be performed
 - Parameter 2：Number of execution repetitions

Available action range：[Pause] [Run] [StepIn]  [StepOut] [StepOver] [Stop] [Wait]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    dbg.set_debug_count("StepIn",10)

    dbg.close()
```

**is_debugger() /is_running():** `is_debugger()` can be used to verify whether the debugger is in debug state, `is_running()` is used to verify whether it is running.

- No parameter transfer

```Python
if __name__ == "__main__":
from LyScript32 import MyDebug
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.is_debugger()
    print(ref)

    ref = dbg.is_running()
    print(ref)

    dbg.close()
```

**set_breakpoint():** Setting breakpoint is separated from canceling breakpoint. Setting breakpoint only needs to pass in decimal memory address.

 - Parameter 1：Incoming memory address (decimal)
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    ref = dbg.set_breakpoint(eip)

    print("设置状态: {}".format(ref))
    dbg.close()
```

**delete_breakpoint():** This function passes in a memory address to cancel a memory breakpoint.

 - Parameter 1：Incoming memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    ref = dbg.set_breakpoint(eip)
    print("设置状态: {}".format(ref))

    del_ref = dbg.delete_breakpoint(eip)
    print("取消状态: {}".format(del_ref))

    dbg.close()
```

**check_breakpoint():** Used to check whether the next breakpoint has been hit. The hit returns true. Otherwise, it returns false.

 - Parameter 1：Incoming memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    ref = dbg.set_breakpoint(eip)
    print("设置状态: {}".format(ref))

    is_check = dbg.check_breakpoint(4134331)
    print("是否命中: {}".format(is_check))

    dbg.close()
```

**get_all_breakpoint():** It is used to get all the breakpoint information in the debugger, including whether to open, hit number, etc.

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

**set_hardware_breakpoint():** It is used to set a hardware breakpoint. Up to 4 hardware breakpoints can be set in a 32-bit system.

 - Parameter 1：Memory address (decimal)
 - Parameter 2：Breakpoint Type

Breakpoint type available range：[Type 0 = HardwareAccess / 1 = HardwareWrite / 2 = HardwareExecute]

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

**delete_hardware_breakpoint():** It is used to delete a hardware breakpoint. You only need to pass in the address without passing in the type.

 - Parameter 1：Memory address (decimal)

Breakpoint type available range：[type 0 = HardwareAccess / 1 = HardwareWrite / 2 = HardwareExecute]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug(address="127.0.0.1",port=6666)
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")

    ref = dbg.set_hardware_breakpoint(eip,2)
    print(ref)

    # 删除断点
    ref = dbg.delete_hardware_breakpoint(eip)
    print(ref)

    dbg.close()
```
<br>

### Module class

**get_module_base():** This function can be used to obtain the base address of a specified module loaded by the program.

 - Parameter 1：Module name string

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    
    user32_base = dbg.get_module_base("user32.dll")
    print(user32_base)

    dbg.close()
```

**get_all_module():** It is used to output all module information of the current loader and return it in the form of dictionary.

 - Parameter: no parameter

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

**get_local_():** Get the base address, length and memory attributes of the module where the current EIP is located. This function no parameter transfer obtains the data of the module pointed to by the current EIP.

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

 - Parameter 1：Module name
 - Parameter 2：Function name

The address is returned successfully, and false is returned in case of failure

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

**get_module_from_import():** Obtain the import table information of the specified module in the current program and output it as a list nested dictionary.

 - Parameter 1：Incoming module name

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

 - Parameter 1：Incoming module name

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

**get_section():** This function is used to output the section table information in the main program.

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

 - Parameter 1：Incoming memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    eip = dbg.get_register("eip")

    ref = dbg.get_base_from_address(eip)
    print("模块首地址: {}".format(hex(ref)))
```

**get_base_from_name():** Get the first memory address of the module according to the passed in module name.

 - Parameter 1：Incoming module name

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    eip = dbg.get_register("eip")

    ref_base = dbg.get_base_from_name("win32project.exe")
    print("模块首地址: {}".format(hex(ref_base)))

    dbg.close()
```

**get_oep_from_name():** Obtain the actual loading OEP location of the module according to the incoming module name.

 - Parameter 1：Incoming module name

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    oep = dbg.get_oep_from_name("win32project.exe")
    print(hex(oep))

    dbg.close()
```

**get_oep_from_address():** According to the incoming memory address, the OEP position of the address module is obtained.

 - Parameter 1：Incoming memory address

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
<br>

### Memory class

**read_memory_():** Read memory series functions, including readbyte, readword and readdword. Qword is only supported under 64 bits

 - Parameter 1：Memory address to be read (decimal)

Current support：
 - read_memory_byte() Read byte
 - read_memory_word() Read word
 - read_memory_dword() Read dword
 - read_memory_qword() Read qword （Only 64 bit is supported）
 - read_memory_ptr() Read pointer

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

**write_memory_():** Write memory series function，WriteByte,WriteWord,WriteDWORD,WriteQword

 - Parameter 1：Memory to write
 - Parameter 2：Byte to be written

Current support：
 - write_memory_byte() Write byte
 - write_memory_word() Write word
 - write_memory_dword() Write dword
 - write_memory_qword() Write qword （Only 64 bit is supported）
 - write_memory_ptr() Write pointer

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

**scan_memory_one():** Memory scanning is realized. When the first qualified feature is scanned, it will be output automatically.

 - Parameter 1：Signature field

 This function should be noted that if our x64dbg tool stops in the system airspace, it will search the features under the system airspace by default. If it is like that in the search program, you need to cut the EIP first.
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    ref = dbg.scan_memory_one("ff 25")
    print(ref)
    dbg.close()
```

**scan_memory_all():** It can scan all qualified characteristic fields and return a list after finding them.

 - Parameter 1：Signature field

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

**get_local_protect():** Get the value of the memory attribute, update the function, cancel the memory attribute that can only get the location indicated by the EIP, and the user can detect it at will.
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

**set_local_protect():** Add the function of setting memory attribute, pass in EIP memory address, set attribute 32 and set memory length 1024.
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    
    eip = dbg.get_register("eip")
    print(eip)

    b = dbg.set_local_protect(eip,32,1024)
    print("设置属性状态: {}".format(b))

    dbg.close()
```

**get_local_page_size():** Used to obtain the PageSize of memory under the airspace indicated by the current EIP.

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

**get_memory_section():** This function is mainly used to get the memory table data of the current debugger in the memory image.

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
<br>

### Stack class

**create_alloc()：** The function `createremotealloc()` can open up a heap space remotely and successfully return the first memory address.

 - Parameter 1：Heap length (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.create_alloc(1024)
    print("开辟地址: ", hex(ref))

    dbg.close()
```

**delete_alloc()：** Functions `delete_ Alloc()` used to unregister a remote heap space.

 - Parameter 1：Pass in the memory address of the heap space to be deleted.

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.create_alloc(1024)
    print("开辟地址: ", hex(ref))

    flag = dbg.delete_alloc(ref)
    print("删除状态: ",flag)

    dbg.close()
```

**push_stack():** Push a decimal number into the stack, which is at the top of the stack by default.

 - Parameter 1：Decimal data

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.push_stack(10)

    print(ref)

    dbg.close()
```

**pop_stack():** Pop function is used to push an element from the stack. By default, it pops up from the top of the stack.

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

**peek_stack():** Peek is used to check the parameters in the stack. You can set the offset value. If it is not set, the first one, that is, the top of the stack, will be checked by default.

 - Parameter 1：Decimal offset

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    # 无参数检查
    check = dbg.peek_stack()
    print(check)

    # 携带参数检查
    check_1 = dbg.peek_stack(2)
    print(check_1)

    dbg.close()
```
<br>

### Process thread class

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

**get_process_handle():** Used to get the current process handle information.

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

**get_process_id():** PID used to get the current loader

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

**get_teb_address() / get_peb_address():** It is used to obtain the current process environment block and the fast thread environment.

 - get_teb_address()  The passed in parameter is the thread ID
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

### Reverse compilation class

**get_disasm_code():** This function is mainly used to disassemble a specific memory address and pass in two parameters.

 - Parameter 1：Address to disassemble (decimal)
 - Parameter 2：The length that needs to be disassembled down

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 得到EIP位置
    eip = dbg.get_register("eip")

    # 反汇编前100行
    disasm_dict = dbg.get_disasm_code(eip,100)

    for ds in disasm_dict:
        print("地址: {} 反汇编: {}".format(hex(ds.get("addr")),ds.get("opcode")))

    dbg.close()
```

**get_disasm_one_code():** Read an assembly instruction in the position specified by the user, and the user can judge it as needed.
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    print("EIP = {}".format(eip))

    disasm = dbg.get_disasm_one_code(eip)
    print("反汇编一条: {}".format(disasm))

    dbg.close()
```

**get_disasm_operand_code():** It is used to obtain the operand in the assembly instruction. For example, `JMP 0x0401000`, the operand is`0x0401000`.

 - Parameter 1：Incoming memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    print("EIP = {}".format(eip))

    opcode = dbg.get_disasm_operand_code(eip)
    print("操作数: {}".format(hex(opcode)))

    dbg.close()
```

**get_disasm_operand_size():** Used to get the machine code length of the assembly code under the current memory address.

 - Parameter 1：Incoming memory address (decimal)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    print("EIP = {}".format(eip))

    opcode = dbg.get_disasm_operand_size(eip)

    print("机器码长度: {}".format(hex(opcode)))

    dbg.close()
```

**assemble_write_memory():** It realizes that the user passes in a correct assembly instruction, and the program automatically converts the instruction into machine code and writes it to the specified location.

 - Parameter 1：Write out memory address (decimal)
 - Parameter 2：Write assembly instructions

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    print(eip)

    ref = dbg.assemble_write_memory(eip,"mov eax,1")
    print("是否写出: {}".format(ref))

    dbg.close()
```

**assemble_code_size():** This function enables the user to input an assembly instruction and automatically calculate how many bytes the instruction occupies.

 - Parameter 1：like OPCODE

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.assemble_code_size("sub esp, 0x324")
    print(ref)

    dbg.close()
```

<br>

### Other general classes

**set_comment_notes():** Add a comment to the specified location code. The following is an example of adding a comment to the EIP location.

 - Parameter 1：Comment memory address
 - Parameter 2：Note Content

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

 - Parameter 1：Command statement

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.run_command_exec("bp MessageBoxA")
    print(ref)

    dbg.close()
```

**set_loger_output():** The output of log is particularly important. This module provides a custom log output function, which can output the specified log to x64dbg log location.

 - Parameter 1：Log content

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
