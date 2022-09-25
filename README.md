# x64dbg 自动化控制插件

<br>
<div align=center>
	<img width="150" src="https://cdn.lyshark.com/archive/LyScript/lyscript_png.jpg" />
 <br><br>
  
  [简体中文](README.md) | [繁體中文(中國)](README-TC.md) | [ENGLISH](README-EN.md) | [русский язык ](README-RU.md)

  <br>
  
[![Build status](https://cdn.lyshark.com/archive/LyScript/build.svg)](https://github.com/lyshark/LyScript) [![Open Source Helpers](https://cdn.lyshark.com/archive/LyScript/users.svg)](https://github.com/lyshark/LyScript) [![Crowdin](https://cdn.lyshark.com/archive/LyScript/email.svg)](mailto:me@lyshark.com) [![Download x64dbg](https://cdn.lyshark.com/archive/LyScript/x64dbg.svg)](https://github.com/lyshark/LyScript/releases/tag/LyScript) [![OSCS Status](https://www.oscs1024.com/platform/badge/lyshark/LyScript.svg?size=small)](https://www.oscs1024.com/project/lyshark/LyScript?ref=badge_small)

[![python3](https://cdn.lyshark.com/archive/LyScript/python3.svg)](https://github.com/lyshark/LyScript) [![platform](https://cdn.lyshark.com/archive/LyScript/platform.svg)](https://github.com/lyshark/LyScript) [![lyscriptver](https://cdn.lyshark.com/archive/LyScript/lyscript_version.svg)](https://github.com/lyshark/LyScript)

<br><br>
一款 x64dbg 自动化控制插件，通过Python控制x64dbg的行为，实现远程动态调试，解决了逆向工作者分析程序，反病毒人员脱壳，漏洞分析者寻找指令片段，原生脚本不够强大的问题，通过与Python相结合利用Python语法的灵活性以及其丰富的第三方库，加速漏洞利用程序的开发，辅助漏洞挖掘以及恶意软件分析。
  
</div>
<br>

Python 包请安装与插件一致的版本，在cmd命令行下执行pip命令即可安装，推荐两个包全部安装。

 - 安装标准包：`pip install LyScript32` 或者 `pip install LyScript64`
 - 安装扩展包：`pip install LyScriptTools32` 或者 `pip install LyScriptTools64`

其次您需要手动下载对应`x64dbg`版本的驱动文件，并放入指定的`plugins`目录下。

 - 调试器下载：<a href="https://sourceforge.net/projects/x64dbg/files/snapshots/snapshot_2022-09-11_15-59.zip/download">snapshot_2022-09-11_15-59.zip</a>
 - 插件下载：<a href="https://github.com/lyshark/LyScript/raw/master/plugins/LyScript32-1.0.13.zip">LyScript32-1.0.13 (32位插件)</a> 或者 <a href="https://github.com/lyshark/LyScript/raw/master/plugins/LyScript64-1.0.13.zip">LyScript64-1.0.13 (64位插件)</a>

插件下载好以后，请将该插件复制到x64dbg的plugins目录下，程序运行后会自动加载插件。

![image](https://user-images.githubusercontent.com/52789403/185293618-68102ea6-8c37-493e-8be3-ca46eca0f0b5.png)

当插件加载成功后，会在日志位置看到具体的绑定信息以及输出调试，该插件并不会在插件栏显示。

![image](https://user-images.githubusercontent.com/52789403/161062658-0452fe0c-3e11-4df4-a83b-b026f74884d0.png)

如果需要远程调试，则只需要在初始化`MyDebug()`类时传入对端IP地址即可，如果不填写参数则默认使用`127.0.0.1`地址，请确保对端放行了`6589`端口，否则无法连接。

![image](https://user-images.githubusercontent.com/52789403/161062393-df04aabb-2d70-4434-80b9-a46974bccf8a.png)

运行x64dbg程序并手动载入需要分析的可执行文件，然后我们可以通过`connect()`方法连接到调试器，连接后会创建一个持久会话直到python脚本结束则连接会被强制断开，在此期间可调用`is_connect()`检查该链接是否还存在，具体代码如下所示。
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
<br><br>

### 寄存器系列函数

**get_register() 函数:** 该函数主要用于实现，对特定寄存器的获取操作，用户需传入需要获取的寄存器名字即可。

 - 参数1：传入寄存器字符串

可用范围："DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI","ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP", "CIP", "CSP", "CAX", "CBX", "CCX", "CDX", "CDI", "CSI", "CBP", "CFLAGS"

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
如果您使用的是64位插件，则寄存器的支持范围将变为E系列加R系列。

可用范围扩展： "DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI", "ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP", "RAX", "RBX", "RCX", "RDX", "RSI", "SIL", "RDI", "DIL", "RBP", "BPL", "RSP", "SPL", "RIP", "R8", "R8D", "R8W", "R8B", "R9", "R9D", "R9W", "R9B", "R10", "R10D", "R10W", "R10B", "R11", "R11D", "R11W", "R11B", "R12", "R12D", "R12W", "R12B", "R13", "R13D", "R13W", "R13B", "R14", "R14D", "R14W", "R14B", "R15", "R15D", "R15W", "R15B"

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

**set_register() 函数:** 该函数实现设置指定寄存器参数，同理64位将支持更多寄存器的参数修改。

 - 参数1：传入寄存器字符串
 - 参数2：十进制数值

可用范围："DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI", "ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP"

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

**get_flag_register() 函数:** 用于获取某个标志位参数，返回值只有真或者假。

 - 参数1：寄存器字符串

可用寄存器范围："ZF", "OF", "CF", "PF", "SF", "TF", "AF", "DF", "IF" 

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

**set_flag_register() 函数:** 用于设置某个标志位参数，返回值只有真或者假。
 
 - 参数1：寄存器字符串
 - 参数2：[ 设置为真 True] / [设置为假 False]

可用寄存器范围："ZF", "OF", "CF", "PF", "SF", "TF", "AF", "DF", "IF" 

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

### 调试系列函数

**set_debug() 函数:** 用于影响调试器，例如前进一次，后退一次，暂停调试，终止等。

 - 参数1: 传入需要执行的动作

可用动作范围：[暂停 Pause] [运行 Run] [步入 StepIn]  [步过 StepOut] [到结束 StepOver] [停止 Stop] [等待 Wait]

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

**set_debug_count() 函数:** 该函数是`set_debug()`函数的延续，目的是执行自动步过次数。

 - 参数1：传入需要执行的动作
 - 参数2：执行重复次数

可用动作范围：[暂停 Pause] [运行 Run] [步入 StepIn]  [步过 StepOut] [到结束 StepOver] [停止 Stop] [等待 Wait]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    dbg.set_debug_count("StepIn",10)

    dbg.close()
```

**is_debugger() /is_running()/is_run_locked() 函数:** 函数`is_debugger`可用于验证当前调试器是否处于调试状态，`is_running`则用于验证是否在运行，`is_run_locked()`用于检查调试器是否被锁定(暂停)。

- 无参数传递

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

**set_breakpoint() 函数:** 设置断点与取消断点进行了分离，设置断点只需要传入十进制内存地址。

 - 参数1：传入内存地址（十进制）
 
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

**delete_breakpoint() 函数:** 该函数传入一个内存地址，可取消一个内存断点。

 - 参数1：传入内存地址（十进制）

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

**check_breakpoint() 函数:** 用于检查下过的断点是否被命中，命中返回True否则返回False。

 - 参数1：传入内存地址（十进制）

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

**get_all_breakpoint() 函数:** 用于获取当前调试程序中，所有下过的断点信息，包括是否开启，命中次数等。

 - 无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    ref = dbg.get_all_breakpoint()
    print(ref)
    dbg.close()
```

**set_hardware_breakpoint() 函数:** 用于设置一个硬件断点，硬件断点在32位系统中最多设置4个。

 - 参数1：内存地址（十进制）
 - 参数2：断点类型

断点类型可用范围：[类型 0 = HardwareAccess / 1 = HardwareWrite / 2 = HardwareExecute]

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

**delete_hardware_breakpoint() 函数:** 用于删除一个硬件断点，只需要传入地址即可，无需传入类型。

 - 参数1：内存地址（十进制）

断点类型可用范围：[类型 0 = HardwareAccess / 1 = HardwareWrite / 2 = HardwareExecute]

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

**is_bp_disable() 函数:** 该函数用于验证指定地址处BP断点是否被禁用。

 - 参数1：内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    is_false = dbg.is_bp_disable(eip)
    print("bp断点状态: {}".format(is_false))

    dbg.close()
```

**get_xref_count_at() 函数:** 获取指定内存地址位置处交叉引用计数。

 - 参数1：内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    types = dbg.get_xref_count_at(eip)
    print("引用计数: {}".format(types))

    dbg.close()
```

**get_function_type_at() 函数:** 获取指定内存地址位置处函数类型，函数`FUNCTYPE`枚举类型。

 - 参数1：内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    types = dbg.get_function_type_at(eip)
    print("函数类型: {}".format(types))

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

**get_bpx_type_at() 函数:** 获取指定地址处BP断点类型，类型`BPXTYPE`枚举。

 - 参数1：内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    types = dbg.get_bpx_type_at(eip)
    print("BPX类型: {}".format(types))

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

**get_xref_type_at() 函数:** 得到指定内存地址位置处交叉引用类型，枚举`XREFTYPE`类型。

 - 参数1：内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    types = dbg.get_xref_type_at(eip)
    print("引用类型: {}".format(types))

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

### 模块系列函数

**get_module_base() 函数:** 该函数可用于获取程序载入的指定一个模块的基地址。

 - 参数1：模块名字符串

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    
    user32_base = dbg.get_module_base("user32.dll")
    print(user32_base)

    dbg.close()
```

**get_all_module() 函数:** 用于输出当前加载程序的所有模块信息，以字典的形式返回。

 - 参数：无参数

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

**get_local_() 系列函数:** 获取当前EIP所在模块基地址，长度，以及内存属性，此功能无参数传递，获取的是当前EIP所指向模块的数据。

 - dbg.get_local_base()    获取模块基地址
 - dbg.get_local_size()    获取模块长度
 - dbg.get_local_protect() 获取模块保护属性

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

**get_module_from_function() 函数:** 获取指定模块中指定函数的内存地址，可用于验证当前程序在内存中指定函数的虚拟地址。

 - 参数1：模块名
 - 参数2：函数名

成功返回地址，失败返回false

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

**get_module_from_import() 函数:** 获取当前程序中指定模块的导入表信息，输出为列表嵌套字典。

 - 参数1：传入模块名称

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

**get_module_from_export() 函数:** 该函数用于获取当前加载程序中的导出表信息。

 - 参数1：传入模块名

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

**get_section() 函数:** 该函数用于输出主程序中的节表信息。

 - 无参数传递

 ```Python
 from LyScript32 import MyDebug
 
if __name__ == "__main__":
    dbg = MyDebug(address="127.0.0.1",port=6666)
    connect_flag = dbg.connect()

    ref = dbg.get_section()
    print(ref)

    dbg.close()
```

**get_base_from_address() 函数:** 根据传入的内存地址得到该模块首地址。

 - 参数1：传入内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    eip = dbg.get_register("eip")

    ref = dbg.get_base_from_address(eip)
    print("模块首地址: {}".format(hex(ref)))
```

**get_base_from_name() 函数:** 根据传入的模块名得到该模块所在内存首地址。

 - 参数1：传入模块名

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

**get_oep_from_name() 函数:** 根据传入的模块名，获取该模块实际装载OEP位置。

 - 参数1：传入模块名

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    oep = dbg.get_oep_from_name("win32project.exe")
    print(hex(oep))

    dbg.close()
```

**get_oep_from_address() 函数:** 根据传入内存地址，得到该地址模块的OEP位置。

 - 参数1：传入内存地址

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

**get_section_from_module_name() 函数:** 用户可传入当前载入的模块名，即可直接取出指定模块的节表信息。

 - 参数1：模块名（字符串）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    section_user32 = dbg.get_section_from_module_name("user32.dll")
    print(section_user32)

    section_ntdll = dbg.get_section_from_module_name("ntdll.dll")
    print(section_ntdll)

    dbg.close()
```

**size_from_address() 函数:** 传入一个模块的基地址得到该模块占用总大小。

 - 参数1：模块地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    base = dbg.get_local_base()
    print("模块基地址: {}".format(hex(base)))

    size = dbg.size_from_address(base)
    print("模块长度: {}".format(size))

    dbg.close()
```

**size_from_name() 函数:** 传入模块名称得到模块占用总大小。

 - 参数1：模块名（字符串）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    size = dbg.size_from_name("win32.exe")
    print("长度: {}".format(size))

    dbg.close()
```

**section_count_from_name() 函数:** 传入模块名称得到模块有多少个节区。

 - 参数1：模块名（字符串）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    size = dbg.section_count_from_name("win32.exe")
    print("节区个数: {}".format(size))

    dbg.close()
```

**section_count_from_address() 函数:** 传入模块基址得到模块有多少个节区。

 - 参数1：模块地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    base = dbg.get_local_base()
    print("模块基地址: {}".format(hex(base)))

    size = dbg.section_count_from_address(base)
    print("节个数: {}".format(size))

    dbg.close()
```

**path_from_name() 函数:** 传入模块名称得到模块路径。

 - 参数1：模块名（字符串）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    size = dbg.path_from_name("win32.exe")
    print("模块路径: {}".format(size))

    dbg.close()
```

**path_from_address() 函数:** 传入模块地址得到模块路径。

 - 参数1：模块地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    base = dbg.get_local_base()
    print("模块基地址: {}".format(hex(base)))

    path = dbg.path_from_address(base)
    print("模块路径: {}".format(path))

    dbg.close()
```

**name_from_address() 函数:** 传入模块地址得到模块名称。

 - 参数1：模块地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    base = dbg.get_local_base()
    print("模块基地址: {}".format(hex(base)))

    path = dbg.name_from_address(base)
    print("模块名: {}".format(path))

    dbg.close()
```

**get_window_handle() 函数:** 取出自身进程模块句柄。

 - 参数：无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    base = dbg.get_window_handle()
    print("进程句柄: {}".format(base))

    dbg.close()
```

**get_module_at() 函数:** 获取指定内存地址处模块名，此处得到的模块名无后缀。

 - 参数1：模块地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    ref = dbg.get_module_at(eip)
    print("模块名: {}".format(ref))

    dbg.close()
```

**get_local_module() 函数:** 该系列函数可用于得到当前载入程序停留EIP位置的模块详细信息。

 - get_local_module_size() 获取当前程序的大小
 - get_local_module_section_Count() 获取自身节数量
 - get_local_module_path() 获取被调试程序完整路径
 - get_local_module_name() 获取自身模块名
 - get_local_module_entry() 获取自身模块入口
 - get_local_module_base() 获取自身模块基地址

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    print("程序大小: {}".format( dbg.get_local_module_size()))
    print("节个数: {}".format(dbg.get_local_module_section_Count()))
    print("完整路径: {}".format(dbg.get_local_module_path()))
    print("模块名: {}".format(dbg.get_local_module_name()))
    print("模块入口: {}".format(dbg.get_local_module_entry()))
    print("模块基地址: {}".format(dbg.get_local_module_base()))

    dbg.close()
```
<br>

### 内存系列函数

**read_memory_() 系列函数:** 读内存系列函数，包括 ReadByte,ReadWord,ReadDword 三种格式，在64位下才支持Qword

 - 参数1：需要读取的内存地址（十进制）

目前支持：
 - read_memory_byte() 读字节
 - read_memory_word() 读word
 - read_memory_dword() 读dword
 - read_memory_qword() 读qword （仅支持64位）
 - read_memory_ptr() 读指针

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

**write_memory_() 系列函数:** 写内存系列函数，WriteByte,WriteWord,WriteDWORD,WriteQword

 - 参数1：需要写入的内存
 - 参数2：需要写入的byte字节

目前支持：
 - write_memory_byte() 写字节
 - write_memory_word() 写word
 - write_memory_dword() 写dword
 - write_memory_qword() 写qword （仅支持64位）
 - write_memory_ptr() 写指针

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

**scan_memory_one() 函数:** 实现了内存扫描，当扫描到第一个符合条件的特征时，自动输出。

 - 参数1：特征码字段

 这个函数需要注意，如果我们的x64dbg工具停在系统领空，则会默认搜索系统领空下的特征，如果想要搜索程序领空里面的数据，需要先将EIP切过去在操作。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    ref = dbg.scan_memory_one("ff 25")
    print(ref)
    dbg.close()
```

**scan_memory_all() 函数:** 实现了扫描所有符合条件的特征字段，找到后返回一个列表。

 - 参数1：特征码字段

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

**scan_memory_any() 函数:** 该函数可实现对特定位置，向下扫描特定长度的特征字段。

 - 参数1：扫描起始地址（十进制）
 - 参数2：扫描长度（十进制）
 - 参数3：特征码字段

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    # 初始化
    dbg = MyDebug()

    # 连接到调试器
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 任意地址扫描
    eip = dbg.get_register("eip")
    ref = dbg.scan_memory_any(eip,1024,"8b 50 04 8b fe")
    print("得到扫描结果: {}".format(hex(ref)))

    dbg.close()
```

**get_local_protect() 函数:** 获取内存属性传值，该函数进行更新，取消了只能得到EIP所指的位置的内存属性，用户可随意检测。

 - 参数1：内存地址（十进制）

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

**set_local_protect() 函数:** 新增设置内存属性函数，传入eip内存地址，设置属性32，以及设置内存长度1024即可。

 - 参数1：内存地址（十进制）
 - 参数2：权限类型（32=执行/读取 30=执行 2=读取/写入）
 - 参数3：属性长度（十进制）

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

**get_local_page_size() 函数:** 用于获取当前EIP所指领空下，内存pagesize分页大小。

 - 无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    size = dbg.get_local_page_size()
    print("pagesize = {}".format(size))

    dbg.close()
```

**get_memory_section() 函数:** 该函数主要用于获取内存映像中，当前调试程序的内存节表数据。

 - 无参数传递
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_memory_section()
    print(ref)
    dbg.close()
```

**is_jmp_going_to_execute() 函数:** 判断内存地址是否跳转到可执行内存块。

 - 参数1：内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    flag = dbg.is_jmp_going_to_execute(eip)
    print("是否是跳转(是否可执行): {}".format(flag))

    dbg.close()
```

**mem_find_base_addr() 函数:** 返回特定位置处内存模块基地址和大小，以字典形式返回。

 - 参数1：内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    dic = dbg.mem_find_base_addr(eip)

    print("内存基地址: {}".format(hex(dic.get("base"))))
    print("内存大小: {}".format(dic.get("size")))

    dbg.close()
```

**mem_get_page_size() 函数:** 得到指定位置处内存页面长度。

 - 参数1：内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    addr = dbg.mem_get_page_size(eip)

    print("内存页面长度: {}".format(hex(addr)))

    dbg.close()
```

**mem_is_valid() 函数:** 验证指定位置处内存地址是否可读取。

 - 参数1：内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    is_read = dbg.mem_is_valid(eip)
    print("内存地址属性: {}".format(is_read))

    dbg.close()
```
<br>

### 堆栈系列函数

**create_alloc() 函数：** 函数`create_alloc()`可在远程开辟一段堆空间，成功返回内存首地址。

 - 参数1：开辟的堆长度（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.create_alloc(1024)
    print("开辟地址: ", hex(ref))

    dbg.close()
```

**delete_alloc() 函数：** 函数`delete_alloc()`用于注销一个远程堆空间。

 - 参数1：传入需要删除的堆空间内存地址。

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

**push_stack() 函数:** 将一个十进制数压入堆栈中，默认在堆栈栈顶。

 - 参数1：十进制数据

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.push_stack(10)

    print(ref)

    dbg.close()
```

**pop_stack() 函数:** pop函数用于从堆栈中推出一个元素，默认从栈顶弹出。

 - 无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    tt = dbg.pop_stack()
    print(tt)

    dbg.close()
```

**peek_stack() 函数:** peek则用于检查堆栈内的参数，可设置偏移值，不设置则默认检查第一个也就是栈顶。

 - 参数1：十进制偏移

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

### 进程线程系列函数

**get_thread_list() 函数:** 该函数可输出当前进程所有在运行的线程信息。

 - 无参数传递

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

**get_process_handle() 函数:** 用于获取当前进程句柄信息。

 - 无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_process_handle()
    print(ref)

    dbg.close()
```

**get_process_id() 函数:** 用于获取当前加载程序的PID

 - 无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_process_id()
    print(ref)

    dbg.close()
```

**get_teb_address() / get_peb_address() 系列函数:** 用于获取当前进程环境块，和线程环境快。

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

### 反汇编系列函数

**get_disasm_code() 函数:** 该函数主要用于对特定内存地址进行反汇编，传入两个参数。

 - 参数1：需要反汇编的地址(十进制) 
 - 参数2：需要向下反汇编的长度

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

**get_disasm_one_code() 函数:** 在用户指定的位置读入一条汇编指令，用户可根据需要对其进行判断。
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

**get_disasm_operand_code() 函数:** 用于获取汇编指令中的操作数，例如`jmp 0x0401000`其操作数就是`0x0401000`。

 - 参数1：传入内存地址（十进制）

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

**get_disasm_operand_size() 函数:** 用于得当前内存地址下汇编代码的机器码长度。

 - 参数1：传入内存地址（十进制）

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

**assemble_write_memory() 函数:** 实现了用户传入一段正确的汇编指令，程序自动将该指令转为机器码，并写入到指定位置。

 - 参数1：写出内存地址（十进制）
 - 参数2：写出汇编指令

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

**assemble_code_size() 函数:** 该函数实现了用户传入一个汇编指令，自动计算出该指令占多少个字节。

 - 参数1：汇编指令字符串

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.assemble_code_size("sub esp, 0x324")
    print(ref)

    dbg.close()
```

**get_branch_destination() 函数:** 获取call或者是jx跳转指令的跳转地址。

 - 参数1：获取内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    print("当前EIP地址: {}".format(hex(eip)))

    value = dbg.get_branch_destination(eip)
    print("操作数: {}".format(hex(value)))

    dbg.close()
```

**get_disassembly() 函数:** 反汇编一条指令，此函数直接输出调试其中看到的，包括符号。

 - 参数1：获取内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    print("当前EIP地址: {}".format(hex(eip)))

    dasm = dbg.get_disassembly(eip)
    print("反汇编一条: {}".format(dasm))

    dbg.close()
```

**assemble_at() 函数:** 汇编系列函数，传入一条汇编指令，直接将指令写出到内存。

 - 参数1：获取内存地址（十进制）
 - 参数2：汇编指令（字符串）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    print("当前EIP地址: {}".format(hex(eip)))

    ref = dbg.assemble_at(eip,"nop")
    print("写出状态: {}".format(ref))

    dbg.close()
```

**disasm_fast_at() 函数:** 该函数同样是反汇编一行并返回字典，但它可以获取到更多有效参数。

 - 参数1：获取内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    print("当前EIP地址: {}".format(hex(eip)))

    dasm = dbg.disasm_fast_at(eip)
    print("地址: {}".format(hex(dasm.get("addr"))))
    print("汇编指令: {}".format(dasm.get("disasm")))
    print("汇编长度: {}".format(dasm.get("size")))
    print("是否分支: {}".format(dasm.get("is_branch")))
    print("是否call: {}".format(dasm.get("is_call")))
    print("类型: {}".format(dasm.get("type")))

    dbg.close()
```
<br>

### 其他系列函数

**set_comment_notes() 函数:** 给指定位置代码增加一段注释，如下演示在eip位置增加注释。

 - 参数1：注释内存地址
 - 参数2：注释内容

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

**run_command_exec() 函数:** 执行内置命令，例如bp,dump等。

 - 参数1：命令语句

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.run_command_exec("bp MessageBoxA")
    print(ref)

    dbg.close()
```

**set_loger_output() 函数:** 日志的输出尤为重要，该模块提供了自定义日志输出功能，可将指定日志输出到x64dbg日志位置。

 - 参数1：日志内容

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

**run_command_exe_ref() 函数:** 该函数是`run_command_exec()`的延申，其主要增加了传出参数的功能，目前可传出整数类型。

 - 参数1：命令语句

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    ref = dbg.run_command_exe_ref("mod.base(eip)")
    print("返回参数: {}".format(hex(ref)))

    dbg.close()
```

**set_status_bar_message() 函数:** 该函数可实现在x64dbg底部状态栏上面输出一个用户传入的字符串。

 - 参数1：输出字符串
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    dbg.set_status_bar_message("EIP => {}".format(hex(eip)))

    dbg.close()
```

**script_loader() 函数:** 该函数接收用户传入的内置脚本所在路径，并将该脚本加载到x64dbg中。

 - 参数1：脚本路径

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    flag = dbg.script_loader("d://x64dbg_script.txt")
    print("返回值: {}".format(flag))

    dbg.close()
```

**script_unloader() 函数:** 该函数用于关闭x64dbg中打开的脚本。

 - 参数：无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    flag = dbg.script_loader("d://x64dbg_script.txt")
    print("返回值: {}".format(flag))
    
    dbg.script_unloader()

    dbg.close()
```

**script_run() 函数:** 该函数用于运行一个已经载入到x64dbg中的脚本。

 - 参数1：运行条数(可空)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    flag = dbg.script_loader("d://x64dbg_script.txt")
    print("返回值: {}".format(flag))

    dbg.script_run()

    dbg.close()
```

**script_set_ip() 函数:** 该函数用于指定从第几行开始运行脚本。

 - 参数1：运行下标

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    flag = dbg.script_loader("d://x64dbg_script.txt")
    print("返回值: {}".format(flag))

    dbg.script_set_ip(3)

    dbg.close()
```

**open_debug() 函数:** 该函数用于打开磁盘中的一个被调试程序。

 - 参数1：被打开程序完整路径

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    flag = dbg.open_debug("d://win32.exe")

    dbg.close()
```

**close_debug() 函数:** 该函数用于关闭当前打开的调试程序，之关闭程序不关闭调试器。

 - 参数：无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    flag = dbg.open_debug("d://win32.exe")
    
    if flag == True:
        dbg.close_debug()
    
    dbg.close()
```

**detach_debug() 函数:** 该函数用于让调试器脱离进程，进程会被运行起来。

 - 参数：无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    flag = dbg.open_debug("d://win32.exe")

    if flag == True:
        dbg.detach_debug()

    dbg.close()
```

**message_box() 函数:** 此功能提供了三种对话框，一种可输入文本，一种判断是否选中，另一种则是普通弹窗。

 - 参数1：弹出的提示信息

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    conn = dbg.connect()

    # 弹出输入框
    flag = dbg.input_string_box("请输入反汇编入口地址?")
    print("用户的输入: {}".format(flag))

    # 弹出是否框
    flag = dbg.message_box_yes_no("是否继续执行脱壳操作?")
    if flag == True:
        print("脱壳")
    else:
        print("退出")

    # 提示框
    flag = dbg.message_box("这是第 {} 次,异常了".format(1))
    print("状态: {}".format(flag))

    dbg.close()
```

**set_argument_brackets() 函数:** 该函数可在`注释`处增加括号。

 - 参数1：开始位置（十进制）
 - 参数2：结束位置（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    ref = dbg.set_argument_brackets(eip, eip +100)
    print("是否增加注释: {}".format(ref))
    
    dbg.close()
```

**del_argument_brackets() 函数:** 该函数可清除通过`set_argument_brackets`设置的括号。

 - 参数1：开始位置（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    
    dbg.del_argument_brackets(eip)

    dbg.close()
```

**set_function_brackets() 函数:** 该函数可实现在`机器码`位置增加括号。

 - 参数1：开始位置（十进制）
 - 参数2：结束位置（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    flag = dbg.set_function_brackets(eip,eip+10)

    dbg.close()
```

**del_function_brackets() 函数:** 该函数可清除通过`del_function_brackets`设置的括号。

 - 参数1：开始位置（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    
    dbg.del_function_brackets(eip)

    dbg.close()
```

**set_loop_brackets() 函数:** 该函数可实现在`反汇编`位置增加括号。

 - 参数1：开始位置（十进制）
 - 参数2：结束位置（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    ref = dbg.set_loop_brackets(eip,eip + 10)
    print("设置状态: {}".format(ref))

    dbg.close()
```

**del_loop_brackets() 函数:** 该函数可清除通过`set_loop_brackets`设置的括号。

 - 参数1：清除层级（默认1）
 - 参数2：开始位置（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    ref = dbg.del_loop_brackets(1,eip)
    print("清除状态: {}".format(ref))

    dbg.close()
```

**set_label_at() 函数:** 该函数可在特定位置设置一个标签。

 - 参数1：设置标签的地址（十进制）
 - 参数2：标签名（字符串）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    
    dbg.set_label_at(eip,"test1")
    dbg.set_label_at(eip+10,"test2")

    dbg.close()
```

**location_label_at() 函数:** 该函数可通过已有的标签定位到所在位置，并返回内存地址。

 - 参数1：标签名（字符串）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")
    
    lab_addr = dbg.location_label_at("test2")
    print("标签所在内存: {}".format(hex(lab_addr)))

    dbg.close()
```

**clear_label() 函数:** 该函数用于清除当前程序内所有的标签。

 - 参数：无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    ref = dbg.clear_label()

    dbg.close()
```

**update_all_view() 函数:** 刷新试图函数，与切换CPU位置。

 - 参数：无参数传递
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 刷新试图
    dbg.update_all_view()
    
    # 切换到CPU窗口
    dbg.switch_cpu()
    
    # 清除所有日志
    dbg.clear_log()

    dbg.close()
```
<br>

### Script 脚本类

脚本类的功能实现都是调用的x64dbg命令，目前由于`run_command_exec()`命令无法返回参数，故通过中转eax寄存器实现了取值，目前只能取出整数类型的参数。

脚本类功能说明来源于 <a href="https://www.cnblogs.com/iBinary/p/16359195.html">iBinary</a> 的博客

|  Script 类内函数名   | 函数作用  |
|  ----  | ----  |
| party(addr) | 获取模块的模式编号, addr = 0则是用户模块,1则是系统模块 |
| base(addr) | 获取模块基址 |
| size(addr) | 返回模块大小 |
| hash(addr) | 返回模块hash |
| entry(addr) | 返回模块入口 |
| system(addr) | 如果addr是系统模块则为true否则则是false |
| user(addr) | 如果是用户模块则返回true 否则为false |
| main() | 返回主模块基地址 |
| rva(addr) | 如果addr不在模块则返回0,否则返回addr所位于模块的RVA偏移 |
| offset(addr) | 获取地址所对应的文件偏移量,如果不在模块则返回0 |
| isexport(addr) | 判断该地址是否是从模块导出的函数 |
| valid(addr) | 判断addr是否有效,有效则返回True |
| base(addr) | 或者当前addr的基址 |
| size(addr) | 获取当前addr内存的大小 |
| iscode(addr) | 判断当前 addr是否是可执行页面,成功返回TRUE |
| decodepointer(ptr) | 解密指针,相当于调用了DecodePointer ptr |
| ReadByte(addr/eg)| 从addr或者寄存器中读取一个字节内存并且返回 |
| Byte(addr) | 从addr或者寄存器中读取一个字节内存并且返回 |
| ReadWord(addr) | 读取两个字节 |
| ReadDDword(addr) | 读取四个字节 |
| ReadQword(addr) | 读取8个字节,但是只能是64位程序方可使用 |
| ReadPtr(addr) | 从地址中读取指针(4/8字节)并返回读取的指针值 |
| ReadPointer(addr) | 从地址中读取指针(4/8字节)并返回读取的指针值 |
| len(addr) | 获取addr处的指令长度 |
| iscond(addr) | 判断当前addr位置是否是条件指令 |
| isbranch(addr) | 判断当前地址是否是分支指令 |
| isret(addr) | 判断是否是ret指令 |
| iscall(addr) | 判断是否是call指令 |
| ismem(addr) | 判断是否是内存操作数 |
| isnop(addr) | 判断是否是nop |
| isunusual(addr) | 判断当前地址是否指示为异常地址 |
| branchdest(addr) | 将指令的分支目标位于addr处 |
| branchexec(addr) | 如果分支要执行 |
| imm(addr) | 获取当前指令位置的立即数 |
| brtrue(addr) | 下一条指令的地址 |
| next(addr) | 获取addr的下一条地址 |
| prev(addr) | 获取addr上一条低地址 |
| iscallsystem(addr) | 判断当前指令是否是系统模块指令 |
| get(index) | 获取当前函数堆栈中的第index个参数 |
| set(index,value) | 设置的索引位置的值 |
| firstchance() | 最后一个异常是否为第一次机会异常 |
| addr() | 最后一个异常地址 |
| code() | 最后一个异常代码 |
| flags() | 最后一个异常标志 |
| infocount() | 上次异常信息计数 |
| info(index) | 最后一个异常信息 |

如上是一些常用的脚本命令的封装，他们的调用方式如下面代码中所示。
```Python
from LyScript32 import MyDebug
from LyScriptTools32 import DebugControl
from LyScriptTools32 import Script

# 有符号整数转无符号数
def long_to_ulong(inter, is_64=False):
    if is_64 == False:
        return inter & ((1 << 32) - 1)
    else:
        return inter & ((1 << 64) - 1)

# 无符号整数转有符号数
def ulong_to_long(inter, is_64=False):
    if is_64 == False:
        return (inter & ((1 << 31) - 1)) - (inter & (1 << 31))
    else:
        return (inter & ((1 << 63) - 1)) - (inter & (1 << 63))

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 定义调试类与脚本类
    control = DebugControl(dbg)
    script = Script(dbg)

    # 得到EIP
    eip = control.get_eip()

    size = script.size(eip)
    print("当前模块大小: {}".format(hex(size)))

    entry = script.entry(eip)
    print("当前模块入口: {}".format(hex(entry)))

    # 得到hash值,默认有符号需要转换
    hash = script.hash(eip)
    print("有符号hash值: {}".format(hash))

    hash = long_to_ulong(script.hash(eip))
    print("无符号hash值: {}".format(hex(hash)))

    dbg.close()
```
如果觉得上面的函数封装不够，或自己需要调用特定命令，那么可以直接调用该类内的`script.GetScriptValue("")`方法，自定义一个参数传递，目前只能接受返回值是整数的命令。
```Python
from LyScript32 import MyDebug
from LyScriptTools32 import DebugControl
from LyScriptTools32 import Script

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 定义控制类与脚本类
    control = DebugControl(dbg)
    script = Script(dbg)

    # 得到EIP
    eip = control.get_eip()

    # 调用脚本命令执行函数
    ref = script.GetScriptValue("mod.size(eip)")
    print("模块返回值: {}".format(hex(ref)))

    dbg.close()
```
<br>

### Stack 堆栈类

Stack 类是通过二次封装stack堆栈操作API函数得到的，并在此基础上增加了全新的调用函数。

|  Stack 类内函数名   | 函数作用  |
|  ----  | ----  |
| create_alloc(decimal_size=1024) | 开辟堆,传入长度,默认1024字节 |
| delete_alloc(decimal_address=0) | 销毁一个远程堆 |
| push_stack(decimal_value=0) | 将传入参数入栈 |
| pop_stack() | 从栈顶弹出元素,默认检查栈顶,可传入参数 |
| peek_stack(decimal_index=0) | 检查指定位置栈针中的地址,返回一个地址 |
| peek_stack_list(decimal_count=0) | 检查指定位置处前index个栈针中的地址,返回一个地址列表 |
| get_current_stack_top() | 获取当前栈帧顶部内存地址 |
| get_current_stack_bottom() | 获取当前栈帧底部内存地址 |
| get_current_stackframe_size() | 获取当前栈帧长度 |
| get_stack_frame_list(decimal_count=0) | 获取index指定的栈帧内存地址,返回列表 |
| get_current_stack_disassemble() | 堆当前栈地址反汇编 |
| get_current_stack_frame_disassemble() | 对当前栈帧地址反汇编 |
| get_current_stack_base() | 得到当前栈地址的基地址 |
| get_current_stack_return_name() | 得到当前栈地址返回到的模块名 |
| get_current_stack_return_size() | 得到当前栈地址返回到的模块大小 |
| get_current_stack_return_entry() | 得到当前栈地址返回到的模块入口 |
| get_current_stack_return_base() | 得到当前栈地址返回到的模块基地址 |

我们以输出当前堆栈中模块地址为例，演示堆栈类如何使用。
```Python
from LyScript32 import MyDebug
from LyScriptTools32 import Stack
from LyScriptTools32 import DebugControl

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 定义堆栈类
    control = DebugControl(dbg)
    stack = Stack(dbg)

    # 得到EIP
    eip = control.get_eip()

    return_name = stack.get_current_stack_return_name()
    print("堆栈返回到: {}".format(return_name))

    return_size = stack.get_current_stack_return_size()
    print("堆栈返回大小: {}".format(return_size))

    return_entry = stack.get_current_stack_return_entry()
    print("堆栈返回模块的入口: {}".format(hex(return_entry)))

    return_base = stack.get_current_stack_return_base()
    print("堆栈返回模块入口基地址: {}".format(hex(return_base)))

    dbg.close()
```
<br>

### Module 模块类

Module 类主要封装自Module系列函数，在提供了标准函数的同时还提供了更多。

|  Module 类内函数名   | 函数作用  |
|  ----  | ----  |
| get_local_full_path() | 得到程序自身完整路径 |
| get_local_program_name() | 获得加载程序的文件名 |
| get_local_program_size() | 得到被加载程序的大小 |
| get_local_program_base() | 得到基地址 |
| get_local_program_entry() | 得到入口地址 |
| check_module_imported(module_name) | 验证程序是否导入了指定模块 |
| get_name_from_module(address) | 根据基地址得到模块名 |
| get_base_from_module(module_name) | 根据模块名得到基地址 |
| get_oep_from_module(module_name) | 根据模块名得到模块OEP入口 |
| get_all_module_information() | 得到所有模块信息 |
| get_module_base(module_name) | 得到特定模块基地址 |
| get_local_base() | 得到当前OEP位置处模块基地址 |
| get_local_size() | 获取当前OEP位置长度 |
| get_local_protect() | 获取当前OEP位置保护属性 |
| get_module_from_function(module,function) | 获取指定模块中指定函数内存地址 |
| get_base_from_address(address) | 根据传入地址得到模块首地址,开头4D 5A |
| get_base_address() | 得到当前.text节基地址 |
| get_base_from_name(module_name) | 根据名字得到模块基地址 |
| get_oep_from_name(module_name) | 传入模块名得到OEP位置 |
| get_oep_from_address(address) | 传入模块地址得到OEP位置 |
| get_module_from_import(module_name)| 得到指定模块的导入表 |
| get_import_inside_function(module_name,function_name) | 检查指定模块内是否存在特定导入函数 |
| get_import_iatva(module_name,function_name) | 根据导入函数名得到函数iat_va地址 |
| get_import_iatrva(module_name,function_name) | 根据导入函数名得到函数iat_rva地址 |
| get_module_from_export(module_name) | 传入模块名,获取模块导出表 |
| get_module_export_va(module_name,function_name) | 传入模块名以及导出函数名,得到va地址 |
| get_module_export_rva(module_name,function_name) | 传入模块名以及导出函数,得到rva地址 |
| get_local_section() | 得到程序节表信息 |
| get_local_address_from_section(section_name) | 根据节名称得到地址 |
| get_local_size_from_section(section_name) | 根据节名称得到节大小 |
| get_local_section_from_address(address)| 根据地址得到节名称 |

此处只提供一个演示案例，获取当前被调试进程详细参数，包括路径，名称，入口地址，基地址，长度等。
```Python
from LyScript32 import MyDebug
from LyScriptTools32 import Module

if __name__ == "__main__":
    # 初始化
    dbg = MyDebug()

    # 连接到调试器
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 类定义,并传入调试器对象
    module = Module(dbg)

    # 得到当前被调试程序完整路径
    full_path = module.get_local_full_path()
    print("完整路径: {}".format(full_path))

    # 得到进程名字
    local_name = module.get_local_program_name()
    print("调试名称: {}".format(local_name))
  
    # 验证是否导入了user32.dll
    is_import = module.check_module_imported("user32.dll")
    print("是否导入: {}".format(is_import))

    # 根据模块名得到基地址
    module_base = module.get_base_from_module("kernelbase.dll")
    print("根据模块名得到基地址: {}".format(hex(module_base)))

    dbg.close()
```
<br>

### Memory 内存类

内存操作类是对内存操作函数与断点系列函数，二次封装而成，新增了新方法可供用户使用。

| Memory 类内函数名 | 函数作用 |
| ---- | ---- |
| read_memory_byte(decimal_int=0) | 读取内存byte字节类型 |
| read_memory_word(decimal_int=0) | 读取内存word字类型 |
| read_memory_dword(decimal_int=0) | 读取内存dword双字类型 |
| read_memory_ptr(decimal_int=0) | 读取内存ptr指针 |
| read_memory(decimal_int=0,decimal_length=0) | 读取内存任意字节数,返回列表格式,错误则返回空列表 |
| write_memory_byte(decimal_address=0, decimal_int=0) | 写内存byte字节类型 |
| write_memory_word(decimal_address=0, decimal_int=0) | 写内存word字类型 |
| write_memory_dword(decimal_address=0, decimal_int=0) | 写内存dword双字类型 |
| write_memory_ptr(decimal_address=0, decimal_int=0) | 写内存ptr指针类型 |
| write_memory(decimal_address=0, decimal_list = \[\]) | 写内存任意字节数,传入十进制列表格式 |
| scan_local_memory_one(search_opcode="") | 扫描当前EIP所指向模块处的特征码 (传入参数 ff 25 ??) |
| scan_local_memory_all(search_opcode="") | 扫描当前EIP所指向模块处的特征码,以列表形式反回全部 |
| scan_memory_all_from_module(module_name="", search_opcode="") | 扫描特定模块中的特征码,以列表形式反汇所有 |
| scan_memory_one_from_module(module_name="", search_opcode="") | 扫描特定模块中的特征码,返回第一条 |
| scanall_memory_module_one(search_opcode="") | 扫描所有模块,找到了以列表形式返回模块名称与地址 |
| get_local_protect() | 获取EIP所在位置处的内存属性值 |
| get_memory_protect(decimal_address=0) | 获取指定位置处内存属性值 |
| set_local_protect(decimal_address=0,decimal_attribute=32,decimal_size=0) | 设置指定位置保护属性值 ER执行/读取=32 |
| get_local_page_size() | 获取当前页面长度 |
| get_memory_section() | 得到内存中的节表 |
| memory_xchage(memory_ptr_x=0, memory_ptr_y=0, bytes=0) | 交换两个内存区域 |
| memory_cmp(dbg,memory_ptr_x=0,memory_ptr_y=0,bytes=0) | 对比两个内存区域 |
| set_breakpoint(decimal_address=0) | 设置内存断点,传入十进制 |
| delete_breakpoint(decimal_address=0) | 删除内存断点 |
| check_breakpoint(decimal_address=0) | 检查内存断点是否命中 |
| get_all_breakpoint() | 获取所有内存断点 |
| set_hardware_breakpoint(decimal_address=0, decimal_type=0) | 设置硬件断点 [类型 0 = r / 1 = w / 2 = e] |
| delete_hardware_breakpoint(decimal_address=0) | 删除硬件断点 |

我们以扫描当前程序中所有符合特定特征条件的代码为例说明使用方法。
```Python
from LyScript32 import MyDebug
from LyScriptTools32 import Memory

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eip = dbg.get_register("eip")

    # 定义内存类
    memory = Memory(dbg)

    # 扫描整个模块中包含特征的地址
    ref = memory.scanall_memory_module_one("ff 25 ??")
    print("输出列表: {}".format(ref))

    dbg.close()
```
<br>

### Disassemble 反汇编类

Disassemble 反汇编类增加了新的API函数的让用户有更多选择，需要注意API定义中，地址后面带有0的说明其可以省略参数，缺省值默认取当前EIP位置。

|  Disassemble 类内函数名   | 函数作用  |
|  ----  | ----  |
| is_call(address=0) | 是否是跳转指令 |
| is_jmp(address=0) | 是否是jmp |
| is_ret(address=0) | 是否是ret |
| is_nop(address=0 )| 是否是nop |
| is_cond(address=0)| 是否是条件跳转指令|
| is_cmp(address=0) | 是否cmp比较指令 |
| is_test(address=0 ) | 是否是test比较指令 |
| is_(address,cond) | 自定义判断条件 |
| get_assembly(address=0) | 得到指定位置汇编指令,不填写默认获取EIP位置处 |
| get_opcode(address=0) | 得到指定位置机器码 |
| get_disasm_operand_size(address=0) | 获取反汇编代码长度 |
| assemble_code_size(assemble) | 计算用户传入汇编指令长度 |
| get_assemble_code(assemble) | 用户传入汇编指令返回机器码 |
| write_assemble(address,assemble) | 将汇编指令写出到指定内存位置 |
| get_disasm_code(address,size) | 反汇编指定行数 |
| get_disasm_one_code(address = 0)| 向下反汇编一行 |
| get_disasm_operand_code(address=0) | 得到当前内存地址反汇编代码的操作数 |
| get_disasm_next(eip) | 获取当前EIP指令的下一条指令 |
| get_disasm_prev(eip) | 获取当前EIP指令的上一条指令 |

我们来举一个使用案例，其实和模块调用原理是一样的，调用时先初始化，然后就可以使用内部的函数了。
```Python
from LyScript32 import MyDebug
from LyScriptTools32 import Module
from LyScriptTools32 import Disassemble

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 反汇编类
    dasm = Disassemble(dbg)

    # 无参数使用
    ref = dasm.is_jmp()
    print("是否是JMP: {}".format(ref))

    # 携带参数使用
    eip = dbg.get_register("eip")
    eip_flag = dasm.is_jmp(eip)
    print("EIP位置: {}".format(eip_flag))

    dbg.close()
```
<br>

### DebugControl 调试控制类

DebugControl 调试控制类，封装自寄存器系列函数。

| debugcontrol 类内函数名   | 函数作用 |
|  ----  | ----  |
| get_eax() | 获取通用寄存器系列 |
| set_eax(decimal_value) | 设置特定寄存器中的值(十进制) |
| get_zf() | 获取标志寄存器系列 |
| set_zf(decimal_bool) | 设置标志寄存器的值(布尔型) |
| script_initdebug(path) | 传入文件路径,载入被调试程序 |
| script_closedebug() | 终止当前被调试进程 |
| script_detachdebug() | 让进程脱离当前调试器 |
| script_rundebug() | 让进程运行起来 |
| script_erun() | 释放锁并允许程序运行，忽略异常 |
| script_serun() | 释放锁并允许程序运行，跳过异常中断 |
| script_pause() | 暂停调试器运行 |
| script_stepinto() | 步进 |
| script_estepinfo() | 步进,跳过异常 |
| script_sestepinto() | 步进,跳过中断 |
| script_stepover() | 步过到结束 |
| script_stepout() | 普通步过f8 |
| script_skip() | 跳过执行 |
| script_inc(register) | 递增寄存器 |
| script_dec(register) | 递减寄存器 |
| script_add(register,decimal_int) | 对寄存器进行add运算 |
| script_sub(register,decimal_int) | 对寄存器进行sub运算 |
| script_mul(register,decimal_int) | 对寄存器进行mul乘法 |
| script_div(register,decimal_int) | 对寄存器进行div除法 |
| script_and(register,decimal_int) | 对寄存器进行and与运算 |
| script_or(register,decimal_int) | 对寄存器进行or或运算 |
| script_xor(register,decimal_int) | 对寄存器进行xor或运算 |
| script_neg(register,decimal_int) | 对寄存器参数进行neg反转 |
| script_rol(register,decimal_int) | 对寄存器进行rol循环左移 |
| script_ror(register,decimal_int) | 对寄存器进行ror循环右移 |
| script_shl(register,decimal_int) | 对寄存器进行shl逻辑左移 |
| script_shr(register,decimal_int) | 对寄存器进行shr逻辑右移 |
| script_sal(register,decimal_int) | 对寄存器进行sal算数左移 |
| script_sar(register,decimal_int) | 对寄存器进行sar算数右移 |
| script_not(register,decimal_int) | 对寄存器进行not按位取反 |
| script_bswap(register,decimal_int) | 进行字节交换也就是反转 |
| script_push(register_or_value) | 对寄存器入栈 |
| script_pop(register_or_value) | 对寄存器弹出元素 |
| pause() | 内置api暂停 |
| run() | 内置api运行 |
| stepin() | 内置api步入 |
| stepout() | 内置api步过 |
| stepout() | 内置api到结束 |
| stop() | 内置api停止 |
| wait() | 内置api等待 |
| is_debug() | 内置api判断调试器是否在调试 |
| is_running() | 内置api判断调试器是否在运行 |

自动控制类主要功能如上表示，其中Script开头的API是调用的脚本命令实现，其他的是API实现，我们以批量自动载入程序为例，演示该类内函数是如何使用的。
```Python
import os
import pefile
import time
from LyScript32 import MyDebug
from LyScriptTools32 import Module
from LyScriptTools32 import Disassemble
from LyScriptTools32 import DebugControl

# 得到特定目录下的所有文件,并返回列表
def GetFullFilePaht(path):
    ref = []
    for root,dirs,files in os.walk(str(path)):
        for index in range(0,len(files)):
            ref.append(str(root + "/" + files[index]))
    return ref

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 初始化调试控制器
    debug = DebugControl(dbg)

    # 得到特定目录下的所有文件
    full_path = GetFullFilePaht("d://test/")

    for i in range(0,len(full_path)):
        debug.Script_InitDebug(str(full_path[i]))
        time.sleep(0.3)
        debug.Script_RunDebug()

        time.sleep(0.3)
        local_base = dbg.get_local_base()
        print("当前调试进程: {} 基地址: {}".format(full_path[i],local_base))

        time.sleep(0.3)
        # 关闭调试
        debug.Script_CloseDebug()

    dbg.close()
```
<br>

### LyPeUtils 工具包

该工具包用于辅助实现文件内PE结构的解析转换。

 - 安装工具包: `pip install LyPeUtils`

| 函数名 | 函数作用 |
| ---- | ---- |
| get_memory_base() | 得到自身程序基址 |
| get_memory_size() | 得到自身程序大小 |
| init_pe_module() |  设置模块,如果为空则设置自身 |
| get_file_oep_va() | 得到文件OEP位置 |
| get_memory_oep_va() | 得到内存OEP位置 |
| get_offset_from_va(va_address) | 传入一个VA值获取到FOA文件地址 |
| get_va_from_foa(foa_address)  | 传入一个FOA文件地址得到VA虚拟地址 |
| get_rva_from_foa(foa_address) | 传入一个FOA文件地址转为RVA地址 |
| get_file_section() | 获取文件节表 |
| get_memory_section() |获取内存节表 |
| get_memory_addr_from_section(section_name) | 获取内存特定节内节表 |
| get_file_section_count() |得到文件节表数量 |
| get_section_name_all() | 得到当前所有节名称 |
|  get_hash_from_section(section_name)|得到特定节内存hash |
| get_va_from_section(section_name) |得到特定节对应到虚拟内存中的地址 |
| get_file_import() |  获取文件内导入表|
| get_memory_import() | 获取内存内导入表 |

这里给出简单的使用案例，如下所示用户传入文件偏移，得到对应到内存中的VA地址。
```Python
from LyScript32 import MyDebug
from LyPeUtils import PE

if __name__ == "__main__":
    dbg = MyDebug()
    connect = dbg.connect()

    # 初始化PE
    pe = PE(dbg)

    # 初始化模块,默认设置主进程
    flag = pe.init_pe_module()

    va = pe.get_va_from_foa(0x123)
    print("文件偏移转为VA是: {}".format(hex(va)))

    dbg.close()
```
<br>

### LyScriptUtils 工具包

进制转换工具包，用于辅助`LyScript`插件实现进制与字符串或字节序列的快速转换，协助逆向工作者更好的反汇编，工具包默认支持32位与64位环境。

 - 安装进制转换工具包: `pip install LyScriptUtils`

将一个特定字节切割成等量的字节数组
```Python
from LyScript32 import MyDebug
from LyScriptUtils import *

if __name__ == '__main__':
    # 切割32位
    # [18, 52, 86, 120]
    ref = split_int32(0x12345678)
    print(ref)

    # 切割64位
    # [0, 255, 255, 255, 18, 52, 86, 120]
    ref = split_int64(0x0FFFFFF12345678)
    print(ref)

    # 自定义切割字节数
    # [18, 52]
    ref = split_int_bits(16,0x1234)
    print(ref)
```

将一个十六进制字符串转成等量的INT类型
```Python
from LyScript32 import MyDebug
from LyScriptUtils import *

if __name__ == '__main__':
    # 0x1234
    ref = str2int16("\x12\x34\x56")
    print(hex(ref))

    # 0x12345678
    ref = str2int32("\x12\x34\x56\x78")
    print(hex(ref))

    # 0x121c5678121c5678
    ref = str2int64("\x12\x34\x56\x78\x12\x34\x56\x78")
    print(hex(ref))

    # 0x1234
    ref = nstr2halfword("\x12\x34")
    print(hex(ref))

    # 0x12345678121c567812345678121c5678
    ref = str2int_bits(128,"\x12\x34\x56\x78\x12\34\x56\x78\x12\x34\x56\x78\x12\34\x56\x78")
    print(hex(ref))
```

将一个十六进制字符串转成等量的INT类型,并反转参数
```Python
from LyScript32 import MyDebug
from LyScriptUtils import *

if __name__ == '__main__':
    # 0x3412
    ref = str2int16_swapped("\x12\x34\x56")
    print(hex(ref))

    # 0x12563412
    ref = str2int32_swapped("\x12\x34\x56\x12\x34\x56")
    print(hex(ref))

    # 0x3412563412563412
    ref = str2int64_swapped("\x12\x34\x56\x12\x34\x56\x12\x34\x56\x12\x34\x56")
    print(hex(ref))

    # 0x3412
    ref = str2int_bits_swapped(16,"\x12\x34")
    print(hex(ref))
```

将字符串转换成对等小端序或大端序的十六进制整数
```Python
from LyScript32 import MyDebug
from LyScriptUtils import *

if __name__ == '__main__':
    # 小端序
    # 0x78563412
    ref = str2littleendian("\x12\x34\x56\x78")
    print(hex(ref))

    # 0x78563412
    ref = intel_str2int("\x12\x34\x56\x78")
    print(hex(ref))

    # 0x78563412
    ref = intel_str2int("\x12\x34\x56\x78")
    print(hex(ref))

    # 大端序
    # 0x12345678
    ref = str2int32("\x12\x34\x56\x78")
    print(hex(ref))

    # 0x12345678
    ref = str2bigendian("\x12\x34\x56\x78")
    print(hex(ref))
```

将一个十六进制整数转换为字节序列
```Python
from LyScript32 import MyDebug
from LyScriptUtils import *

if __name__ == '__main__':
    ref = int2str16(0x1234)
    if ref == '\x12\x34':
        print("int2str16")

    ref = halfword2bstr(0x1234)
    if ref == '\x12\x34':
        print("int2str16")

    ref = short2bigstr(0x1234)
    if ref == '\x12\x34':
        print("int2str16")

    ref = big_short(0x1234)
    if ref == '\x12\x34':
        print("int2str16")
```

将一个十六进制整数转换为字节序列,并反转参数
```Python
from LyScript32 import MyDebug
from LyScriptUtils import *

if __name__ == '__main__':
    ref = int2str16_swapped(0x1234)
    if ref == '\x34\x12':
        print("int2str16_swapped")

    ref = halfword2istr(0x1234)
    if ref == '\x34\x12':
        print("halfword2istr")

    ref = intel_short(0x1234)
    if ref == '\x34\x12':
        print("intel_short")

    ref = intel_short(0x123445678)
    if ref == '\x78\x56':
        print("intel_short")
```

将INT类型十六进制数值,转换为str32位字节序列
```Python
from LyScript32 import MyDebug
from LyScriptUtils import *

if __name__ == '__main__':
    ref = int2str32(0x12345678)
    if ref == '\x12\x34\x56\x78':
        print("int2str32")

    ref = big_order(0x12345678)
    if ref == '\x12\x34\x56\x78':
        print("big_order")
```

将一个INT类型,转换为str32字节序列,并反转参数
```Python
from LyScript32 import MyDebug
from LyScriptUtils import *

if __name__ == '__main__':
    ref = int2str32_swapped(0x12345678)
    if ref == '\x78\x56\x34\x12':
        print("int2str32_swapped")

    ref = intel_order(0x12345678)
    if ref == '\x78\x56\x34\x12':
        print("intel_order")
```

将一个十六进制INT整数,转换成一个二进制字符串
```Python
from LyScript32 import MyDebug
from LyScriptUtils import *

if __name__ == '__main__':
    # 00010010001101000101011001111000
    ref = print_binary(0x12345678)
    if ref == '00010010001101000101011001111000':
        print(ref)

    # 0101011001111000
    ref = binary_string_short(0x12345678)
    if ref == '0101011001111000':
        print(ref)
```

针对有符号数与无符号数的类型转换函数
```Python
from LyScript32 import MyDebug
from LyScriptUtils import *

if __name__ == '__main__':
    # 无符号数转换
    if uint16(0xffff) == 0xffff:
        print("uint16")

    if uint64(0x0000000ffffffff) == 0x0000000ffffffff:
        print("uint64")

    # 有符号数转换
    if sint16(0xffff) == -1:
        print("sint16")

    if sint16(0xffff) == sint16(-1):
        print("sint16==sint16")

    if signedshort(0xffff) == -1:
        print("signedshort")

    # 有符号大整数
    if sint32(-1) == -1:
        print("sint32")

    if big2int(0x123456789) == 0x23456789:
        print("big2int")
```

将一个无符号数格式化为十六进制字符串
```Python
from LyScript32 import MyDebug
from LyScriptUtils import *

if __name__ == '__main__':
    if(uintfmt_bits(32,0x12345678)=='0x12345678'):
        print("uintfmt_bits")

    if(uintfmt_bits(16,0x1234)=='0x1234'):
        print("uintfmt_bits")

    if(uint16fmt(0x123456)=='0x3456'):
        print("uintfmt_bits")

    if(uint16fmt(-0x123456)=='0xcbaa'):
        print("uintfmt_bits")

    if(uint32fmt(0x1234)=='0x00001234'):
        print("uintfmt_bits")

    if(uint64fmt(0x12345678)=='0x0000000012345678'):
        print("uintfmt_bits")

    if(uint64fmt(-1)=='0xffffffffffffffff'):
        print("uintfmt_bits")

    if(uint8fmt(0x0f)=='0x0f'):
        print("uint8fmt")
```

将一个有符号数格式化为十六进制字符串
```Python
from LyScript32 import MyDebug
from LyScriptUtils import *

if __name__ == '__main__':
    # sint16fmt
    if(sint16fmt(0x1234)=='0x1234'):
        print("sint16fmt")

    if(sint16fmt(-0x1234)=='-0x1234'):
        print("sint16fmt")

    # sint32fmt
    if(sint32fmt(-0x1234)=='-0x00001234'):
        print("sint32fmt")

    # sint64fmt
    if(sint64fmt(-1)=='-0x0000000000000001'):
        print("sint64fmt")
```

将一个十六进制INT整数反转
```Python
from LyScript32 import MyDebug
from LyScriptUtils import *

if __name__ == '__main__':
    # 0x78563412
    if(byteswap_32(0x12345678)==0x78563412):
        print("32位反转")

    # 0x5634129078563412
    if(byteswap_64(0x1234567890123456)==0x5634129078563412):
        print("64位反转")
```

对一个字符串执行十六进制格式化输出
```Python
from LyScript32 import MyDebug
from LyScriptUtils import *

if __name__ == '__main__':
    # 十六进制格式输出
    # [0x12][0x34]
    hexpr = hexprint("".join(int2list(uint16(0x1234))[2:4]))
    print(hexpr)

    # 字节序列转换成字符串
    # [8b][ec][12][ff][8b][ec][12][ff]
    byte_string = prettyprint("\x8b\xec\x12\xff\x8b\xec\x12\xff")
    print(byte_string)

    # 字符串转换成shellcode
    # unsigned char buf[] = "\x6c\x79\x73\x68\x61\x72\x6b"; // 7 bytes
    shellcode = c_array("lyshark")
    print(shellcode)

    # dump shellcode
    dump = shellcode_dump("\x6c\x79\x73\x68\x61\x72\x6b")

    # 将字符串转为二进制数组
    # [0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1]
    ref = binary_from_string("lushark")
    print(ref)

    # 输出字符串的十六进制格式
    # [('6C 79 73 68 61 72 6B ', 'lyshark')]
    ref = hexdump("lyshark")
    print(ref)
```
<br>

## [官方API应用案例]

本人结合LyScript插件API函数实现的一些通用案例，用于演示插件内置方法是如何灵活组合运用的，其目的是让用户可以自行研究学习API函数的参数传递，并能够通过案例的学习，能够快速掌握官方API函数的使用方法与技巧。

**PEFile载入PE程序到内存:** 将PE可执行文件中的内存数据通过PEfile模块打开并读入内存，实现PE参数解析。
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
如下通过`LyScirpt`模块配合`PEFile`模块解析内存镜像中的`section`节表属性。
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
    for index in range(0,8192):
        read_byte = dbg.read_memory_byte(base + index)
        byte_array.append(read_byte)

    oPE = pefile.PE(data = byte_array)

    for section in oPE.sections:
        print("%10s %10x %10x %10x" 
	%(section.Name.decode("utf-8"), section.VirtualAddress, 
	section.Misc_VirtualSize, section.SizeOfRawData))
    dbg.close()
```

**验证PE启用的保护方式:** 验证保护方式需要通过`dbg.get_all_module()`遍历加载过的模块，并依次读入`DllCharacteristics`与操作数进行与运算得到保护方式。
```Python
from LyScript32 import MyDebug
import pefile

if __name__ == "__main__":
    # 初始化
    dbg = MyDebug()
    dbg.connect()

    # 得到所有加载过的模块
    module_list = dbg.get_all_module()

    print("-" * 100)
    print("模块名 \t\t\t 基址随机化 \t\t DEP保护 \t\t 强制完整性 \t\t SEH异常保护 \t\t")
    print("-" * 100)

    for module_index in module_list:
        print("{:15}\t\t".format(module_index.get("name")),end="")

        # 依次读入程序所载入的模块
        byte_array = bytearray()
        for index in range(0, 4096):
            read_byte = dbg.read_memory_byte(module_index.get("base") + index)
            byte_array.append(read_byte)

        oPE = pefile.PE(data=byte_array)

        # 随机基址 => hex(pe.OPTIONAL_HEADER.DllCharacteristics) & 0x40 == 0x40
        if ((oPE.OPTIONAL_HEADER.DllCharacteristics & 64) == 64):
            print("True\t\t\t",end="")
        else:
            print("False\t\t\t",end="")
        # 数据不可执行 DEP => hex(pe.OPTIONAL_HEADER.DllCharacteristics) & 0x100 == 0x100
        if ((oPE.OPTIONAL_HEADER.DllCharacteristics & 256) == 256):
            print("True\t\t\t",end="")
        else:
            print("False\t\t\t",end="")
        # 强制完整性=> hex(pe.OPTIONAL_HEADER.DllCharacteristics) & 0x80 == 0x80
        if ((oPE.OPTIONAL_HEADER.DllCharacteristics & 128) == 128):
            print("True\t\t\t",end="")
        else:
            print("False\t\t\t",end="")
        if ((oPE.OPTIONAL_HEADER.DllCharacteristics & 1024) == 1024):
            print("True\t\t\t",end="")
        else:
            print("False\t\t\t",end="")
        print()
    dbg.close()
```

**计算PE节区内存特征:** 通过循环读入节区数据，并动态计算出该节的MD5以及CRC32特征值输出。
```Python
import binascii
import hashlib
from LyScript32 import MyDebug

def crc32(data):
    return "0x{:X}".format(binascii.crc32(data) & 0xffffffff)

def md5(data):
    md5 = hashlib.md5(data)
    return md5.hexdigest()

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 循环节
    section = dbg.get_section()
    for index in section:
        # 定义字节数组
        mem_byte = bytearray()

        address = index.get("addr")
        section_name = index.get("name")
        section_size = index.get("size")

        # 读出节内的所有数据
        for item in range(0,int(section_size)):
            mem_byte.append( dbg.read_memory_byte(address + item))

        # 开始计算特征码
        md5_sum = md5(mem_byte)
        crc32_sum = crc32(mem_byte)

        print("[*] 节名: {:10s} | 节长度: {:10d} | MD5特征: {} | CRC32特征: {}"
              .format(section_name,section_size,md5_sum,crc32_sum))

    dbg.close()
```

**文件FOA与内存VA转换:** 封装实现`get_offset_from_va()`用于将VA内存虚拟地址转为FOA文件偏移地址，封装实现`get_va_from_foa()`用于将FOA文件偏移地址转为VA内存虚拟地址。
```Python
from LyScript32 import MyDebug
import pefile

# 传入一个VA值获取到FOA文件地址
def get_offset_from_va(pe_ptr, va_address):
    # 得到内存中的程序基地址
    memory_image_base = dbg.get_base_from_address(dbg.get_local_base())

    # 与VA地址相减得到内存中的RVA地址
    memory_local_rva = va_address - memory_image_base

    # 根据RVA得到文件内的FOA偏移地址
    foa = pe_ptr.get_offset_from_rva(memory_local_rva)
    return foa

# 传入一个FOA文件地址得到VA虚拟地址
def get_va_from_foa(pe_ptr, foa_address):
    # 先得到RVA相对偏移
    rva = pe_ptr.get_rva_from_offset(foa_address)

    # 得到内存中程序基地址,然后计算VA地址
    memory_image_base = dbg.get_base_from_address(dbg.get_local_base())
    va = memory_image_base + rva
    return va

# 传入一个FOA文件地址转为RVA地址
def get_rva_from_foa(pe_ptr, foa_address):
    sections = [s for s in pe_ptr.sections if s.contains_offset(foa_address)]
    if sections:
        section = sections[0]
        return (foa_address - section.PointerToRawData) + section.VirtualAddress
    else:
        return 0

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 载入文件PE
    pe = pefile.PE(name=dbg.get_local_module_path())

    # 读取文件中的地址
    rva = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    va = pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.AddressOfEntryPoint
    foa = pe.get_offset_from_rva(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    print("文件VA地址: {} 文件FOA地址: {} 从文件获取RVA地址: {}".format(hex(va), foa, hex(rva)))

    # 将VA虚拟地址转为FOA文件偏移
    eip = dbg.get_register("eip")
    foa = get_offset_from_va(pe, eip)
    print("虚拟地址: 0x{:x} 对应文件偏移: {}".format(eip, foa))

    # 将FOA文件偏移转为VA虚拟地址
    va = get_va_from_foa(pe, foa)
    print("文件地址: {} 对应虚拟地址: 0x{:x}".format(foa, va))

    # 将FOA文件偏移地址转为RVA相对地址
    rva = get_rva_from_foa(pe, foa)
    print("文件地址: {} 对应的RVA相对地址: 0x{:x}".format(foa, rva))

    dbg.close()
```

**查找SafeSEH内存地址:** 读入PE文件到内存，验证该程序的SEH保护是否开启，如果开启则尝试输出SEH内存地址。
```Python
from LyScript32 import MyDebug
import struct

LOG_HANDLERS = True

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 得到PE头部基地址
    memory_image_base = dbg.get_base_from_address(dbg.get_local_base())

    peoffset = dbg.read_memory_dword(memory_image_base + int(0x3c))
    pebase = memory_image_base + peoffset

    flags = dbg.read_memory_word(pebase + int(0x5e))
    if(flags & int(0x400)) != 0:
        print("SafeSEH | NoHandler")

    numberofentries = dbg.read_memory_dword(pebase + int(0x74))
    if numberofentries > 10:

        # 读取 pebase+int(0x78)+8*10 | pebase+int(0x78)+8*10+4  读取八字节,分成两部分读取
        sectionaddress, sectionsize = [dbg.read_memory_dword(pebase+int(0x78)+8*10),
                                       dbg.read_memory_dword(pebase+int(0x78)+8*10 + 4)
                                       ]
        sectionaddress += memory_image_base
        data = dbg.read_memory_dword(sectionaddress)
        condition = (sectionsize != 0) and ((sectionsize == int(0x40)) or (sectionsize == data))

        if condition == False:
            print("[-] SafeSEH 无保护")
        if data < int(0x48):
            print("[-] 无法识别的DLL/EXE程序")

        sehlistaddress, sehlistsize = [dbg.read_memory_dword(sectionaddress+int(0x40)),
                                       dbg.read_memory_dword(sectionaddress+int(0x40) + 4)
                                       ]
        if sehlistaddress != 0 and sehlistsize != 0:
            print("[+] SafeSEH 保护中 | 长度: {}".format(sehlistsize))
            if LOG_HANDLERS == True:
                for i in range(sehlistsize):
                    sehaddress = dbg.read_memory_dword(sehlistaddress + 4 * i)
                    sehaddress += memory_image_base
                    print("SEHAddress = {}".format(hex(sehaddress)))

    dbg.close()
```

**扫描所有模块匹配特征:** 针对程序内加载的所有模块扫描特征码，如果找到了会返回内存地址，以及模块详细参数。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 获取所有模块
    for entry in dbg.get_all_module():
        eip = entry.get("entry")
        base = entry.get("base")
        name = entry.get("name")

        if eip != 0:
            # 设置EIP到模块入口处
            dbg.set_register("eip",eip)

            # 开始搜索特征
            search = dbg.scan_memory_one("ff 25 ??")
            if search != 0 or search != None:

                # 如果找到了,则反汇编此行
                dasm = dbg.disasm_fast_at(search)

                print("addr = {} | base = {} | module = {} | search_addr = {} | dasm = {}"
                      .format(eip,base,name,eip,dasm.get("disasm")))

    dbg.close()
```

**绕过反调试机制:** 最常用的反调试机制就是用`IsDebuggerPresent`该标志检查`PEB+2`位置处的内容，如果为1则表示正在被调试，我们运行脚本直接将其设置为0即可绕过反调试机制。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    # 初始化
    dbg = MyDebug()
    dbg.connect()

    # 通过PEB找到调试标志位
    peb = dbg.get_peb_address(dbg.get_process_id())
    print("调试标志地址: 0x{:x}".format(peb+2))

    flag = dbg.read_memory_byte(peb+2)
    print("调试标志位: {}".format(flag))

    # 将调试标志设置为0即可过掉反调试
    nop_debug = dbg.write_memory_byte(peb+2,0)
    print("反调试绕过状态: {}".format(nop_debug))
    
    dbg.close()
```

**绕过进程枚举:** 病毒会枚举所有运行的进程以确认是否有调试器在运行，我们可以在特定的函数开头处写入`SUB EAX,EAX RET`指令让其无法调用枚举函数从而失效。
```Python
from LyScript32 import MyDebug

# 得到所需要的机器码
def set_assemble_opcde(dbg,address):
    # 得到第一条长度
    opcode_size = dbg.assemble_code_size("sub eax,eax")

    # 写出汇编指令
    dbg.assemble_at(address, "sub eax,eax")
    dbg.assemble_at(address + opcode_size , "ret")

if __name__ == "__main__":
    # 初始化
    dbg = MyDebug()
    dbg.connect()

    # 得到函数所在内存地址
    process32first = dbg.get_module_from_function("kernel32","Process32FirstW")
    process32next = dbg.get_module_from_function("kernel32","Process32NextW")
    print("process32first = 0x{:x} | process32next = 0x{:x}".format(process32first,process32next))

    # 替换函数位置为sub eax,eax ret
    set_assemble_opcde(dbg, process32first)
    set_assemble_opcde(dbg, process32next)

    dbg.close()
```

**批量搜索反汇编代码:** 与搜索机器码类似，此功能实现了搜索代码段中所有指令集，匹配列表中是否存在，存在则返回地址。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    local_base_start = dbg.get_local_base()
    local_base_end = local_base_start + dbg.get_local_size()
    print("开始地址: {} --> 结束地址: {}".format(hex(local_base_start),hex(local_base_end)))

    search_asm = ['test eax,eax', 'cmp esi, edi', 'pop edi', 'cmp esi,edi', 'jmp esp']

    while local_base_start <= local_base_end:
        disasm = dbg.get_disasm_one_code(local_base_start)
        print("地址: 0x{:08x} --> 反汇编: {}".format(local_base_start,disasm))

        # 寻找指令
        for index in range(0, len(search_asm)):
            if disasm == search_asm[index]:
                print("地址: {} --> 反汇编: {}".format(hex(local_base_start), disasm))

        # 递增计数器
        local_base_start = local_base_start + dbg.get_disasm_operand_size(local_base_start)

    dbg.close()
```

**搜索反汇编列表特征:** 使用python实现方法，通过特定方法扫描内存范围，如果出现我们所需要的指令集序列，则输出该指令的具体内存地址。
```Python
from LyScript32 import MyDebug

# 传入汇编代码,得到对应机器码
def get_opcode_from_assemble(dbg_ptr,asm):
    byte_code = bytearray()

    addr = dbg_ptr.create_alloc(1024)
    if addr != 0:
        asm_size = dbg_ptr.assemble_code_size(asm)
        # print("汇编代码占用字节: {}".format(asm_size))

        write = dbg_ptr.assemble_write_memory(addr,asm)
        if write == True:
            for index in range(0,asm_size):
                read = dbg_ptr.read_memory_byte(addr + index)
                # print("{:02x} ".format(read),end="")
                byte_code.append(read)
        dbg_ptr.delete_alloc(addr)
        return byte_code
    else:
        return bytearray(0)

# 搜索机器码,如果存在则返回
def SearchOpCode(dbg_ptr, Search):

    # 搜索机器码并转换为列表
    op_code = []
    for index in Search:
        byte_array = get_opcode_from_assemble(dbg, index)
        for index in byte_array:
            op_code.append(hex(index))

    # print("机器码列表: {}".format(op_code))

    # 将机器码列表转换为字符串
    # 1.先转成字符串列表
    x = [str(i) for i in op_code]

    # 2.将字符串列表转为字符串
    # search_code = ' '.join(x).replace("0x","")
    search_code = []

    # 增加小于三位前面的0
    for l in range(0,len(x)):
        if len(x[l]) <= 3:
            # 如果是小于3位数则在前面增加0
            # print(''.join(x[l]).replace("0x","").zfill(2))
            search_code.append(''.join(x[l]).replace("0x","").zfill(2))
        else:
            search_code.append(''.join(x[l]).replace("0x", ""))

    # 3.变成字符串
    search_code = ' '.join(search_code).replace("0x", "")
    print("被搜索字符串: {}".format(search_code))

    # 调用搜索命令
    ref = dbg.scan_memory_one(search_code)
    if ref != None or ref != 0:
        return ref
    else:
        return 0
    return 0

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 搜索一个指令序列,用于快速查找构建漏洞利用代码
    SearchCode = [
        ["pop ecx", "pop ebp", "ret", "push ebp"],
        ["push ebp", "mov ebp,esp"],
        ["mov ecx, dword ptr ds:[eax+0x3C]", "add ecx, eax"]
    ]

    # 检索内存指令集
    for item in range(0, len(SearchCode)):
        Search = SearchCode[item]
        ret = SearchOpCode(dbg, Search)
        print("所搜指令所在内存: {}".format(hex(ret)))

    dbg.close()
```

**搜索内存中的机器码:** 相比于文件机器码而言，内存机器码则需要配合`LyScript`插件，从内存中寻找指令片段。
```Python
from LyScript32 import MyDebug

# 将可执行文件中的单数转换为 0x00 格式
def ReadHexCode(code):
    hex_code = []

    for index in code:
        if index >= 0 and index <= 15:
            #print("0" + str(hex(index).replace("0x","")))
            hex_code.append("0" + str(hex(index).replace("0x","")))
        else:
            hex_code.append(hex(index).replace("0x",""))
            #print(hex(index).replace("0x",""))

    return hex_code

# 获取到内存中的机器码
def GetCode():
    try:
        ref_code = []
        dbg = MyDebug()
        connect_flag = dbg.connect()
        if connect_flag != 1:
            return None

        start_address = dbg.get_local_base()
        end_address = start_address + dbg.get_local_size()

        # 循环得到机器码
        for index in range(start_address,end_address):
            read_bytes = dbg.read_memory_byte(index)
            ref_code.append(read_bytes)

        dbg.close()
        return ref_code
    except Exception:
        return False

# 在字节数组中匹配是否与特征码一致
def SearchHexCode(Code,SearchCode,ReadByte):
    SearchCount = len(SearchCode)
    #print("特征码总长度: {}".format(SearchCount))
    for item in range(0,ReadByte):
        count = 0
        # 对十六进制数切片,每次向后遍历SearchCount
        OpCode = Code[ 0+item :SearchCount+item ]
        #print("切割数组: {} --> 对比: {}".format(OpCode,SearchCode))
        try:
            for x in range(0,SearchCount):
                if OpCode[x] == SearchCode[x]:
                    count = count + 1
                    #print("寻找特征码计数: {} {} {}".format(count,OpCode[x],SearchCode[x]))
                    if count == SearchCount:
                        # 如果找到了,就返回True,否则返回False
                        return True
                        exit(0)
        except Exception:
            pass
    return False

if __name__ == "__main__":
    # 读取到内存机器码
    ref_code = GetCode()
    if ref_code != False:
        # 转为十六进制
        hex_code = ReadHexCode(ref_code)
        code_size = len(hex_code)

        # 指定要搜索的特征码序列
        search = ['c0', '74', '0d', '66', '3b', 'c6', '77', '08']

        # 搜索特征: hex_code = exe的字节码,search=搜索特征码,code_size = 搜索大小
        ret = SearchHexCode(hex_code, search, code_size)
        if ret == True:
            print("特征码 {} 存在".format(search))
        else:
            print("特征码 {} 不存在".format(search))
    else:
        print("读入失败")
```

**搜索内存反汇编代码:** 通过`LyScript`插件读入内存机器码，并在该机器码中寻找指令片段，找到后返回内存首地址。
```Python
from LyScript32 import MyDebug

# 检索指定序列中是否存在一段特定的指令集
def SearchOpCode(OpCodeList,SearchCode,ReadByte):
    SearchCount = len(SearchCode)
    for item in range(0,ReadByte):
        count = 0
        OpCode_Dic = OpCodeList[ 0 + item : SearchCount + item ]
        # print("切割字典: {}".format(OpCode_Dic))
        try:
            for x in range(0,SearchCount):
                if OpCode_Dic[x].get("opcode") == SearchCode[x]:
                    #print(OpCode_Dic[x].get("addr"),OpCode_Dic[x].get("opcode"))
                    count = count + 1
                    if count == SearchCount:
                        #print(OpCode_Dic[0].get("addr"))
                        return OpCode_Dic[0].get("addr")
                        exit(0)
        except Exception:
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
封装如上代码接口，实现`get_opcode_from_assemble()`用户传入汇编指令，得到该指令对应机器码。
```Python
from LyScript32 import MyDebug

# 传入汇编代码,得到对应机器码
def get_opcode_from_assemble(dbg_ptr,asm):
    byte_code = bytearray()

    addr = dbg_ptr.create_alloc(1024)
    if addr != 0:
        asm_size = dbg_ptr.assemble_code_size(asm)
        # print("汇编代码占用字节: {}".format(asm_size))

        write = dbg_ptr.assemble_write_memory(addr,asm)
        if write == True:
            for index in range(0,asm_size):
                read = dbg_ptr.read_memory_byte(addr + index)
                # print("{:02x} ".format(read),end="")
                byte_code.append(read)
        dbg_ptr.delete_alloc(addr)
        return byte_code
    else:
        return bytearray(0)

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

**指令机器码内存搜索:** 在当前载入程序的所有模块中搜索特定的一组机器码指令，找到后返回该指令集内存地址。
```Python
from LyScript32 import MyDebug
import time

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 需要搜索的指令集片段
    opcode = ['ff 25','ff 55 fc','8b fe']

    # 循环搜索指令集内存地址
    for index,entry in zip(range(0,len(opcode)), dbg.get_all_module()):
        eip = entry.get("entry")
        base_name = entry.get("name")
        if eip != 0:
            dbg.set_register("eip",eip)
            search_address = dbg.scan_memory_all(opcode[index])

            if search_address != False:
                print("搜索模块: {} --> 匹配个数: {} --> 机器码: {}"
			.format(base_name,len(search_address),opcode[index]))
                # 输出地址
                for search_index in search_address:
                    print("[*] {}".format(hex(search_index)))

        time.sleep(0.3)
    dbg.close()
```

**逐条进行反汇编输出:** 封装函数`disasm_code()`实现了通过循环的方式逐条输出反汇编代码完整信息，并打印到屏幕。
```Python
from LyScript32 import MyDebug

# 封装反汇编多条函数
def disasm_code(dbg_ptr, eip, count):
    disasm_length = 0

    for index in range(0, count):
        # 获取一条反汇编代码
        disasm_asm = dbg_ptr.get_disasm_one_code(eip + disasm_length)
        disasm_addr = eip + disasm_length

        # 某些指令无法被计算出长度,此处可以添加直接跳过
        if(disasm_asm == "push 0xC0000409"):
            disasm_size = 5
        else:
            disasm_size = dbg_ptr.assemble_code_size(disasm_asm)

        print("内存地址: 0x{:08x} | 反汇编: {:35} | 长度: {}  | 机器码: "
		.format(disasm_addr, disasm_asm, disasm_size),end="")

        # 逐字节读入机器码
        for length in range(0, disasm_size):
            read = dbg_ptr.read_memory_byte(disasm_addr + length)
            print("{:02x} ".format(read),end="")
        print()

        # 递增地址
        disasm_length = disasm_length + disasm_size

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")
    disasm_code(dbg, eip, 55)

    dbg.close()
```

**实现劫持EIP指针:** 这里我们演示一个案例，你可以自己实现一个`write_opcode_from_assemble()`函数批量将列表中的指令集写出到内存。
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
封装实现`write_opcode_from_assemble()`函数，传入一个汇编指令列表，自动转为机器码并写出到堆内，控制EIP执行流实现劫持指令的目的。
```Python
from LyScript32 import MyDebug

# 传入汇编指令列表,直接将机器码写入对端内存
def write_opcode_from_assemble(dbg_ptr,asm_list):
    addr_count = 0
    addr = dbg_ptr.create_alloc(1024)
    if addr != 0:
        for index in asm_list:
            asm_size = dbg_ptr.assemble_code_size(index)
            if asm_size != 0:
                # print("长度: {}".format(asm_size))
                write = dbg_ptr.assemble_write_memory(addr + addr_count, index)
                if write == True:
                    addr_count = addr_count + asm_size
                else:
                    dbg_ptr.delete_alloc(addr)
                    return 0
            else:
                dbg_ptr.delete_alloc(addr)
                return 0
    else:
        return 0
    return addr

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
执行劫持函数很简单，运行后会看到一个错误弹窗，说明程序执行流已经被转向了。

**得到_PEB_LDR_DATA线程环境块:** 想要得到线程环境块最好的办法就是在目标内存中执行获取线程块的汇编指令，我们可以写出到内存并执行取值。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug(address="127.0.0.1")
    dbg.connect()

    # 保存当前EIP
    eip = dbg.get_register("eip")

    # 创建堆
    heap_addres = dbg.create_alloc(1024)
    print("堆空间地址: {}".format(hex(heap_addres)))

    # 写出汇编指令
    # mov eax,fs:[0x30] 得到 _PEB
    dbg.assemble_at(heap_addres,"mov eax,fs:[0x30]")
    asmfs_size = dbg.get_disasm_operand_size(heap_addres)

    # 写出汇编指令
    # mov eax,[eax+0x0C] 得到 _PEB_LDR_DATA
    dbg.assemble_at(heap_addres + asmfs_size, "mov eax, [eax + 0x0C]")
    asmeax_size = dbg.get_disasm_operand_size(heap_addres + asmfs_size)

    # 跳转回EIP位置
    dbg.assemble_at(heap_addres+ asmfs_size + asmeax_size , "jmp {}".format(hex(eip)))

    # 设置EIP到堆首地址
    dbg.set_register("eip",heap_addres)

    dbg.close()
```

**实现脱UPX压缩壳:** 将当前EIP停留在UPX壳的首地址处，执行如下脚本，将可以自动寻找到当前EIP的具体位置。
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

    is_64 = False

    # 判断是否时64位数
    if is_64 == False:
        currentIP = dbg.get_register("eip")

        if dbg.read_memory_word(currentIP) != int(0xBE60):
            print("[-] 可能不是UPX")
            dbg.close()

        patternAddr = dbg.scan_memory_one("83 EC ?? E9 ?? ?? ?? ?? 00")
        print("匹配到的地址: {}".format(hex(patternAddr)))

        dbg.set_breakpoint(patternAddr)
        dbg.set_debug("Run")
        dbg.set_debug("Wait")
        dbg.delete_breakpoint(patternAddr)

        dbg.set_debug("StepOver")
        dbg.set_debug("StepOver")
        print("[+] 程序OEP = 0x{:x}".format(dbg.get_register("eip")))

    else:
        currentIP = dbg.get_register("rip")

        if dbg.read_memory_dword(currentIP) != int(0x55575653):
            print("[-] 可能不是UPX")
            dbg.close()

        patternAddr = dbg.scan_memory_one("48 83 EC ?? E9")
        print("匹配到的地址: {}".format(hex(patternAddr)))

        dbg.set_breakpoint(patternAddr)
        dbg.set_debug("Run")
        dbg.set_debug("Wait")
        dbg.delete_breakpoint(patternAddr)

        dbg.set_debug("StepOver")
        dbg.set_debug("StepOver")
        print("[+] 程序OEP = 0x{:x}".format(dbg.get_register("eip")))

    dbg.close()
```

**通过断点检测监视函数:** 通过运用`check_breakpoint()`断点检测函数，在断下后遍历堆栈，即可实现特定函数参数枚举。
```Python
import time
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()

    # 连接到调试器
    connect_flag = dbg.connect()
    dbg.is_connect()

    # 获取函数内存地址
    addr = dbg.get_module_from_function("user32.dll","MessageBoxA")

    # 设置断点
    dbg.set_breakpoint(addr)

    # 循环监视
    while True:
        # 检查断点是否被命中
        check = dbg.check_breakpoint(addr)
        if check == True:
            # 命中则取出堆栈参数
            esp = dbg.get_register("esp")
            arg4 = dbg.read_memory_dword(esp)
            arg3 = dbg.read_memory_dword(esp + 4)
            arg2 = dbg.read_memory_dword(esp + 8)
            arg1 = dbg.read_memory_dword(esp + 12)
            print("arg1 = {:x} arg2 = {:x} arg3 = {:x} arg4 = {:x}".
                  format(arg1,arg2,arg3,arg4))

            dbg.set_debug("Run")
            time.sleep(1)
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

**将ShellCode从文本中注入到内存:** 从文本中读取`ShellCode`代码，将该代码注入到目标进程的堆中，并把当前内存属性设置为可执行。
```Python
from LyScript32 import MyDebug

# 将shellcode读入内存
def read_shellcode(path):
    shellcode_list = []
    with open(path,"r",encoding="utf-8") as fp:
        for index in fp.readlines():
            shellcode_line = index.replace('"',"").replace(" ","").replace("\n","").replace(";","")
            for code in shellcode_line.split("\\x"):
                if code != "" and code != "\\n":
                    shellcode_list.append("0x" + code)
    return shellcode_list

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 开辟堆空间
    address = dbg.create_alloc(1024)
    print("开辟堆空间: {}".format(hex(address)))
    if address == False:
        exit()

    # 设置内存可执行属性
    dbg.set_local_protect(address,32,1024)

    # 从文本中读取shellcode
    shellcode = read_shellcode("d://shellcode.txt")

    # 循环写入到内存
    for code_byte in range(0,len(shellcode)):
        bytef = int(shellcode[code_byte],16)
        dbg.write_memory_byte(code_byte + address, bytef)

    # 设置EIP位置
    dbg.set_register("eip",address)

    input()
    dbg.delete_alloc(address)

    dbg.close()
```
如果把这个过程反过来，就是将特定位置的汇编代码保存到本地。
```Python
from LyScript32 import MyDebug

# 将特定内存保存到文本中
def write_shellcode(dbg,address,size,path):
    with open(path,"a+",encoding="utf-8") as fp:
        for index in range(0, size - 1):
            # 读取机器码
            read_code = dbg.read_memory_byte(address + index)

            if (index+1) % 16 == 0:
                print("\\x" + str(read_code))
                fp.write("\\x" + str(read_code) + "\n")
            else:
                print("\\x" + str(read_code),end="")
                fp.write("\\x" + str(read_code))

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")
    write_shellcode(dbg,eip,128,"d://lyshark.txt")
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
                print("指令: {} --> 模块: {} --> 个数: {}".
		format(search_asm[index],base_name,len(search_address)))

                for search_index in search_address:
                    print("[*] {}".format(hex(search_index)))
            else:
                print("a")

        time.sleep(0.3)
    dbg.close()
 ```
 
 **使用内置脚本得到返回值:** 使用内置`run_command_exec()`函数时，用户只能得到内置脚本执行后的状态值，如果想要得到内置命令的返回值则你可以这样写。
 ```Python
 from LyScript32 import MyDebug
 
 dbg = MyDebug()
 conn = dbg.connect()
 
 # 首先定义一个脚本变量
 ref = dbg.run_command_exec("$addr=1024")
 
 # 将脚本返回值放到eax寄存器，或者开辟一个堆放到堆里
 dbg.run_command_exec("eax=$addr")
 
 # 最后拿到寄存器的值
 hex(dbg.get_register("eax"))
 ```
通过中转的方式，可以很好的得到内置脚本的返回值，如下我将其封装成了一个独立的方法。
```Python
from LyScript32 import MyDebug

# 得到脚本返回值
def GetScriptValue(dbg,script):
    try:
        ref = dbg.run_command_exec("push eax")
        if ref != True:
            return None
        ref = dbg.run_command_exec(f"eax={script}")
        if ref != True:
            return None
        reg = dbg.get_register("eax")
        ref = dbg.run_command_exec("pop eax")
        if ref != True:
            return None
        return reg
    except Exception:
        return None
    return None

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eax = "401000"
    ref = GetScriptValue(dbg,"mod.base({})".format(eax))
    print(hex(ref))
    
    dbg.close()
```

**获取节表内存属性:** 默认情况下插件可以得到当前节表，但无法直接取到节表内存属性，如果需要得到某个节的内存属性，可以这样写。

节表属性是一个数字，数字含义如下:
 - ER 执行/读取 32
 - E 执行 30
 - R 读取 2
 - W 写入 2
 - C 未知 4
 - N 空属性 1

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    conn = dbg.connect()

    section = dbg.get_section()
    for i in section:
        section_address = hex(i.get("addr"))
        section_name = i.get("name")
        section_size = i.get("size")
        section_type = dbg.get_local_protect(i.get("addr"))
        print(f"地址: {section_address} -> 名字: {section_name} -> 大小: {section_size}bytes -> ",end="")

        if(section_type == 32):
            print("属性: 执行/读取")
        elif(section_type == 30):
            print("属性: 执行")
        elif(section_type == 2):
            print("属性: 只读")
        elif(section_type == 4):
            print("属性: 读写")
        elif(section_type == 1):
            print("属性: 空属性")
        else:
            print("属性: 读/写/控制")

    dbg.close()
    pass
```

**封装获取反汇编代码:** 反汇编时可以使用`get_disasm_code()`函数，但如果想要自己实现可以这样写。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    conn = dbg.connect()

    # 获取当前EIP地址
    eip = dbg.get_register("eip")
    print("eip = {}".format(hex(eip)))

    # 向下反汇编字节数
    count = eip + 15
    while True:
        # 每次得到一条反汇编指令
        dissasm = dbg.get_disasm_one_code(eip)

        print("0x{:08x} | {}".format(eip, dissasm))

        # 判断是否满足退出条件
        if eip >= count:
            break
        else:
            # 得到本条反汇编代码的长度
            dis_size = dbg.assemble_code_size(dissasm)
            eip = eip + dis_size

    dbg.close()
    pass
```

**得到当前EIP机器码:** 获取到当前EIP指针所在位置的机器码，你可以灵活运用反汇编代码的组合实现。
```Python
from LyScript32 import MyDebug

# 得到机器码
def GetHexCode(dbg,address):
    ref_bytes = []
    # 首先得到反汇编指令,然后得到该指令的长度
    asm_len = dbg.assemble_code_size( dbg.get_disasm_one_code(address) )

    # 循环得到每个机器码
    for index in range(0,asm_len):
        ref_bytes.append(dbg.read_memory_byte(address))
        address = address + 1
    return ref_bytes

if __name__ == "__main__":
    dbg = MyDebug()
    conn = dbg.connect()

    # 获取当前EIP地址
    eip = dbg.get_register("eip")
    print("eip = {}".format(hex(eip)))

    # 得到机器码
    ref = GetHexCode(dbg,eip)
    for i in range(0,len(ref)):
        print("0x{:02x} ".format(ref[i]),end="")

    dbg.close()
    pass
```
如果将如上的两个方法结合起来，那么基本上就实现了获取反汇编窗口中的所有内容。
```Python
from LyScript32 import MyDebug

# 得到机器码
def GetHexCode(dbg,address):
    ref_bytes = []
    # 首先得到反汇编指令,然后得到该指令的长度
    asm_len = dbg.assemble_code_size( dbg.get_disasm_one_code(address) )
    # 循环得到每个机器码
    for index in range(0,asm_len):
        ref_bytes.append(dbg.read_memory_byte(address))
        address = address + 1
    return ref_bytes

if __name__ == "__main__":
    dbg = MyDebug()
    conn = dbg.connect()

    # 获取当前EIP地址
    eip = dbg.get_register("eip")
    print("eip = {}".format(hex(eip)))

    # 向下反汇编字节数
    count = eip + 20
    while True:
        # 每次得到一条反汇编指令
        dissasm = dbg.get_disasm_one_code(eip)

        print("0x{:08x} | {:50} | ".format(eip, dissasm),end="")

        # 得到机器码
        ref = GetHexCode(dbg, eip)
        for i in range(0, len(ref)):
            print("0x{:02x} ".format(ref[i]), end="")
        print()

        # 判断是否满足退出条件
        if eip >= count:
            break
        else:
            # 得到本条反汇编代码的长度
            dis_size = dbg.assemble_code_size(dissasm)
            eip = eip + dis_size

    dbg.close()
    pass
```

**封装汇编指令提取器:** 当用户传入指定汇编指令的时候，自动的将其转换成对应的机器码，代码很简单，首先`dbg.create_alloc(1024)`在进程内存中开辟堆空间，用于存放我们的机器码，然后调用`dbg.assemble_write_memory(alloc_address,"sub esp,10")`将一条汇编指令变成机器码写到对端内存，然后再`op = dbg.read_memory_byte(alloc_address + index)`依次将其读取出来即可。

```Python
from LyScript32 import MyDebug

# 传入汇编指令,获取该指令的机器码
def get_assembly_machine_code(dbg,asm):
    pass

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    machine_code_list = []

    # 开辟堆空间
    alloc_address = dbg.create_alloc(1024)
    print("分配堆: {}".format(hex(alloc_address)))

    # 得到汇编机器码
    machine_code = dbg.assemble_write_memory(alloc_address,"sub esp,10")
    if machine_code == False:
        dbg.delete_alloc(alloc_address)

    # 得到汇编指令长度
    machine_code_size = dbg.assemble_code_size("sub esp,10")
    if machine_code == False:
        dbg.delete_alloc(alloc_address)

    # 读取机器码
    for index in range(0,machine_code_size):
        op = dbg.read_memory_byte(alloc_address + index)
        machine_code_list.append(op)

    # 释放堆空间
    dbg.delete_alloc(alloc_address)

    # 输出机器码
    print(machine_code_list)
    dbg.close()
```
我们继续封装如上方法，封装成一个可以直接使用的`get_assembly_machine_code`函数。
```Python
from LyScript32 import MyDebug

# 传入汇编指令,获取该指令的机器码
def get_assembly_machine_code(dbg,asm):
    machine_code_list = []

    # 开辟堆空间
    alloc_address = dbg.create_alloc(1024)
    print("分配堆: {}".format(hex(alloc_address)))

    # 得到汇编机器码
    machine_code = dbg.assemble_write_memory(alloc_address,asm)
    if machine_code == False:
        dbg.delete_alloc(alloc_address)

    # 得到汇编指令长度
    machine_code_size = dbg.assemble_code_size(asm)
    if machine_code == False:
        dbg.delete_alloc(alloc_address)

    # 读取机器码
    for index in range(0,machine_code_size):
        op = dbg.read_memory_byte(alloc_address + index)
        machine_code_list.append(op)

    # 释放堆空间
    dbg.delete_alloc(alloc_address)
    return machine_code_list

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 转换第一对
    opcode = get_assembly_machine_code(dbg,"mov eax,1")
    for index in opcode:
        print("0x{:02X} ".format(index),end="")
    print()

    # 转换第二对
    opcode = get_assembly_machine_code(dbg,"sub esp,10")
    for index in opcode:
        print("0x{:02X} ".format(index),end="")
    print()

    dbg.close()
```

**扫描符合条件的内存:** 通过使用上方封装的`get_assembly_machine_code()`并配合`scan_memory_one(scan_string)`函数，在对端内存搜索是否存在符合条件的指令。
```Python
from LyScript32 import MyDebug

# 传入汇编指令,获取该指令的机器码
def get_assembly_machine_code(dbg,asm):
    machine_code_list = []

    # 开辟堆空间
    alloc_address = dbg.create_alloc(1024)
    print("分配堆: {}".format(hex(alloc_address)))

    # 得到汇编机器码
    machine_code = dbg.assemble_write_memory(alloc_address,asm)
    if machine_code == False:
        dbg.delete_alloc(alloc_address)

    # 得到汇编指令长度
    machine_code_size = dbg.assemble_code_size(asm)
    if machine_code == False:
        dbg.delete_alloc(alloc_address)

    # 读取机器码
    for index in range(0,machine_code_size):
        op = dbg.read_memory_byte(alloc_address + index)
        machine_code_list.append(op)

    # 释放堆空间
    dbg.delete_alloc(alloc_address)
    return machine_code_list

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    for item in ["push eax","mov eax,1","jmp eax","pop eax"]:
        # 转换成列表
        opcode = get_assembly_machine_code(dbg,item)
        #print("得到机器码列表: ",opcode)

        # 列表转换成字符串
        scan_string = " ".join([str(_) for _ in opcode])
        #print("搜索机器码字符串: ", scan_string)

        address = dbg.scan_memory_one(scan_string)
        print("第一个符合条件的内存块: {}".format(hex(address)))

    dbg.close()
```

**获取下一条汇编指令:** 下一条汇编指令的获取需要注意如果是被命中的指令则此处应该是CC断点占用一个字节，如果不是则正常获取到当前指令即可。

- 1.我们需要检查当前内存断点是否被命中，如果没有命中则说明此处我们需要获取到原始的汇编指令长度，然后与当前eip地址相加获得。
- 2.如果命中了断点，则此处有两种情况
  - 1.1 如果是用户下的断点，则此处调试器会在指令位置替换为CC，也就是汇编中的init停机指令，该指令占用1个字节，需要eip+1得到。
  - 1.2 如果是系统断点，EIP所停留的位置，则我们需要正常获取当前指令地址，此处调试器没有改动汇编指令仅仅只下下了异常断点。

```Python
from LyScript32 import MyDebug

# 获取当前EIP指令的下一条指令
def get_disasm_next(dbg,eip):
    next = 0

    # 检查当前内存地址是否被下了绊子
    check_breakpoint = dbg.check_breakpoint(eip)

    # 说明存在断点，如果存在则这里就是一个字节了
    if check_breakpoint == True:

        # 接着判断当前是否是EIP，如果是EIP则需要使用原来的字节
        local_eip = dbg.get_register("eip")

        # 说明是EIP并且命中了断点
        if local_eip == eip:
            dis_size = dbg.get_disasm_operand_size(eip)
            next = eip + dis_size
            next_asm = dbg.get_disasm_one_code(next)
            return next_asm
        else:
            next = eip + 1
            next_asm = dbg.get_disasm_one_code(next)
            return next_asm
        return None

    # 不是则需要获取到原始汇编代码的长度
    elif check_breakpoint == False:
        # 得到当前指令长度
        dis_size = dbg.get_disasm_operand_size(eip)
        next = eip + dis_size
        next_asm = dbg.get_disasm_one_code(next)
        return next_asm
    else:
        return None

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")

    next = get_disasm_next(dbg,eip)
    print("下一条指令: {}".format(next))

    prev = get_disasm_next(dbg,12391436)
    print("下一条指令: {}".format(prev))

    dbg.close()
```

**获取上一条汇编指令:** 上一条指令的获取难点就在于，我们无法确定当前指令的上一条指令到底有多长，所以只能用笨办法，逐行扫描对比汇编指令，如果找到则取出其上一条指令即可。
```Python
from LyScript32 import MyDebug

# 获取当前EIP指令的上一条指令
def get_disasm_prev(dbg,eip):
    prev_dasm = None
    # 得到当前汇编指令
    local_disasm = dbg.get_disasm_one_code(eip)

    # 只能向上扫描10行
    eip = eip - 10
    disasm = dbg.get_disasm_code(eip,10)

    # 循环扫描汇编代码
    for index in range(0,len(disasm)):
        # 如果找到了,就取出他的上一个汇编代码
        if disasm[index].get("opcode") == local_disasm:
            prev_dasm = disasm[index-1].get("opcode")
            break

    return prev_dasm

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")

    next = get_disasm_prev(dbg,eip)
    print("上一条指令: {}".format(next))

    dbg.close()
```

**判断是否为特定指令:** 判断当前传入的内存地址处的汇编指令集，看是否是`call,nop,jmp,ret`指令，如果是返回True否则返回False。
```Python
from LyScript32 import MyDebug

# 是否是跳转指令
def is_call(dbg,address):
    try:
        dis = dbg.get_disasm_one_code(address)
        if dis != False or dis != None:
            if dis.split(" ")[0].replace(" ","") == "call":
                return True
            return False
        return False
    except Exception:
        return False
    return False

# 是否是jmp
def is_jmp(dbg,address):
    try:
        dis = dbg.get_disasm_one_code(address)
        if dis != False or dis != None:
            if dis.split(" ")[0].replace(" ","") == "jmp":
                return True
            return False
        return False
    except Exception:
        return False
    return False

# 是否是ret
def is_ret(dbg,address):
    try:
        dis = dbg.get_disasm_one_code(address)
        if dis != False or dis != None:
            if dis.split(" ")[0].replace(" ","") == "ret":
                return True
            return False
        return False
    except Exception:
        return False
    return False

# 是否是nop
def is_nop(dbg,address):
    try:
        dis = dbg.get_disasm_one_code(address)
        if dis != False or dis != None:
            if dis.split(" ")[0].replace(" ","") == "nop":
                return True
            return False
        return False
    except Exception:
        return False
    return False

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")

    call = is_call(dbg, eip)
    print("是否是Call指令: {}".format(call))
    dbg.close()
````
同如上所示，我们也可以验证指令集是否是条件跳转命令，验证方式只需要稍微改动代码即可。
```Python
from LyScript32 import MyDebug

# 是否是条件跳转指令
def is_cond(dbg,address):
    try:
        dis = dbg.get_disasm_one_code(address)
        if dis != False or dis != None:

            if dis.split(" ")[0].replace(" ","") 
	    	in ["je","jne","jz","jnz","ja","jna","jp","jnp","jb","jnb","jg","jng","jge","jl","jle"]:
                return True
            return False
        return False
    except Exception:
        return False
    return False

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")

    call = is_cond(dbg, eip)
    print("是否是条件跳转指令: {}".format(call))
    dbg.close()
```

**内存区域交换与差异对比:** 内存交换可调用`memory_xchage`将两个内存颠倒顺序，内存差异对比可调用`memory_cmp`对比内存差异并返回列表。
```Python
from LyScript32 import MyDebug

# 交换两个内存区域
def memory_xchage(dbg,memory_ptr_x,memory_ptr_y,bytes):
    ref = False
    for index in range(0,bytes):
        # 读取两个内存区域
        read_byte_x = dbg.read_memory_byte(memory_ptr_x + index)
        read_byte_y = dbg.read_memory_byte(memory_ptr_y + index)

        # 交换内存
        ref = dbg.write_memory_byte(memory_ptr_x + index,read_byte_y)
        ref = dbg.write_memory_byte(memory_ptr_y + index, read_byte_x)
    return ref

# 对比两个内存区域
def memory_cmp(dbg,memory_ptr_x,memory_ptr_y,bytes):
    cmp_memory = []
    for index in range(0,bytes):

        item = {"addr":0, "x": 0, "y": 0}

        # 读取两个内存区域
        read_byte_x = dbg.read_memory_byte(memory_ptr_x + index)
        read_byte_y = dbg.read_memory_byte(memory_ptr_y + index)

        if read_byte_x != read_byte_y:
            item["addr"] = memory_ptr_x + index
            item["x"] = read_byte_x
            item["y"] = read_byte_y
            cmp_memory.append(item)
    return cmp_memory

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")

    # 内存交换
    flag = memory_xchage(dbg, 12386320,12386352,4)
    print("内存交换状态: {}".format(flag))

    # 内存对比
    cmp_ref = memory_cmp(dbg, 12386320,12386352,4)
    for index in range(0,len(cmp_ref)):
        print("地址: 0x{:08X} -> X: 0x{:02x} -> y: 0x{:02x}"
		.format(cmp_ref[index].get("addr"),cmp_ref[index].get("x"),cmp_ref[index].get("y")))

    dbg.close()
```

**内存与磁盘机器码比较:** 通过调用`read_memory_byte()`函数，或者`open()`打开文件，等就可以得到程序磁盘与内存中特定位置的机器码参数，然后通过对每一个列表中的字节进行比较，就可得到特定位置下磁盘与内存中的数据是否一致的判断。
```Python
#coding: utf-8
import binascii,os,sys
from LyScript32 import MyDebug

# 得到程序的内存镜像中的机器码
def get_memory_hex_ascii(address,offset,len):
    count = 0
    ref_memory_list = []
    for index in range(offset,len):
        # 读出数据
        char = dbg.read_memory_byte(address + index)
        count = count + 1

        if count % 16 == 0:
            if (char) < 16:
                print("0" + hex((char))[2:])
                ref_memory_list.append("0" + hex((char))[2:])
            else:
                print(hex((char))[2:])
                ref_memory_list.append(hex((char))[2:])
        else:
            if (char) < 16:
                print("0" + hex((char))[2:] + " ",end="")
                ref_memory_list.append("0" + hex((char))[2:])
            else:
                print(hex((char))[2:] + " ",end="")
                ref_memory_list.append(hex((char))[2:])
    return ref_memory_list

# 读取程序中的磁盘镜像中的机器码
def get_file_hex_ascii(path,offset,len):
    count = 0
    ref_file_list = []

    with open(path, "rb") as fp:
        # file_size = os.path.getsize(path)
        fp.seek(offset)

        for item in range(offset,offset + len):
            char = fp.read(1)
            count = count + 1
            if count % 16 == 0:
                if ord(char) < 16:
                    print("0" + hex(ord(char))[2:])
                    ref_file_list.append("0" + hex(ord(char))[2:])
                else:
                    print(hex(ord(char))[2:])
                    ref_file_list.append(hex(ord(char))[2:])
            else:
                if ord(char) < 16:
                    print("0" + hex(ord(char))[2:] + " ", end="")
                    ref_file_list.append("0" + hex(ord(char))[2:])
                else:
                    print(hex(ord(char))[2:] + " ", end="")
                    ref_file_list.append(hex(ord(char))[2:])
    return ref_file_list

if __name__ == "__main__":
    dbg = MyDebug()

    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    module_base = dbg.get_base_from_address(dbg.get_local_base())
    print("模块基地址: {}".format(hex(module_base)))

    # 得到内存机器码
    memory_hex_byte = get_memory_hex_ascii(module_base,0,1024)

    # 得到磁盘机器码
    file_hex_byte = get_file_hex_ascii("d://Win32Project1.exe",0,1024)

    # 输出机器码
    for index in range(0,len(memory_hex_byte)):
        # 比较磁盘与内存是否存在差异
        if memory_hex_byte[index] != file_hex_byte[index]:
            # 存在差异则输出
            print("\n相对位置: [{}] --> 磁盘字节: 0x{} --> 内存字节: 0x{}".
                  format(index,memory_hex_byte[index],file_hex_byte[index]))
    dbg.close()
```

**内存ASCII码解析:** 通过封装的`get_memory_hex_ascii`得到内存机器码，然后再使用如下过程实现输出该内存中的机器码所对应的ASCII码。
```Python
from LyScript32 import MyDebug
import os,sys

# 转为ascii
def to_ascii(h):
    list_s = []
    for i in range(0, len(h), 2):
        list_s.append(chr(int(h[i:i+2], 16)))
    return ''.join(list_s)

# 转为16进制
def to_hex(s):
    list_h = []
    for c in s:
        list_h.append(hex(ord(c))[2:])
    return ''.join(list_h)

# 得到程序的内存镜像中的机器码
def get_memory_hex_ascii(address,offset,len):
    count = 0
    ref_memory_list = []
    for index in range(offset,len):
        # 读出数据
        char = dbg.read_memory_byte(address + index)
        count = count + 1

        if count % 16 == 0:
            if (char) < 16:
                ref_memory_list.append("0" + hex((char))[2:])
            else:
                ref_memory_list.append(hex((char))[2:])
        else:
            if (char) < 16:
                ref_memory_list.append("0" + hex((char))[2:])
            else:
                ref_memory_list.append(hex((char))[2:])
    return ref_memory_list


if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")

    # 得到模块基地址
    module_base = dbg.get_base_from_address(dbg.get_local_base())

    # 得到指定区域内存机器码
    ref_memory_list = get_memory_hex_ascii(module_base,0,1024)

    # 解析ascii码
    break_count = 1
    for index in ref_memory_list:
        if break_count %32 == 0:
            print(to_ascii(hex(int(index, 16))[2:]))
        else:
            print(to_ascii(hex(int(index, 16))[2:]),end="")
        break_count = break_count + 1

    dbg.close()
```

**内存特征码匹配:** 通过二次封装`get_memory_hex_ascii()`实现扫描内存特征码功能，如果存在则返回True否则返回False。
```Python
from LyScript32 import MyDebug
import os,sys

# 得到程序的内存镜像中的机器码
def get_memory_hex_ascii(address,offset,len):
    count = 0
    ref_memory_list = []
    for index in range(offset,len):
        # 读出数据
        char = dbg.read_memory_byte(address + index)
        count = count + 1

        if count % 16 == 0:
            if (char) < 16:
                ref_memory_list.append("0" + hex((char))[2:])
            else:
                ref_memory_list.append(hex((char))[2:])
        else:
            if (char) < 16:
                ref_memory_list.append("0" + hex((char))[2:])
            else:
                ref_memory_list.append(hex((char))[2:])
    return ref_memory_list


# 在指定区域内搜索特定的机器码,如果完全匹配则返回
def search_hex_ascii(address,offset,len,hex_array):
    # 得到指定区域内存机器码
    ref_memory_list = get_memory_hex_ascii(address,offset,len)

    array = []

    # 循环输出字节
    for index in range(0,len + len(hex_array)):

        # 如果有则继续装
        if len(hex_array) != len(array):
            array.append(ref_memory_list[offset + index])

        else:
            for y in range(0,len(array)):
                if array[y] != ref_memory_list[offset + index + y]:
                    return False

        array.clear()
    return False

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")

    # 得到模块基地址
    module_base = dbg.get_base_from_address(dbg.get_local_base())
    
    re = search_hex_ascii(module_base,0,100,hex_array=["0x4d","0x5a"])
    
    dbg.close()
```
特征码扫描一般不需要自己写，自己写的麻烦，而且不支持通配符，可以直接调用我们API中封装好的`scan_memory_one()`它可以支持`??`通配符模糊匹配，且效率要高许多。

**堆栈地址有符号无符号转换:** peek_stack命令传入的是堆栈下标位置默认从0开始，并输出一个`十进制有符号`长整数，首先实现有符号与无符号数之间的转换操作，为后续堆栈扫描做准备。
```Python
from LyScript32 import MyDebug

# 有符号整数转无符号数
def long_to_ulong(inter,is_64 = False):
    if is_64 == False:
        return inter & ((1 << 32) - 1)
    else:
        return inter & ((1 << 64) - 1)

# 无符号整数转有符号数
def ulong_to_long(inter,is_64 = False):
    if is_64 == False:
        return (inter & ((1 << 31) - 1)) - (inter & (1 << 31))
    else:
        return (inter & ((1 << 63) - 1)) - (inter & (1 << 63))

if __name__ == "__main__":
    dbg = MyDebug()

    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    for index in range(0,10):

        # 默认返回有符号数
        stack_address = dbg.peek_stack(index)

        # 使用转换
        print("默认有符号数: {:15} --> 转为无符号数: {:15} --> 转为有符号数: {:15}".
              format(stack_address, 
	      long_to_ulong(stack_address),
	      ulong_to_long(long_to_ulong(stack_address))))

    dbg.close()
```

**扫描堆栈并反汇编一条:** 我们使用`get_disasm_one_code()`函数，扫描堆栈地址并得到该地址处的第一条反汇编代码。
```Python
from LyScript32 import MyDebug

# 有符号整数转无符号数
def long_to_ulong(inter,is_64 = False):
    if is_64 == False:
        return inter & ((1 << 32) - 1)
    else:
        return inter & ((1 << 64) - 1)

# 无符号整数转有符号数
def ulong_to_long(inter,is_64 = False):
    if is_64 == False:
        return (inter & ((1 << 31) - 1)) - (inter & (1 << 31))
    else:
        return (inter & ((1 << 63) - 1)) - (inter & (1 << 63))

if __name__ == "__main__":
    dbg = MyDebug()

    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    for index in range(0,10):

        # 默认返回有符号数
        stack_address = dbg.peek_stack(index)

        # 反汇编一行
        dasm = dbg.get_disasm_one_code(stack_address)

        # 根据地址得到模块基址
        if stack_address <= 0:
            mod_base = 0
        else:
            mod_base = dbg.get_base_from_address(long_to_ulong(stack_address))

        print("stack => [{}] addr = {:10} base = {:10} dasm = {}".
		format(index, hex(long_to_ulong(stack_address)),hex(mod_base), dasm))

    dbg.close()
```

**得到堆栈返回模块基址:** 首先我们需要得到程序全局状态下的所有加载模块的基地址，然后得到当前堆栈内存地址内的实际地址，并通过实际内存地址得到模块基地址，对比全局表即可拿到当前模块是返回到了哪里。
```Python
from LyScript32 import MyDebug

# 有符号整数转无符号数
def long_to_ulong(inter,is_64 = False):
    if is_64 == False:
        return inter & ((1 << 32) - 1)
    else:
        return inter & ((1 << 64) - 1)

# 无符号整数转有符号数
def ulong_to_long(inter,is_64 = False):
    if is_64 == False:
        return (inter & ((1 << 31) - 1)) - (inter & (1 << 31))
    else:
        return (inter & ((1 << 63) - 1)) - (inter & (1 << 63))

if __name__ == "__main__":
    dbg = MyDebug()

    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 得到程序加载过的所有模块信息
    module_list = dbg.get_all_module()

    # 向下扫描堆栈
    for index in range(0,10):

        # 默认返回有符号数
        stack_address = dbg.peek_stack(index)

        # 反汇编一行
        dasm = dbg.get_disasm_one_code(stack_address)

        # 根据地址得到模块基址
        if stack_address <= 0:
            mod_base = 0
        else:
            mod_base = dbg.get_base_from_address(long_to_ulong(stack_address))

        # print("stack => [{}] addr = {:10} base = {:10} dasm = {}"
		.format(index, hex(long_to_ulong(stack_address)),hex(mod_base), dasm))
        if mod_base > 0:
            for x in module_list:
                if mod_base == x.get("base"):
                    print("stack => [{}] addr = {:10} base = {:10} dasm = {:15} return = {:10}"
                          .format(index,hex(long_to_ulong(stack_address)),hex(mod_base), dasm,
                                  x.get("name")))

    dbg.close()
```

**第三方反汇编库应用:** 通过LyScript插件读取出内存中的机器码，然后交给`capstone`反汇编库执行，并将结果输出成字典格式。
```Python
#coding: utf-8
import binascii,os,sys
import pefile
from capstone import *
from LyScript32 import MyDebug

# 得到内存反汇编代码
def get_memory_disassembly(address,offset,len):
    # 反汇编列表
    dasm_memory_dict = []

    # 内存列表
    ref_memory_list = bytearray()

    # 读取数据
    for index in range(offset,len):
        char = dbg.read_memory_byte(address + index)
        ref_memory_list.append(char)

    # 执行反汇编
    md = Cs(CS_ARCH_X86,CS_MODE_32)
    for item in md.disasm(ref_memory_list,0x1):
        addr = int(pe_base) + item.address
        dasm_memory_dict.append({"address": str(addr), "opcode": item.mnemonic + " " + item.op_str})
    return dasm_memory_dict

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    pe_base = dbg.get_local_base()
    pe_size = dbg.get_local_size()

    print("模块基地址: {}".format(hex(pe_base)))
    print("模块大小: {}".format(hex(pe_size)))

    # 得到内存反汇编代码
    dasm_memory_list = get_memory_disassembly(pe_base,0,pe_size)
    print(dasm_memory_list)

    dbg.close()
```
如果我们将磁盘文件也反汇编到一个列表内，然后对比两者就实现了一个简易版应用层钩子扫描器。
```Python
#coding: utf-8
import binascii,os,sys
import pefile
from capstone import *
from LyScript32 import MyDebug

# 得到内存反汇编代码
def get_memory_disassembly(address,offset,len):
    # 反汇编列表
    dasm_memory_dict = []

    # 内存列表
    ref_memory_list = bytearray()

    # 读取数据
    for index in range(offset,len):
        char = dbg.read_memory_byte(address + index)
        ref_memory_list.append(char)

    # 执行反汇编
    md = Cs(CS_ARCH_X86,CS_MODE_32)
    for item in md.disasm(ref_memory_list,0x1):
        addr = int(pe_base) + item.address
        dic = {"address": str(addr), "opcode": item.mnemonic + " " + item.op_str}
        dasm_memory_dict.append(dic)
    return dasm_memory_dict

# 反汇编文件中的机器码
def get_file_disassembly(path):
    opcode_list = []
    pe = pefile.PE(path)
    ImageBase = pe.OPTIONAL_HEADER.ImageBase

    for item in pe.sections:
        if str(item.Name.decode('UTF-8').strip(b'\x00'.decode())) == ".text":
            # print("虚拟地址: 0x%.8X 虚拟大小: 0x%.8X" %(item.VirtualAddress,item.Misc_VirtualSize))
            VirtualAddress = item.VirtualAddress
            VirtualSize = item.Misc_VirtualSize
            ActualOffset = item.PointerToRawData
    StartVA = ImageBase + VirtualAddress
    StopVA = ImageBase + VirtualAddress + VirtualSize
    with open(path,"rb") as fp:
        fp.seek(ActualOffset)
        HexCode = fp.read(VirtualSize)

    md = Cs(CS_ARCH_X86, CS_MODE_32)
    for item in md.disasm(HexCode, 0):
        addr = hex(int(StartVA) + item.address)
        dic = {"address": str(addr) , "opcode": item.mnemonic + " " + item.op_str}
        # print("{}".format(dic))
        opcode_list.append(dic)
    return opcode_list

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    pe_base = dbg.get_local_base()
    pe_size = dbg.get_local_size()

    print("模块基地址: {}".format(hex(pe_base)))
    print("模块大小: {}".format(hex(pe_size)))

    # 得到内存反汇编代码
    dasm_memory_list = get_memory_disassembly(pe_base,0,pe_size)
    dasm_file_list = get_file_disassembly("d://win32project1.exe")

    # 循环对比内存与文件中的机器码
    for index in range(0,len(dasm_file_list)):
        if dasm_memory_list[index] != dasm_file_list[index]:
            print("地址: {:8} --> 内存反汇编: {:32} --> 磁盘反汇编: {:32}".
                  format(dasm_memory_list[index].get("address"),
		  	dasm_memory_list[index].get("opcode"),dasm_file_list[index].get("opcode")))
    dbg.close()
```

**通过PEB获取堆基址:** 堆基址的获取非常简单，我们只需要找到`peb+0x90`的位置，将其读取出来即可。
```Python
from LyScript32 import MyDebug

# 获取模块基址
def getKernelModuleBase(dbg):
    # 内置函数得到进程PEB
    local_pid = dbg.get_process_id()
    peb = dbg.get_peb_address(local_pid)
    # print("进程PEB: {}".format(hex(peb)))

    # esi = PEB_LDR_DATA结构体的地址
    ptr = peb + 0x0c

    # 读取内存指针
    PEB_LDR_DATA = dbg.read_memory_ptr(ptr)
    # print("读入PEB_LDR_DATA里面的地址: {}".format(hex(PEB_LDR_DATA)))

    # esi = 模块链表指针InInitializationOrderModuleList
    ptr = PEB_LDR_DATA + 0x1c
    InInitializationOrderModuleList = dbg.read_memory_ptr(ptr)
    # print("读入InInitializationOrderModuleList里面的地址: {}".
    # format(hex(InInitializationOrderModuleList)))

    # 取出kernel32.dll模块基址
    ptr = InInitializationOrderModuleList + 0x08
    modbase = dbg.read_memory_ptr(ptr)
    # print("kernel32.dll = {}".format(hex(modbase)))
    return modbase

# 获取进程堆基址
def getHeapsAddress(dbg):
    # 内置函数得到进程PEB
    local_pid = dbg.get_process_id()
    peb = dbg.get_peb_address(local_pid)
    # print("进程PEB: {}".format(hex(peb)))

    # 读取堆分配地址
    ptr = peb + 0x90
    peb_address = dbg.read_memory_ptr(ptr)
    # print("读取堆分配: {}".format(hex(peb_address)))

    heap_address = dbg.read_memory_ptr(peb_address)
    # print("当前进程堆基址: {}".format(hex(heap_address)))
    return heap_address

if __name__ == "__main__":
    dbg = MyDebug()
    conn = dbg.connect()

    k32 = getKernelModuleBase(dbg)
    print("kernel32 = {}".format(hex(k32)))

    heap = getHeapsAddress(dbg)
    print("heap 堆地址: {}".format(hex(heap)))

    dbg.close()
```

**汇编Hook替换弹窗内容:** 通过钩子劫持技术，实现用户点击弹窗后，弹出我们自己的版权信息。
```Python
from LyScript32 import MyDebug

# 传入汇编列表,写出到内存
def assemble(dbg, address=0, asm_list=[]):
    asm_len_count = 0
    for index in range(0,len(asm_list)):
        # 写出到内存
        dbg.assemble_at(address, asm_list[index])
        # print("地址: {} --> 长度计数器: {} --> 写出: {}".
	# format(hex(address + asm_len_count), asm_len_count,asm_list[index]))
        # 得到asm长度
        asm_len_count = dbg.assemble_code_size(asm_list[index])
        # 地址每次递增
        address = address + asm_len_count

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 找到MessageBoxA
    messagebox_address = dbg.get_module_from_function("user32.dll","MessageBoxA")
    print("MessageBoxA内存地址 = {}".format(hex(messagebox_address)))

    # 分配空间
    HookMem = dbg.create_alloc(1024)
    print("自定义内存空间: {}".format(hex(HookMem)))

    # 写出FindWindowA内存地址,跳转地址
    asm = [
        f"push {hex(HookMem)}",
        "ret"
    ]

    # 将列表中的汇编指令写出到内存
    assemble(dbg,messagebox_address,asm)

    # 定义两个变量,存放字符串
    MsgBoxAddr = dbg.create_alloc(512)
    MsgTextAddr = dbg.create_alloc(512)

    # 填充字符串内容
    # lyshark 标题
    txt = [0x6c, 0x79, 0x73, 0x68, 0x61, 0x72, 0x6b]
    # 内容 lyshark.com
    box = [0x6C, 0x79, 0x73, 0x68, 0x61, 0x72, 0x6B, 0x2E, 0x63, 0x6F, 0x6D]

    for txt_count in range(0,len(txt)):
        dbg.write_memory_byte(MsgBoxAddr + txt_count, txt[txt_count])

    for box_count in range(0,len(box)):
        dbg.write_memory_byte(MsgTextAddr + box_count, box[box_count])

    print("标题地址: {} 内容: {}".format(hex(MsgBoxAddr),hex(MsgTextAddr)))

    # 此处是MessageBox替换后的片段
    PatchCode =\
    [
        "mov edi, edi",
        "push ebp",
        "mov ebp,esp",
        "push -1",
        "push 0",
        "push dword ptr ss:[ebp+0x14]",
        f"push {hex(MsgBoxAddr)}",
        f"push {hex(MsgTextAddr)}",
        "push dword ptr ss:[ebp+0x8]",
        "call 0x76030E20",
        "pop ebp",
        "ret 0x10"
    ]

    # 写出到自定义内存
    assemble(dbg, HookMem, PatchCode)

    print("地址已被替换,可以运行了.")
    dbg.set_debug("Run")
    dbg.set_debug("Run")

    dbg.close()
```

**计算HASH并生成报告:** 通过运用第三方库`xlsxwriter`实现读入指定内存片段生成`hash`特征，并写出成EXCEL表格。
```Python
import hashlib
import time
import zlib,binascii
from LyScript32 import MyDebug
import xlsxwriter

# 计算哈希
def calc_hash(dbg, rva,size):
    read_list = bytearray()
    ref_hash = { "va": None, "size": None, "md5":None, "sha256":None, "sha512":None, "crc32":None }

    # 得到基地址
    base = dbg.get_local_module_base()

    # 读入数据
    for index in range(0,size):
        readbyte = dbg.read_memory_byte(base + rva + index)
        read_list.append(readbyte)

    # 计算特征
    md5hash = hashlib.md5(read_list)
    sha512hash = hashlib.sha512(read_list)
    sha256hash = hashlib.sha256(read_list)
    # crc32hash = binascii.crc32(read_list) & 0xffffffff

    ref_hash["va"] = hex(base+rva)
    ref_hash["size"] = size
    ref_hash["md5"] = md5hash.hexdigest()
    ref_hash["sha256"] = sha256hash.hexdigest()
    ref_hash["sha512"] = sha512hash.hexdigest()
    ref_hash["crc32"] = hex(zlib.crc32(read_list))
    return ref_hash

if __name__ == "__main__":
    dbg = MyDebug()
    connect = dbg.connect()

    # 打开一个被调试进程
    dbg.open_debug("D:\\Win32Project.exe")

    # 传入相对地址,计算计算字节
    ref = calc_hash(dbg,0x19fd,10)
    print(ref)

    ref2 = calc_hash(dbg,0x1030,26)
    print(ref2)

    ref3 = calc_hash(dbg,0x15EB,46)
    print(ref3)

    ref4 = calc_hash(dbg,0x172B,8)
    print(ref4)

    # 写出表格
    workbook = xlsxwriter.Workbook("pe_hash.xlsx")
    worksheet = workbook.add_worksheet()

    headings = ["VA地址", "计算长度", "MD5", "SHA256", "SHA512","CRC32"]
    data = [
        [ref.get("va"),ref.get("size"),ref.get("md5"),
	ref.get("sha256"),ref.get("sha512"),ref.get("crc32")],
        [ref2.get("va"), ref2.get("size"), ref2.get("md5"),
	ref2.get("sha256"), ref2.get("sha512"), ref2.get("crc32")],
        [ref3.get("va"), ref3.get("size"), ref3.get("md5"),
	ref3.get("sha256"), ref3.get("sha512"), ref3.get("crc32")],
        [ref4.get("va"), ref4.get("size"), ref4.get("md5"),
	ref4.get("sha256"), ref4.get("sha512"), ref4.get("crc32")]
    ]

    # 定义表格样式
    head_style = workbook.add_format({"bold": True, "align": "center", "fg_color": "#D7E4BC"})
    worksheet.set_column("A1:F1", 15)

    # 逐条写入数据
    worksheet.write_row("A1", headings, head_style)
    for i in range(0, len(data)):
        worksheet.write_row("A{}".format(i + 2), data[i])

    # 添加条形图，显示前十个元素
    chart = workbook.add_chart({"type": "line"})
    chart.add_series({
        "name": "=Sheet1!$B$1",              # 图例项
        "categories": "=Sheet1!$A$2:$A$10",  # X轴 Item名称
        "values": "=Sheet1!$B$2:$B$10"       # X轴Item值
    })
    chart.add_series({
        "name": "=Sheet1!$C$1",
        "categories": "=Sheet1!$A$2:$A$10",
        "values": "=Sheet1!$C$2:$C$10"
    })
    chart.add_series({
        "name": "=Sheet1!$D$1",
        "categories": "=Sheet1!$A$2:$A$10",
        "values": "=Sheet1!$D$2:$D$10"
    })

    # 添加柱状图标题
    chart.set_title({"name": "计算HASH统计图"})
    # chart.set_style(8)

    chart.set_size({'width': 500, 'height': 250})
    chart.set_legend({'position': 'top'})

    # 在F2处绘制
    worksheet.insert_chart("H2", chart)
    workbook.close()

    # 关闭被调试进程
    time.sleep(1)
    dbg.close_debug()
    dbg.close()
```

**Tkinter组合图形化:** 与TK图形接口组合使用，用户传入特征码后，自动搜索特征值，找到了将自动同步到列表框内。
```Python
from LyScript32 import MyDebug
from tkinter import *

dbg = MyDebug()
dbg.connect()

def Scan():
    print("得到输入框内特征: {}".format(e1.get()))

    if len(e1.get()) == 0:
        return

    ref = dbg.scan_memory_all(e1.get())
    # 往列表里添加数据
    for item in ref:
        theLB.insert("end", hex(item))

if __name__ == "__main__":
    root = Tk()

    root.title("特征码搜索工具")

    Label(root, text="输入特征值:").grid(row=0, column=0)

    e1 = Entry(root)
    e1.grid(row=0, column=1, padx=10, pady=5)

    Button(root, text="搜索特征", width=10, command=Scan).grid(row=3, column=0, sticky=W, padx=10, pady=5)

    # 创建一个空列表
    theLB = Listbox(root)
    theLB.grid(row=20, column=0, sticky=W, padx=10, pady=5)

    # 设置窗口大小变量
    width = 400
    height = 270

    # 窗口居中
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size_geo)

    mainloop()
    dbg.close()
```

**通过PEB结构解析堆内存段:** 当我们得到了堆的起始地址以后，那么对堆地址进行深度解析就变得很容易了，只需要填充特定的结构体即可并格式化即可，如下首先实现解析堆内段这个功能。
```Python
from LyScript32 import MyDebug
import struct
import string

DEBUG = False

class _PEB():
    def __init__(self, dbg):
        # 内置函数得到进程PEB
        self.base = dbg.get_peb_address(dbg.get_process_id())
        self.PEB = bytearray()

        # 填充前488字节
        for index in range(0, 488):
            readbyte = dbg.read_memory_byte(self.base + index)
            self.PEB.append(readbyte)

        index = 0x018
        self.ProcessHeap = self.PEB[index:index + 4]

    def get_ProcessHeaps(self):
        pack = struct.unpack('<L', bytes(self.ProcessHeap))
        return pack[0]

class GrabHeap():
    def __init__(self, dbg, heap_addr):
        # 内置函数得到进程PEB
        self.base = dbg.get_peb_address(dbg.get_process_id())
        self.address = heap_addr
        self.buffer = bytearray()

    def grapHeap(self):
        for idx in range(0, 1416):
            readbyte = dbg.read_memory_byte(self.address + idx)
            self.buffer.append(readbyte)

        index = 0x8
        (self.Signature, self.Flags, self.ForceFlags, self.VirtualMemoryThreshold, \
         self.SegmentReserve, self.SegmentCommit, self.DeCommitFreeBlockThreshold, \
	 self.DeCommitTotalBlockThreshold, \
         self.TotalFreeSize, self.MaximumAllocationSize, self.ProcessHeapListIndex, \
	 self.HeaderValidateLength, \
         self.HeaderValidateCopy, self.NextAvailableTagIndex, self.MaximumTagIndex, self.TagEntries, \
         self.UCRSegments, self.UnusedUnCommittedRanges, self.AlignRound, self.AlignMask) = \
            struct.unpack("LLLLLLLLLLHHLHHLLLLL", self.buffer[index:index + (0x50 - 8)])

        index += 0x50 - 8
        self.VirtualAllocedBlock = struct.unpack("LL", self.buffer[index:index + 8])

        index += 8
        self._Segments = struct.unpack("L" * 64, self.buffer[index:index + 64 * 4])
        index += 64 * 4
        self.FreeListInUseLong = struct.unpack("LLLL", self.buffer[index:index + 16])
        index += 16
        (self.FreeListInUseTerminate, self.AllocatorBackTraceIndex) = \
	struct.unpack("HH", self.buffer[index: index + 4])
        index += 4
        (self.Reserved1, self.LargeBlocksIndex) = struct.unpack("LL", self.buffer[index: index + 8])

    def get_Signature(self):
        return self.Signature

# 段
class Segment():
    def __init__(self, dbg, heap_addr):
        self.address = heap_addr
        self.buffer = bytearray()

        # AVOID THE ENTRY ITSELF
        self.address += 8
        for idx in range(0, 0x34):
            readbyte = dbg.read_memory_byte(self.address + idx)
            self.buffer.append(readbyte)

        (self.Signature, self.Flags, self.Heap, self.LargestUnCommitedRange, self.BaseAddress, \
         self.NumberOfPages, self.FirstEntry, self.LastValidEntry, self.NumberOfUnCommittedPages, \
         self.NumberOfUnCommittedRanges, self.UnCommittedRanges, self.AllocatorBackTraceIndex, \
         self.Reserved, self.LastEntryInSegment) = struct.unpack("LLLLLLLLLLLHHL", self.buffer)

        if DEBUG == True:
            print("SEGMENT: {} Sig: {}".format(hex(self.address), hex(self.Signature)))

            print("Heap: {} LargetUncommit {} Base: {}"
                  .format(hex(self.Heap), hex(self.LargestUnCommitedRange), hex(self.BaseAddress)))

            print("NumberOfPages {} FirstEntry: {} LastValid: {}"
                  .format(hex(self.NumberOfPages), hex(self.FirstEntry), hex(self.LastValidEntry)))

            print("Uncommited: {}".format(self.UnCommittedRanges))

            Pages = []
            Items = bytearray()
            if self.UnCommittedRanges:
                addr = self.UnCommittedRanges
                if addr != 0:
                    # 读入内存
                    for idx in range(0, 0x10):
                        readbyte = dbg.read_memory_byte(self.address + idx)
                        Items.append(readbyte)

                    (C_Next, C_Addr, C_Size, C_Filler) = struct.unpack("LLLL", Items)
                    print("Memory: {} Address: {} (a: {}) Size: {}"
                          .format(hex(self.address), hex(C_Next), C_Addr, C_Size))
                    Pages.append(C_Addr + C_Size)
                    addr = C_Next

if __name__ == "__main__":
    dbg = MyDebug()
    connect = dbg.connect()

    # 初始化PEB填充结构
    peb = _PEB(dbg)

    # 堆地址
    process_heap = peb.get_ProcessHeaps()
    print("堆地址: {}".format(hex(process_heap)))

    # 定义Segment
    heap = Segment(dbg, process_heap)

    # 输出内容
    print("Signature = {}".format(heap.Signature))
    print("Flags = {}".format(heap.Flags))
    print("Heap = {}".format(heap.Heap))

    # 初始化堆
    heap = GrabHeap(dbg, process_heap)
    heap.grapHeap()

    # 获取Signature
    Signature = heap.get_Signature()
    print("Signature = {}".format(hex(Signature)))

    dbg.close()
```

**通过PEB结构解析低内存堆:** 低内存堆的输出也可以使用如上方法实现，只是在输出是需要解析的结构体程序稍多一些，但总体上原理与上方代码一致。
```Python
from LyScript32 import MyDebug
import struct
import string

# 读内存
def readMemory(address,size):
    ref_buffer = bytearray()
    for idx in range(0, size):
        readbyte = dbg.read_memory_byte(address + idx)
        ref_buffer.append(readbyte)
    return ref_buffer

def readLong(address):
    return dbg.read_memory_dword(address)

# 得到进程PEB
class _PEB():
    def __init__(self, dbg):
        # 内置函数得到进程PEB
        self.base = dbg.get_peb_address(dbg.get_process_id())
        self.PEB = bytearray()
        self.PEB = readMemory(self.base,488)

        # 通过偏移找到ProcessHeap
        index = 0x018
        self.ProcessHeap = self.PEB[index:index + 4]

    def get_ProcessHeaps(self):
        pack = struct.unpack('<L', bytes(self.ProcessHeap))
        return pack[0]

class UserMemoryCache():
    def __init__(self, addr, mem):
        self.address = addr
        (self.Next, self.Depth, self.Sequence, self.AvailableBlocks,\
         self.Reserved) = struct.unpack("LHHLL", mem[ 0 : 16 ])

class Bucket():
    def __init__(self, addr, mem):
        self.address = addr
        (self.BlockUnits, self.SizeIndex, Flag) =\
         struct.unpack("HBB", mem[:4])

        # 从理论上讲，这是标志的分离方式
        self.UseAffinity = Flag & 0x1
        self.DebugFlags  = (Flag >1) & 0x3

# 低内存堆
class LFHeap():
    def __init__(self, addr):
        mem = readMemory(addr, 0x300)
        index = 0
        self.address = addr

        (self.Lock, self.field_4, self.field_8, self.field_c,\
         self.field_10, field_14, self.SubSegmentZone_Flink,
         self.SubSegmentZone_Blink, self.ZoneBlockSize,\
         self.Heap, self.SegmentChange, self.SegmentCreate,\
         self.SegmentInsertInFree, self.SegmentDelete, self.CacheAllocs,\
         self.CacheFrees) = struct.unpack("L" * 0x10, mem[index:index+0x40])

        index += 0x40
        self.UserBlockCache = []
        for a in range(0,12):
            umc = UserMemoryCache(addr + index, mem[index:index + 0x10])
            index += 0x10
            self.UserBlockCache.append(umc)

        self.Buckets = []
        for a in range(0, 128):
            entry = mem[index: index + 4]
            b = Bucket(addr + index, entry)
            index = index + 4
            self.Buckets.append(b)

if __name__ == "__main__":
    dbg = MyDebug()
    connect = dbg.connect()

    # 初始化PEB填充结构
    peb = _PEB(dbg)

    # 堆地址
    process_heap = peb.get_ProcessHeaps()
    print("堆地址: {}".format(hex(process_heap)))

    # 定义低内存堆类
    lf_heap = LFHeap(process_heap)

    print("堆内存锁: {}".format(hex(lf_heap.Lock)))
    print("堆地址: {}".format(hex(lf_heap.Heap)))
    print("堆分配: {}".format(hex(lf_heap.CacheAllocs)))

    # 循环输出block
    for index in lf_heap.UserBlockCache:
        print("地址: {} --> 下一个地址: {}".format(hex(index.address),hex(index.Next)))

    for index in lf_heap.Buckets:
        print(index.SizeIndex,index.DebugFlags)

    dbg.close()
```
