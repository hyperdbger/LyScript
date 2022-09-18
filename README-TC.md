# x64dbg 自動化控制插件

<br>
<div align=center>
	<img width="150" src="https://cdn.lyshark.com/archive/LyScript/lyscript_png.jpg" />
<!--
  <img width="100" src="https://cdn.lyshark.com/archive/LyScript/bug_black.png"/><tr>
    <img width="100" src="https://cdn.lyshark.com/archive/LyScript/python.png"/>
-->
 <br><br>
  
  [简体中文](README.md) | [繁體中文(中國)](README-TC.md) | [ENGLISH](README-EN.md) | [русский язык ](README-RU.md)

  <br>
  
[![Build status](https://cdn.lyshark.com/archive/LyScript/build.svg)](https://github.com/lyshark/LyScript) [![Open Source Helpers](https://cdn.lyshark.com/archive/LyScript/users.svg)](https://github.com/lyshark/LyScript) [![Crowdin](https://cdn.lyshark.com/archive/LyScript/email.svg)](mailto:me@lyshark.com) [![Download x64dbg](https://cdn.lyshark.com/archive/LyScript/x64dbg.svg)](https://github.com/lyshark/LyScript/releases/tag/LyScript) [![OSCS Status](https://www.oscs1024.com/platform/badge/lyshark/LyScript.svg?size=small)](https://www.oscs1024.com/project/lyshark/LyScript?ref=badge_small)

[![python3](https://cdn.lyshark.com/archive/LyScript/python3.svg)](https://github.com/lyshark/LyScript) [![platform](https://cdn.lyshark.com/archive/LyScript/platform.svg)](https://github.com/lyshark/LyScript) [![lyscriptver](https://cdn.lyshark.com/archive/LyScript/lyscript_version.svg)](https://github.com/lyshark/LyScript)

<br><br>
一款 x64dbg 自动化控制插件，通过Python控制x64dbg的行为，实现远程动态调试，解决了逆向工作者分析程序，反病毒人员脱壳，漏洞分析者寻找指令片段，原生脚本不够强大的问题，通过与Python相结合利用Python语法的灵活性以及其丰富的第三方库，加速漏洞利用程序的开发，辅助漏洞挖掘以及恶意软件分析。
  
</div>
<br>

Python 包請安裝與插件一致的版本，在cmd命令行下執行pip命令即可安裝，推薦兩個包全部安裝。

- 安裝標準包：`pip install LyScript32` 或者`pip install LyScript64`
- 安裝擴展包：`pip install LyScriptTools32` 或者`pip install LyScriptTools64`

其次您需要手動下載對應`x64dbg`版本的驅動文件，並放入指定的`plugins`目錄下。

- 調試器下載：<a href="https://sourceforge.net/projects/x64dbg/files/snapshots/snapshot_2022-09-11_15-59.zip/download">snapshot_2022-09-11_15-59.zip</a>
- 插件下載：<a href="https://github.com/lyshark/LyScript/raw/master/plugins/LyScript32-1.0.13.zip">LyScript32-1.0.13 (32位插件)</a> 或者<a href="https://github.com/lyshark/LyScript/raw/master/plugins/LyScript64-1.0.13.zip">LyScript64-1.0.13 (64位插件)</a>

插件下載好以後，請將該插件複製到x64dbg的plugins目錄下，程序運行後會自動加載插件。

![image](https://user-images.githubusercontent.com/52789403/185293618-68102ea6-8c37-493e-8be3-ca46eca0f0b5.png)

當插件加載成功後，會在日誌位置看到具體的綁定信息以及輸出調試，該插件並不會在插件欄顯示。

![image](https://user-images.githubusercontent.com/52789403/161062658-0452fe0c-3e11-4df4-a83b-b026f74884d0.png)

如果需要遠程調試，則只需要在初始化`MyDebug()`類時傳入對端IP地址即可，如果不填寫參數則默認使用`127.0.0.1`地址，請確保對端放行了`6589`端口，否則無法連接。

![image](https://user-images.githubusercontent.com/52789403/161062393-df04aabb-2d70-4434-80b9-a46974bccf8a.png)

運行x64dbg程序並手動載入需要分析的可執行文件，然後我們可以通過`connect()`方法連接到調試器，連接後會創建一個持久會話直到python腳本結束則連接會被強制斷開，在此期間可調用`is_connect()`檢查該鏈接是否還存在，具體代碼如下所示。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	# 初始化
	dbg = MyDebug()

	# 連接到調試器
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	# 檢測套接字是否還在
	ref = dbg.is_connect()
	print("是否在連接: ", ref)

	dbg.close()
```
<br><br>

### 寄存器系列函數

**get_register():** 該函數主要用於實現，對特定寄存器的獲取操作，用戶需傳入需要獲取的寄存器名字即可。

- 參數1：傳入寄存器字符串

可用範圍："DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI","ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP", "CIP", "CSP", "CAX", "CBX", "CCX", "CDX", "CDI", "CSI", "CBP", "CFLAGS"

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eax = dbg.get_register("eax")
	ebx = dbg.get_register("ebx")

	print("eax = {}".format(hex(eax)))
	print("ebx = {}".format(hex(ebx)))

	dbg.close()
```
如果您使用的是64位插件，則寄存器的支持範圍將變為E系列加R系列。

可用範圍擴展： "DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI", "ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP", "RAX", "RBX", "RCX", "RDX", "RSI", "SIL", "RDI", "DIL", "RBP", "BPL", "RSP", "SPL", "RIP", "R8", "R8D", "R8W", "R8B", "R9", "R9D", "R9W", "R9B", "R10", "R10D", "R10W", "R10B", "R11", "R11D", "R11W", "R11B", "R12", "R12D", "R12W", "R12B", "R13", "R13D", "R13W", "R13B", "R14", "R14D", "R14W", "R14B", "R15", "R15D", "R15W", "R15B"

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
	print("獲取R系列寄存器: {}".format(hex(r8)))

	dbg.close()
```

**set_register():** 該函數實現設置指定寄存器參數，同理64位將支持更多寄存器的參數修改。

- 參數1：傳入寄存器字符串
- 參數2：十進制數值

可用範圍："DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI", "ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP"

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eax = dbg.get_register("eax")
		
	dbg.set_register("eax",100)

	print("eax = {}".format(hex(eax)))

	dbg.close()
```

**get_flag_register():** 用於獲取某個標誌位參數，返回值只有真或者假。

- 參數1：寄存器字符串

可用寄存器範圍："ZF", "OF", "CF", "PF", "SF", "TF", "AF", "DF", "IF"

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	cf = dbg.get_flag_register("cf")
	print("標誌: {}".format(cf))
		
	dbg.close()
```

**set_flag_register():** 用於設置某個標誌位參數，返回值只有真或者假。
 
- 參數1：寄存器字符串
- 參數2：[ 設置為真True] / [設置為假False]

可用寄存器範圍："ZF", "OF", "CF", "PF", "SF", "TF", "AF", "DF", "IF"

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

### 調試系列函數

**set_debug():** 用於影響調試器，例如前進一次，後退一次，暫停調試，終止等。

- 參數1: 傳入需要執行的動作

可用動作範圍：[暫停Pause] [運行Run] [步入StepIn] [步過StepOut] [到結束StepOver] [停止Stop] [等待Wait]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	while True:
	dbg.set_debug("StepIn")
			
	eax = dbg.get_register("eax")
			
	if eax == 0:
	print("找到了")
	break
			
	dbg.close()
```

**set_debug_count():** 該函數是`set_debug()`函數的延續，目的是執行自動步過次數。

- 參數1：傳入需要執行的動作
- 參數2：執行重複次數

可用動作範圍：[暫停Pause] [運行Run] [步入StepIn] [步過StepOut] [到結束StepOver] [停止Stop] [等待Wait]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	dbg.set_debug_count("StepIn",10)

	dbg.close()
```

**is_debugger() /is_running()/is_run_locked():**`is_debugger`可用於驗證當前調試器是否處於調試狀態，`is_running`則用於驗證是否在運行，`is_run_locked()`用於檢查調試器是否被鎖定(暫停)。

- 無參數傳遞

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

**set_breakpoint():** 設置斷點與取消斷點進行了分離，設置斷點只需要傳入十進制內存地址。

- 參數1：傳入內存地址（十進制）
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	ref = dbg.set_breakpoint(eip)

	print("設置狀態: {}".format(ref))
	dbg.close()
```

**delete_breakpoint():** 該函數傳入一個內存地址，可取消一個內存斷點。

- 參數1：傳入內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	ref = dbg.set_breakpoint(eip)
	print("設置狀態: {}".format(ref))

	del_ref = dbg.delete_breakpoint(eip)
	print("取消狀態: {}".format(del_ref))

	dbg.close()
```

**check_breakpoint():** 用於檢查下過的斷點是否被命中，命中返回True否則返回False。

- 參數1：傳入內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	ref = dbg.set_breakpoint(eip)
	print("設置狀態: {}".format(ref))

	is_check = dbg.check_breakpoint(4134331)
	print("是否命中: {}".format(is_check))

	dbg.close()
```

**get_all_breakpoint():** 用於獲取當前調試程序中，所有下過的斷點信息，包括是否開啟，命中次數等。

- 無參數傳遞

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	ref = dbg.get_all_breakpoint()
	print(ref)
	dbg.close()
```

**set_hardware_breakpoint():** 用於設置一個硬件斷點，硬件斷點在32位系統中最多設置4個。

- 參數1：內存地址（十進制）
- 參數2：斷點類型

斷點類型可用範圍：[類型0 = HardwareAccess / 1 = HardwareWrite / 2 = HardwareExecute]

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

**delete_hardware_breakpoint():** 用於刪除一個硬件斷點，只需要傳入地址即可，無需傳入類型。

- 參數1：內存地址（十進制）

斷點類型可用範圍：[類型0 = HardwareAccess / 1 = HardwareWrite / 2 = HardwareExecute]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug(address="127.0.0.1",port=6666)
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")

	ref = dbg.set_hardware_breakpoint(eip,2)
	print(ref)

	# 刪除斷點
	ref = dbg.delete_hardware_breakpoint(eip)
	print(ref)

	dbg.close()
```

**is_bp_disable():** 該函數用於驗證指定地址處BP斷點是否被禁用。

- 參數1：內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	is_false = dbg.is_bp_disable(eip)
	print("bp斷點狀態: {}".format(is_false))

	dbg.close()
```

**get_xref_count_at():** 獲取指定內存地址位置處交叉引用計數。

- 參數1：內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	types = dbg.get_xref_count_at(eip)
	print("引用計數: {}".format(types))

	dbg.close()
```

**get_function_type_at():** 獲取指定內存地址位置處函數類型，函數`FUNCTYPE`枚舉類型。

- 參數1：內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	類型 = dbg.get_function_type_at(eip)
	print("函數類型：{}".format(types))

	如果（類型 == 0）：
	打印（“FUNC_NONE”）
	elif（類型 == 1）：
	打印（“FUNC_BEGIN”）
	elif（類型 == 2）：
	打印（“FUNC_MIDDLE”）
	elif（類型 == 3）：
	打印（“FUNC_END”）
	elif（類型 == 4）：
	打印（“FUNC_SINGLE”）
	別的：
	打印（“錯誤”）

	dbg.close()
```

**get_bpx_type_at():** 獲取指定地址處BP斷點類型，類型`BPXTYPE`枚舉。

- 參數1：內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	types = dbg.get_bpx_type_at(eip)
	print("BPX類型: {}".format(types))

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

**get_xref_type_at():** 得到指定內存地址位置處交叉引用類型，枚舉`XREFTYPE`類型。

- 參數1：內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態：{}".format(connect_flag))

	eip = dbg.get_register("eip")

	類型 = dbg.get_xref_type_at(eip)
	print("引用類型：{}".format(types))

	如果（類型 == 0）：
	打印（“XREF_NONE”）
	elif（類型 == 1）：
	打印（“XREF_DATA”）
	elif（類型 == 2）：
	打印（“XREF_JMP”）
	elif（類型 == 3）：
	打印（“XREF_CALL”）
	別的：
	打印（“錯誤”）

	dbg.close()
```
<br>

### 模塊系列函數

**get_module_base():** 該函數可用於獲取程序載入的指定一個模塊的基地址。

- 參數1：模塊名字符串

```Python
	from LyScript32 import MyDebug

	if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
		
	user32_base = dbg.get_module_base("user32.dll")
	print(user32_base)

	dbg.close()
```

**get_all_module():** 用於輸出當前加載程序的所有模塊信息，以字典的形式返回。

- 參數：無參數

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

**get_local_() 系列函數:** 獲取當前EIP所在模塊基地址，長度，以及內存屬性，此功能無參數傳遞，獲取的是當前EIP所指向模塊的數據。

- dbg.get_local_base() 獲取模塊基地址
- dbg.get_local_size() 獲取模塊長度
- dbg.get_local_protect() 獲取模塊保護屬性

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

**get_module_from_function():** 獲取指定模塊中指定函數的內存地址，可用於驗證當前程序在內存中指定函數的虛擬地址。

- 參數1：模塊名
- 參數2：函數名

成功返回地址，失敗返回false

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

**get_module_from_import():** 獲取當前程序中指定模塊的導入表信息，輸出為列表嵌套字典。

- 參數1：傳入模塊名稱

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

**get_module_from_export():** 該函數用於獲取當前加載程序中的導出表信息。

- 參數1：傳入模塊名

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

**get_section():** 該函數用於輸出主程序中的節表信息。

- 無參數傳遞

```Python
from LyScript32 import MyDebug
 
if __name__ == "__main__":
	dbg = MyDebug(address="127.0.0.1",port=6666)
	connect_flag = dbg.connect()

	ref = dbg.get_section()
	print(ref)

	dbg.close()
```

**get_base_from_address():** 根據傳入的內存地址得到該模塊首地址。

- 參數1：傳入內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	eip = dbg.get_register("eip")

	ref = dbg.get_base_from_address(eip)
	print("模塊首地址: {}".format(hex(ref)))
```

**get_base_from_name():** 根據傳入的模塊名得到該模塊所在內存首地址。

- 參數1：傳入模塊名

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	eip = dbg.get_register("eip")

	ref_base = dbg.get_base_from_name("win32project.exe")
	print("模塊首地址: {}".format(hex(ref_base)))

	dbg.close()
```

**get_oep_from_name():** 根據傳入的模塊名，獲取該模塊實際裝載OEP位置。

- 參數1：傳入模塊名

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	oep = dbg.get_oep_from_name("win32project.exe")
	print(hex(oep))

	dbg.close()
```

**get_oep_from_address():** 根據傳入內存地址，得到該地址模塊的OEP位置。

- 參數1：傳入內存地址

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

**get_section_from_module_name():** 用戶可傳入當前載入的模塊名，即可直接取出指定模塊的節表信息。

- 參數1：模塊名（字符串）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	section_user32 = dbg.get_section_from_module_name("user32.dll")
	print(section_user32)

	section_ntdll = dbg.get_section_from_module_name("ntdll.dll")
	print(section_ntdll)

	dbg.close()
```

**size_from_address():** 傳入一個模塊的基地址得到該模塊佔用總大小。

- 參數1：模塊地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	base = dbg.get_local_base()
	print("模塊基地址: {}".format(hex(base)))

	size = dbg.size_from_address(base)
	print("模塊長度: {}".format(size))

	dbg.close()
```

**size_from_name():** 傳入模塊名稱得到模塊佔用總大小。

- 參數1：模塊名（字符串）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	size = dbg.size_from_name("win32.exe")
	print("長度: {}".format(size))

	dbg.close()
```

**section_count_from_name():** 傳入模塊名稱得到模塊有多少個節區。

- 參數1：模塊名（字符串）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	size = dbg.section_count_from_name("win32.exe")
	print("節區個數: {}".format(size))

	dbg.close()
```

**section_count_from_address():** 傳入模塊基址得到模塊有多少個節區。

- 參數1：模塊地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	base = dbg.get_local_base()
	print("模塊基地址: {}".format(hex(base)))

	size = dbg.section_count_from_address(base)
	print("節個數: {}".format(size))

	dbg.close()
```

**path_from_name():** 傳入模塊名稱得到模塊路徑。

- 參數1：模塊名（字符串）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	size = dbg.path_from_name("win32.exe")
	print("模塊路徑: {}".format(size))

	dbg.close()
```

**path_from_address():** 傳入模塊地址得到模塊路徑。

- 參數1：模塊地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	base = dbg.get_local_base()
	print("模塊基地址: {}".format(hex(base)))

	path = dbg.path_from_address(base)
	print("模塊路徑: {}".format(path))

	dbg.close()
```

**name_from_address():** 傳入模塊地址得到模塊名稱。

- 參數1：模塊地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	base = dbg.get_local_base()
	print("模塊基地址: {}".format(hex(base)))

	path = dbg.name_from_address(base)
	print("模塊名: {}".format(path))

	dbg.close()
```

**get_window_handle():** 取出自身進程模塊句柄。

- 參數：無參數傳遞

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	base = dbg.get_window_handle()
	print("進程句柄: {}".format(base))

	dbg.close()
```

**get_module_at():** 獲取指定內存地址處模塊名，此處得到的模塊名無後綴。

- 參數1：模塊地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	ref = dbg.get_module_at(eip)
	print("模塊名: {}".format(ref))

	dbg.close()
```

**get_local_module():** 該系列函數可用於得到當前載入程序停留EIP位置的模塊詳細信息。

- get_local_module_size() 獲取當前程序的大小
- get_local_module_section_Count() 獲取自身節數量
- get_local_module_path() 獲取被調試程序完整路徑
- get_local_module_name() 獲取自身模塊名
- get_local_module_entry() 獲取自身模塊入口
- get_local_module_base() 獲取自身模塊基地址

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	print("程序大小: {}".format( dbg.get_local_module_size()))
	print("節個數: {}".format(dbg.get_local_module_section_Count()))
	print("完整路徑: {}".format(dbg.get_local_module_path()))
	print("模塊名: {}".format(dbg.get_local_module_name()))
	print("模塊入口: {}".format(dbg.get_local_module_entry()))
	print("模塊基地址: {}".format(dbg.get_local_module_base()))

	dbg.close()
```
<br>

### 內存系列函數

**read_memory_() 系列函數:** 讀內存系列函數，包括ReadByte,ReadWord,ReadDword 三種格式，在64位下才支持Qword

- 參數1：需要讀取的內存地址（十進制）

目前支持：
- read_memory_byte() 讀字節
- read_memory_word() 讀word
- read_memory_dword() 讀dword
- read_memory_qword() 讀qword （僅支持64位）
- read_memory_ptr() 讀指針

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

**write_memory_() 系列函數:** 寫內存系列函數，WriteByte,WriteWord,WriteDWORD,WriteQword

- 參數1：需要寫入的內存
- 參數2：需要寫入的byte字節

目前支持：
- write_memory_byte() 寫字節
- write_memory_word() 寫word
- write_memory_dword() 寫dword
- write_memory_qword() 寫qword （僅支持64位）
- write_memory_ptr() 寫指針

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

**scan_memory_one():** 實現了內存掃描，當掃描到第一個符合條件的特徵時，自動輸出。

- 參數1：特徵碼字段

這個函數需要注意，如果我們的x64dbg工具停在系統領空，則會默認搜索系統領空下的特徵，如果想要搜索程序領空裡面的數據，需要先將EIP切過去在操作。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	ref = dbg.scan_memory_one("ff 25")
	print(ref)
	dbg.close()
```

**scan_memory_all():** 實現了掃描所有符合條件的特徵字段，找到後返回一個列表。

- 參數1：特徵碼字段

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

**scan_memory_any():** 該函數可實現對特定位置，向下掃描特定長度的特徵字段。

- 參數1：掃描起始地址（十進制）
- 參數2：掃描長度（十進制）
- 參數3：特徵碼字段

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	# 初始化
	dbg = MyDebug()

	# 連接到調試器
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	# 任意地址掃描
	eip = dbg.get_register("eip")
	ref = dbg.scan_memory_any(eip,1024,"8b 50 04 8b fe")
	print("得到掃描結果: {}".format(hex(ref)))

	dbg.close()
```

**get_local_protect():** 獲取內存屬性傳值，該函數進行更新，取消了只能得到EIP所指的位置的內存屬性，用戶可隨意檢測。

- 參數1：內存地址（十進制）

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

**set_local_protect():** 新增設置內存屬性函數，傳入eip內存地址，設置屬性32，以及設置內存長度1024即可。

- 參數1：內存地址（十進制）
- 參數2：權限類型（32=執行/讀取30=執行2=讀取/寫入）
- 參數3：屬性長度（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
		
	eip = dbg.get_register("eip")
	print(eip)

	b = dbg.set_local_protect(eip,32,1024)
	print("設置屬性狀態: {}".format(b))

	dbg.close()
```

**get_local_page_size():** 用於獲取當前EIP所指領空下，內存pagesize分頁大小。

- 無參數傳遞

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	size = dbg.get_local_page_size()
	print("pagesize = {}".format(size))

	dbg.close()
```

**get_memory_section():** 該函數主要用於獲取內存映像中，當前調試程序的內存節表數據。

- 無參數傳遞
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ref = dbg.get_memory_section()
	print(ref)
	dbg.close()
```

**is_jmp_going_to_execute():** 判斷內存地址是否跳轉到可執行內存塊。

- 參數1：內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	flag = dbg.is_jmp_going_to_execute(eip)
	print("是否是跳轉(是否可執行): {}".format(flag))

	dbg.close()
```

**mem_find_base_addr():** 返回特定位置處內存模塊基地址和大小，以字典形式返回。

- 參數1：內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	dic = dbg.mem_find_base_addr(eip)

	print("內存基地址: {}".format(hex(dic.get("base"))))
	print("內存大小: {}".format(dic.get("size")))

	dbg.close()
```

**mem_get_page_size():** 得到指定位置處內存頁面長度。

- 參數1：內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	addr = dbg.mem_get_page_size(eip)

	print("內存頁面長度: {}".format(hex(addr)))

	dbg.close()
```

**mem_is_valid():** 驗證指定位置處內存地址是否可讀取。

- 參數1：內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	is_read = dbg.mem_is_valid(eip)
	print("內存地址屬性: {}".format(is_read))

	dbg.close()
```
<br>

### 堆棧系列函數

**create_alloc()：**`create_alloc()`可在遠程開闢一段堆空間，成功返回內存首地址。

- 參數1：開闢的堆長度（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ref = dbg.create_alloc(1024)
	print("開闢地址: ", hex(ref))

	dbg.close()
```

**delete_alloc()：**`delete_alloc()`用於註銷一個遠程堆空間。

- 參數1：傳入需要刪除的堆空間內存地址。

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ref = dbg.create_alloc(1024)
	print("開闢地址: ", hex(ref))

	flag = dbg.delete_alloc(ref)
	print("刪除狀態: ",flag)

	dbg.close()
```

**push_stack():** 將一個十進制數壓入堆棧中，默認在堆棧棧頂。

- 參數1：十進制數據

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ref = dbg.push_stack(10)

	print(ref)

	dbg.close()
```

**pop_stack():** pop函數用於從堆棧中推出一個元素，默認從棧頂彈出。

- 無參數傳遞

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	tt = dbg.pop_stack()
	print(tt)

	dbg.close()
```

**peek_stack():** peek則用於檢查堆棧內的參數，可設置偏移值，不設置則默認檢查第一個也就是棧頂。

- 參數1：十進制偏移

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	# 無參數檢查
	check = dbg.peek_stack()
	print(check)

	# 攜帶參數檢查
	check_1 = dbg.peek_stack(2)
	print(check_1)

	dbg.close()
```
<br>

### 進程線程系列函數

**get_thread_list():** 該函數可輸出當前進程所有在運行的線程信息。

- 無參數傳遞

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

**get_process_handle():** 用於獲取當前進程句柄信息。

- 無參數傳遞

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ref = dbg.get_process_handle()
	print(ref)

	dbg.close()
```

**get_process_id():** 用於獲取當前加載程序的PID

- 無參數傳遞

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ref = dbg.get_process_id()
	print(ref)

	dbg.close()
```

**get_teb_address() / get_peb_address() 系列函數:** 用於獲取當前進程環境塊，和線程環境快。

- get_teb_address() 傳入參數是線程ID
- get_peb_address() 傳入參數是進程ID

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

### 反彙編系列函數

**get_disasm_code():** 該函數主要用於對特定內存地址進行反彙編，傳入兩個參數。

- 參數1：需要反彙編的地址(十進制)
- 參數2：需要向下反彙編的長度

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	# 得到EIP位置
	eip = dbg.get_register("eip")

	# 反彙編前100行
	disasm_dict = dbg.get_disasm_code(eip,100)

	for ds in disasm_dict:
	print("地址: {} 反彙編: {}".format(hex(ds.get("addr")),ds.get("opcode")))

	dbg.close()
```

**get_disasm_one_code():** 在用戶指定的位置讀入一條彙編指令，用戶可根據需要對其進行判斷。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	print("EIP = {}".format(eip))

	disasm = dbg.get_disasm_one_code(eip)
	print("反彙編一條: {}".format(disasm))

	dbg.close()
```

**get_disasm_operand_code():** 用於獲取彙編指令中的操作數，例如`jmp 0x0401000`其操作數就是`0x0401000`。

- 參數1：傳入內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	print("EIP = {}".format(eip))

	opcode = dbg.get_disasm_operand_code(eip)
	print("操作數: {}".format(hex(opcode)))

	dbg.close()
```

**get_disasm_operand_size():** 用於得當前內存地址下彙編代碼的機器碼長度。

- 參數1：傳入內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	print("EIP = {}".format(eip))

	opcode = dbg.get_disasm_operand_size(eip)

	print("機器碼長度: {}".format(hex(opcode)))

	dbg.close()
```

**assemble_write_memory():** 實現了用戶傳入一段正確的彙編指令，程序自動將該指令轉為機器碼，並寫入到指定位置。

- 參數1：寫出內存地址（十進制）
- 參數2：寫出彙編指令

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	print(eip)

	ref = dbg.assemble_write_memory(eip,"mov eax,1")
	print("是否寫出: {}".format(ref))

	dbg.close()
```

**assemble_code_size():** 該函數實現了用戶傳入一個彙編指令，自動計算出該指令佔多少個字節。

- 參數1：彙編指令字符串

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ref = dbg.assemble_code_size("sub esp, 0x324")
	print(ref)

	dbg.close()
```

**get_branch_destination():** 獲取call或者是jx跳轉指令的跳轉地址。

- 參數1：獲取內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	print("當前EIP地址: {}".format(hex(eip)))

	value = dbg.get_branch_destination(eip)
	print("操作數: {}".format(hex(value)))

	dbg.close()
```

**get_disassembly():** 反彙編一條指令，此函數直接輸出調試其中看到的，包括符號。

- 參數1：獲取內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	print("當前EIP地址: {}".format(hex(eip)))

	dasm = dbg.get_disassembly(eip)
	print("反彙編一條: {}".format(dasm))

	dbg.close()
```

**assemble_at():** 彙編系列函數，傳入一條彙編指令，直接將指令寫出到內存。

- 參數1：獲取內存地址（十進制）
- 參數2：彙編指令（字符串）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	print("當前EIP地址: {}".format(hex(eip)))

	ref = dbg.assemble_at(eip,"nop")
	print("寫出狀態: {}".format(ref))

	dbg.close()
```

**disasm_fast_at():** 該函數同樣是反彙編一行並返回字典，但它可以獲取到更多有效參數。

- 參數1：獲取內存地址（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	print("當前EIP地址: {}".format(hex(eip)))

	dasm = dbg.disasm_fast_at(eip)
	print("地址: {}".format(hex(dasm.get("addr"))))
	print("彙編指令: {}".format(dasm.get("disasm")))
	print("彙編長度: {}".format(dasm.get("size")))
	print("是否分支: {}".format(dasm.get("is_branch")))
	print("是否call: {}".format(dasm.get("is_call")))
	print("類型: {}".format(dasm.get("type")))

	dbg.close()
```
<br>

### 其他系列函數

**set_comment_notes():** 給指定位置代碼增加一段註釋，如下演示在eip位置增加註釋。

- 參數1：註釋內存地址
- 參數2：註釋內容

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

**run_command_exec():** 執行內置命令，例如bp,dump等。

- 參數1：命令語句

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ref = dbg.run_command_exec("bp MessageBoxA")
	print(ref)

	dbg.close()
```

**set_loger_output():** 日誌的輸出尤為重要，該模塊提供了自定義日誌輸出功能，可將指定日誌輸出到x64dbg日誌位置。

- 參數1：日誌內容

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

**run_command_exe_ref():** 該函數是`run_command_exec()`的延申，其主要增加了傳出參數的功能，目前可傳出整數類型。

- 參數1：命令語句

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	ref = dbg.run_command_exe_ref("mod.base(eip)")
	print("返回參數: {}".format(hex(ref)))

	dbg.close()
```

**set_status_bar_message():** 該函數可實現在x64dbg底部狀態欄上面輸出一個用戶傳入的字符串。

- 參數1：輸出字符串
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	dbg.set_status_bar_message("EIP => {}".format(hex(eip)))

	dbg.close()
```

**script_loader():** 該函數接收用戶傳入的內置腳本所在路徑，並將該腳本加載到x64dbg中。

- 參數1：腳本路徑

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	flag = dbg.script_loader("d://x64dbg_script.txt")
	print("返回值: {}".format(flag))

	dbg.close()
```

**script_unloader():** 該函數用於關閉x64dbg中打開的腳本。

- 參數：無參數傳遞

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	flag = dbg.script_loader("d://x64dbg_script.txt")
	print("返回值: {}".format(flag))
		
	dbg.script_unloader()

	dbg.close()
```

**script_run():** 該函數用於運行一個已經載入到x64dbg中的腳本。

- 參數1：運行條數(可空)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	flag = dbg.script_loader("d://x64dbg_script.txt")
	print("返回值: {}".format(flag))

	dbg.script_run()

	dbg.close()
```

**script_set_ip():** 該函數用於指定從第幾行開始運行腳本。

- 參數1：運行下標

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	flag = dbg.script_loader("d://x64dbg_script.txt")
	print("返回值: {}".format(flag))

	dbg.script_set_ip(3)

	dbg.close()
```

**open_debug():** 該函數用於打開磁盤中的一個被調試程序。

- 參數1：被打開程序完整路徑

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	flag = dbg.open_debug("d://win32.exe")

	dbg.close()
```

**close_debug():** 該函數用於關閉當前打開的調試程序，之關閉程序不關閉調試器。

- 參數：無參數傳遞

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	flag = dbg.open_debug("d://win32.exe")
		
	if flag == True:
	dbg.close_debug()
		
	dbg.close()
```

**detach_debug():** 該函數用於讓調試器脫離進程，進程會被運行起來。

- 參數：無參數傳遞

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	flag = dbg.open_debug("d://win32.exe")

	if flag == True:
	dbg.detach_debug()

	dbg.close()
```

**message_box():** 此功能提供了三種對話框，一種可輸入文本，一種判斷是否選中，另一種則是普通彈窗。

- 參數1：彈出的提示信息

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	conn = dbg.connect()

	# 彈出輸入框
	flag = dbg.input_string_box("請輸入反彙編入口地址?")
	print("用戶的輸入: {}".format(flag))

	# 彈出是否框
	flag = dbg.message_box_yes_no("是否繼續執行脫殼操作?")
	if flag == True:
	print("脫殼")
	else:
	print("退出")

	# 提示框
	flag = dbg.message_box("這是第{} 次,異常了".format(1))
	print("狀態: {}".format(flag))

	dbg.close()
```

**set_argument_brackets():** 該函數可在`註釋`處增加括號。

- 參數1：開始位置（十進制）
- 參數2：結束位置（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	ref = dbg.set_argument_brackets(eip, eip +100)
	print("是否增加註釋: {}".format(ref))
		
	dbg.close()
```

**del_argument_brackets():** 該函數可清除通過`set_argument_brackets`設置的括號。

- 參數1：開始位置（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")
		
	dbg.del_argument_brackets(eip)

	dbg.close()
```

**set_function_brackets():** 該函數可實現在`機器碼`位置增加括號。

- 參數1：開始位置（十進制）
- 參數2：結束位置（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	flag = dbg.set_function_brackets(eip,eip+10)

	dbg.close()
```

**del_function_brackets():** 該函數可清除通過`del_function_brackets`設置的括號。

- 參數1：開始位置（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")
		
	dbg.del_function_brackets(eip)

	dbg.close()
```

**set_loop_brackets():** 該函數可實現在`反彙編`位置增加括號。

- 參數1：開始位置（十進制）
- 參數2：結束位置（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	ref = dbg.set_loop_brackets(eip,eip + 10)
	print("設置狀態: {}".format(ref))

	dbg.close()
```

**del_loop_brackets():** 該函數可清除通過`set_loop_brackets`設置的括號。

- 參數1：清除層級（默認1）
- 參數2：開始位置（十進制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	ref = dbg.del_loop_brackets(1,eip)
	print("清除狀態: {}".format(ref))

	dbg.close()
```

**set_label_at():** 該函數可在特定位置設置一個標籤。

- 參數1：設置標籤的地址（十進制）
- 參數2：標籤名（字符串）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")
		
	dbg.set_label_at(eip,"test1")
	dbg.set_label_at(eip+10,"test2")

	dbg.close()
```

**location_label_at():** 該函數可通過已有的標籤定位到所在位置，並返回內存地址。

- 參數1：標籤名（字符串）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	eip = dbg.get_register("eip")
		
	lab_addr = dbg.location_label_at("test2")
	print("標籤所在內存: {}".format(hex(lab_addr)))

	dbg.close()
```

**clear_label():** 該函數用於清除當前程序內所有的標籤。

- 參數：無參數傳遞

```Python
	from LyScript32 import MyDebug

	if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	ref = dbg.clear_label()

	dbg.close()
```

**update_all_view():** 刷新試圖函數，與切換CPU位置。

- 參數：無參數傳遞
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("連接狀態: {}".format(connect_flag))

	# 刷新試圖
	dbg.update_all_view()
		
	# 切換到CPU窗口
	dbg.switch_cpu()
		
	# 清除所有日誌
	dbg.clear_log()

	dbg.close()
```
<br>

<b>中文繁体（中国）版不完整。 如需完整閱讀，請閱讀中文版。</b>
