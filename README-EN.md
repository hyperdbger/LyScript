# x64dbg Automation control plug-in

<br>
<div align=center>
  <img width="100" src="https://cdn.lyshark.com/archive/LyScript/bug_black.png"/><tr>
    <img width="100" src="https://cdn.lyshark.com/archive/LyScript/python.png"/>
 <br><br><br>
  
  [简体中文](README.md) | [ENGLISH](README-EN.md) | [русский язык ](README-RU.md)

  <br>
  
[![Build status](https://cdn.lyshark.com/archive/LyScript/build.svg)](https://github.com/lyshark/LyScript) [![Open Source Helpers](https://cdn.lyshark.com/archive/LyScript/users.svg)](https://github.com/lyshark/LyScript) [![Crowdin](https://cdn.lyshark.com/archive/LyScript/email.svg)](mailto:me@lyshark.com) [![Download x64dbg](https://cdn.lyshark.com/archive/LyScript/x64dbg.svg)](https://sourceforge.net/projects/x64dbg/files/latest/download)

<br><br>
An x64dbg automation control plug-in, which controls x64dbg through python, realizes remote dynamic debugging, solves the problems that reverse workers analyze vulnerabilities, find instruction fragments, and the native script is not powerful enough. By combining with Python, it uses the flexibility of Python syntax and rich third-party libraries to improve analysis efficiency and realize automatic code analysis.
  
</div>
<br>

 - Install Python package：`pip install LyScript32` or `pip install LyScript64`
 - 32bit Plug in download：https://cdn.lyshark.com/software/LyScript32.zip
 - 64bit Plug in download：https://cdn.lyshark.com/software/LyScript64.zip

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

**get_thread_list():** 该函数可输出当前进程所有在运行的线程信息。

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

**get_process_handle():** 用于获取当前进程句柄信息。

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

**get_process_id():** 用于获取当前加载程序的PID

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

**get_teb_address() / get_peb_address():** 用于获取当前进程环境块，和线程环境快。

 - get_teb_address()  传入参数是线程ID
 - get_peb_address() 传入参数是进程ID

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

**get_disasm_code():** 该函数主要用于对特定内存地址进行反汇编，传入两个参数。

 - Parameter 1：需要反汇编的地址(十进制) 
 - Parameter 2：需要向下反汇编的长度

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

**get_disasm_one_code():** 在用户指定的位置读入一条汇编指令，用户可根据需要对其进行判断。
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

**get_disasm_operand_code():** 用于获取汇编指令中的操作数，例如`jmp 0x0401000`其操作数就是`0x0401000`。

 - Parameter 1：传入内存地址（十进制）

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

**get_disasm_operand_size():** 用于得当前内存地址下汇编代码的机器码长度。

 - Parameter 1：传入内存地址（十进制）

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

**assemble_write_memory():** 实现了用户传入一段正确的汇编指令，程序自动将该指令转为机器码，并写入到指定位置。

 - Parameter 1：写出内存地址（十进制）
 - Parameter 2：写出汇编指令

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

**assemble_code_size():** 该函数实现了用户传入一个汇编指令，自动计算出该指令占多少个字节。

 - Parameter 1：汇编指令字符串

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

**set_comment_notes():** 给指定位置代码增加一段注释，如下演示在eip位置增加注释。

 - Parameter 1：注释内存地址
 - Parameter 2：注释内容

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

**run_command_exec():** 执行内置命令，例如bp,dump等。

 - Parameter 1：命令语句

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.run_command_exec("bp MessageBoxA")
    print(ref)

    dbg.close()
```

**set_loger_output():** 日志的输出尤为重要，该模块提供了自定义日志输出功能，可将指定日志输出到x64dbg日志位置。

 - Parameter 1：日志内容

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
<br>

### General case

**PEFile载入内存格式:** 案例演示了，如何将一个可执行文件中的内存数据通过PEfile模块打开。
```Python
from LyScript32 import MyDebug
import pefile

if __name__ == "__main__":
    # 初始化
    dbg = MyDebug()
    dbg.connect()

    # 得到text节基地址
    local_base = dbg.get_local_base()

    # 根据text节得到程序首地址
    base = dbg.get_base_from_address(local_base)

    byte_array = bytearray()
    for index in range(0,4096):
        read_byte = dbg.read_memory_byte(base + index)
        byte_array.append(read_byte)

    oPE = pefile.PE(data = byte_array)
    timedate = oPE.OPTIONAL_HEADER.dump_dict()
    print(timedate)
```

**全模块特征匹配:** 针对所有模块中的特征码模糊匹配，找到会返回内存地址。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    for entry in dbg.get_all_module():
        eip = entry.get("entry")

        if eip != 0:
            dbg.set_register("eip",eip)

            search = dbg.scan_memory_one("ff 25 ??")
            print(hex(search))

    dbg.close()
```

**运用Python搜索汇编特征:** 使用python实现方法，通过特定方法扫描内存范围，如果出现我们所需要的指令集序列，则输出该指令的具体内存地址。
```Python
from LyScript32 import MyDebug

# 检索指定序列中是否存在一段特定的指令集
def SearchOpCode(OpCodeList,SearchCode,ReadByte):
            pass

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 得到EIP位置
    eip = dbg.get_register("eip")

    # 反汇编前1000行
    disasm_dict = dbg.get_disasm_code(eip,1000)

    # 搜索一个指令序列,用于快速查找构建漏洞利用代码
    SearchCode = [
        ["push 0xC0000409", "call 0x003F1B38", "pop ecx"],
        ["mov ebp, esp", "sub esp, 0x324"]
    ]

    # 检索内存指令集
    for item in range(0,len(SearchCode)):
        Search = SearchCode[item]
        # disasm_dict = 返回汇编指令 Search = 寻找指令集 1000 = 向下检索长度
        ret = SearchOpCode(disasm_dict,Search,1000)
        if ret != None:
            print("指令集: {} --> 首次出现地址: {}".format(SearchCode[item],hex(ret)))

    dbg.close()
```

**得到汇编指令机器码:** 该功能主要实现，得到用户传入汇编指令所对应的机器码，这段代码你可以这样来实现。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    addr = dbg.create_alloc(1024)

    print("堆空间: {}".format(hex(addr)))

    asm_size = dbg.assemble_code_size("mov eax,1")
    print("汇编代码占用字节: {}".format(asm_size))

    write = dbg.assemble_write_memory(addr,"mov eax,1")

    byte_code = bytearray()

    for index in range(0,asm_size):
        read = dbg.read_memory_byte(addr + index)
        print("{:02x} ".format(read),end="")

    dbg.delete_alloc(addr)
```
封装上方代码，你就可以实现一个汇编指令获取工具了，如下`get_opcode_from_assemble()`函数。
```Python
from LyScript32 import MyDebug

# 传入汇编代码,得到对应机器码
def get_opcode_from_assemble(dbg_ptr,asm):
              pass

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 获取汇编代码
    byte_array = get_opcode_from_assemble(dbg,"xor eax,eax")
    for index in byte_array:
        print(hex(index),end="")
    print()

    # 汇编一个序列
    asm_list = ["xor eax,eax", "xor ebx,ebx", "mov eax,1"]
    for index in asm_list:
        byte_array = get_opcode_from_assemble(dbg, index)
        for index in byte_array:
            print(hex(index),end="")
        print()

    dbg.close()
```

**如何劫持EIP:** 这里我们演示一个案例，你可以自己实现一个`write_opcode_from_assemble()`函数批量将列表中的指令集写出到内存，演示案例。
```Python
from LyScript32 import MyDebug

# 传入汇编指令列表,直接将机器码写入对端内存
def write_opcode_from_assemble(dbg_ptr,asm_list):
              pass

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 写出指令集到内存
    asm_list = ['mov eax,1','mov ebx,2','add eax,ebx']
    write_addr = write_opcode_from_assemble(dbg,asm_list)
    print("写出地址: {}".format(hex(write_addr)))

    # 设置执行属性
    dbg.set_local_protect(write_addr,32,1024)

    # 将EIP设置到指令集位置
    dbg.set_register("eip",write_addr)

    dbg.close()
```
如何执行函数呢？很简单，看以下代码是如何实现的，相信你能看懂，运行后会看到一个错误弹窗，说明程序执行流已经被转向了。
```Python
from LyScript32 import MyDebug

# 传入汇编指令列表,直接将机器码写入对端内存
def write_opcode_from_assemble(dbg_ptr,asm_list):
              pass

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 得到messagebox内存地址
    msg_ptr = dbg.get_module_from_function("user32.dll","MessageBoxA")
    call = "call {}".format(str(hex(msg_ptr)))
    print("函数地址: {}".format(call))

    # 写出指令集到内存
    asm_list = ['push 0','push 0','push 0','push 0',call]
    write_addr = write_opcode_from_assemble(dbg,asm_list)
    print("写出地址: {}".format(hex(write_addr)))

    # 设置执行属性
    dbg.set_local_protect(write_addr,32,1024)

    # 将EIP设置到指令集位置
    dbg.set_register("eip",write_addr)

    # 执行代码
    dbg.set_debug("Run")

    dbg.close()
```

**内存字节变更后回写:** 封装字节函数`write_opcode_list()`传入内存地址，对该地址中的字节更改后再回写到原来的位置。

 - 加密算法在内存中会通过S盒展开解密，有时需要特殊需求，捕捉解密后的S-box写入内存，或对矩阵进行特殊处理后替换，这样写即可实现。

```Python
from LyScript32 import MyDebug

# 对每一个字节如何处理
def write_func(x):
    x = x + 10
    return x

# 对指定内存地址机器码进行相应处理
def write_opcode_list(dbg_ptr, address, count, function_ptr):
    for index in range(0, count):
        read = dbg_ptr.read_memory_byte(address + index)

        ref = function_ptr(read)
        print("处理后结果: {}".format(ref))

        dbg.write_memory_byte(address + index, ref)
    return True

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 得到EIP
    eip = dbg.get_register("eip")

    # 对指定内存中的数据+10后写回去
    write_opcode_list(dbg,eip,100,write_func)

    dbg.close()
```

**指令集探针快速检索:** 快速检索当前程序中所有模块中是否存在特定的指令集片段，存在则返回内存地址。
```Python
from LyScript32 import MyDebug

# 将bytearray转为字符串
def get_string(byte_array):
    ref_string = str()
    for index in byte_array:
        ref_string = ref_string + "".join(str(index))
    return ref_string

# 传入汇编代码,得到对应机器码
def get_opcode_from_assemble(dbg_ptr,asm):
  pass

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 需要搜索的指令集片段
    search_asm = ['pop ecx','mov edi,edi', 'push eax', 'jmp esp']
    opcode = []

    # 将汇编指令转为机器码,放入opcode
    for index in range(len(search_asm)):
        byt = bytearray()
        byt = get_opcode_from_assemble(dbg, search_asm[index])
        opcode.append(get_string(byt))

    # 循环搜索指令集内存地址
    for index,entry in zip(range(0,len(opcode)), dbg.get_all_module()):
        eip = entry.get("entry")
        base_name = entry.get("name")
        if eip != 0:
            dbg.set_register("eip",eip)
            search_address = dbg.scan_memory_all(opcode[index])

            if search_address != False:
                print("指令: {} --> 模块: {} --> 个数: {}".format(search_asm[index],base_name,len(search_address)))

                for search_index in search_address:
                    print("[*] {}".format(hex(search_index)))
            else:
                print("a")

        time.sleep(0.3)
    dbg.close()
 ```
 
 
