# модуль автоматического управления X64dbg 

<br>
<div align=center>
	<img width="150" src="https://cdn.lyshark.com/archive/LyScript/lyscript_png.jpg" />
<!--
  <img width="100" src="https://cdn.lyshark.com/archive/LyScript/bug_black.png"/><tr>
    <img width="100" src="https://cdn.lyshark.com/archive/LyScript/python.png"/>
-->
 <br><br>
  
  [简体中文](README.md) | [繁體中文(中國)](README-TC.md) | [ENGLISH](README-EN.md) | [русский язык ](README-RU.md)

  <br>
  
[![Build status](https://cdn.lyshark.com/archive/LyScript/build.svg)](https://github.com/lyshark/LyScript) [![Open Source Helpers](https://cdn.lyshark.com/archive/LyScript/users.svg)](https://github.com/lyshark/LyScript) [![Crowdin](https://cdn.lyshark.com/archive/LyScript/email.svg)](mailto:me@lyshark.com) [![Download x64dbg](https://cdn.lyshark.com/archive/LyScript/x64dbg.svg)](https://github.com/lyshark/LyScript/releases/tag/LyScript) [![OSCS Status](https://www.oscs1024.com/platform/badge/lyshark/LyScript.svg?size=small)](https://www.oscs1024.com/project/lyshark/LyScript?ref=badge_small)

[![python3](https://cdn.lyshark.com/archive/LyScript/python3.svg)](https://github.com/lyshark/LyScript) [![platform](https://cdn.lyshark.com/archive/LyScript/platform.svg)](https://github.com/lyshark/LyScript) [![lyscriptver](https://cdn.lyshark.com/archive/LyScript/lyscript_version.svg)](https://github.com/lyshark/LyScript)

<br><br>
модуль автоматизированного управления X64dbg с помощью Python для управления поведением x64dbg, для достижения удалённой динамической отладки, для решения проблем, связанных с программой анализа обратного специалиста, деактивизацией антивирусного персонала, поиском фрагментов команд аналитиками, оригинальными сценариями недостаточно сильны, благодаря сочетанию с Python, используя гибкость грамматики Python и его богатую базу данных третьей стороны, ускоряя разработку программ с использованием лазеек,  Дополнительные вскрытия и анализ вредоносного программного обеспечения.

</div>
<br>

пакет Python установите версию, соответствующую модуле, и выполните команду pip в командной строке cmd для установки и рекомендуется полностью установить оба пакета.

 - монтажный стандартный пакет：`pip install LyScript32` или  `pip install LyScript64`
 - монтажный пакет：`pip install LyScriptTools32` или  `pip install LyScriptTools64`

Во вторых, вам нужно вручную загрузить драйвер, соответствующий версии x64dbg, и поместить его в указанный каталог `plugins`.

 - x64dbg модулей：<a href="https://sourceforge.net/projects/x64dbg/files/snapshots/snapshot_2022-09-11_15-59.zip/download">snapshot_2022-09-11_15-59.zip</a>
 - Загрузка модулей ：<a href="https://github.com/lyshark/LyScript/raw/master/plugins/LyScript32-1.0.13.zip">LyScript32-1.0.13 (32bit)</a> или <a href="https://github.com/lyshark/LyScript/raw/master/plugins/LyScript64-1.0.13.zip">LyScript64-1.0.13 (64bit)</a>

после загрузки модуля, пожалуйста, скопируйте этот модуль в каталог plugins x64dbg, который будет загружен автоматически после запуска программы.

![image](https://user-images.githubusercontent.com/52789403/185293618-68102ea6-8c37-493e-8be3-ca46eca0f0b5.png)

После успешной загрузки модуля в журнале будет показана информация о привязке и отладке вывода, которая не отображается в панели модулей.

![image](https://user-images.githubusercontent.com/52789403/161062658-0452fe0c-3e11-4df4-a83b-b026f74884d0.png)

Если требуется отладка на большие расстояния, то достаточно ввести IP - адрес только в случае инициализации `MyDebug()` по аналогии, и, если параметр не будет заполнен, по умолчанию использовать адрес `127.0.0.1`, пожалуйста, убедитесь в том, что в конце указан `порт 6589`, иначе соединение не может быть установлено.

![image](https://user-images.githubusercontent.com/52789403/161062393-df04aabb-2d70-4434-80b9-a46974bccf8a.png)

запустить программу x64dbg и вручную загрузить исполняемый файл, требующий анализа, и затем мы можем подключиться к отладчику через `connect()`, соединение будет создано после продолжительного сеанса, пока не закончится сценарий python, соединение будет принудительно отключено, в течение этого периода можно позвонить `is_connect()` проверить наличие ссылки, как указано ниже.
```Python
from LyScript32 import MyDebug
if __name__ == "__main__":
    # инициализация 
    dbg = MyDebug()
	
    # подключиться к отладчику
    connect_flag = dbg.connect()
    print("состояние соединения: {}".format(connect_flag))
	
    # проверка сокета
    ref = dbg.is_connect()
    print("при соединении: ", ref)
    dbg.close()
```
<br>

### Функции серии регистров

**get_register():** Эта в основном используется для реализации.Чтобы получить конкретный регистр, пользователю необходимо передать имя регистра, который необходимо получить.

- Параметр 1: входящая строка регистра

Доступные диапазоны: "DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX" , "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI", " ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP", "CIP", "CSP", "CAX", "CBX", "CCX", "CDX" , "CDI", "CSI", "CBP", "CFLAGS"

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eax = dbg.get_register("eax")
	ebx = dbg.get_register("ebx")

	print("eax = {}".format(hex(eax)))
	print("ebx = {}".format(hex(ebx)))

	dbg.close()
```
if вы используете 64-битный подключаемый модуль, диапазон поддерживаемых регистров становится равным серии E плюс серии R.

Доступные расширения диапазона: «DR0», «DR1», «DR2», «DR3», «DR6», «DR7», «EAX», «AX», «AH», «AL», «EBX», «BX». " ", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI" , "ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP", "RAX", "RBX", "RCX", "RDX", "RSI", " SIL "", "RDI", "DIL", "RBP", "BPL", "RSP", "SPL", "RIP", "R8", "R8D", "R8W", "R8B", "R9 ", "R9D", "R9W", "R9B", "R10", "R10D", "R10W", "R10B", "R11", "R11D", "R11W", "R11B", "R12", "R12D", "R12W", "R12B", "R13", "R13D", "R13W", "R13B", "R14", "R14D", "R14W", "R14B", "R15", " Р15Д", "Р15W", "Р15Б"

```Python
из LyScript64 импортировать MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ракс = dbg.get_register("ракс")
	eax = dbg.get_register("eax")
	топор = dbg.get_register("топор")

	print("rax = {} eax = {} ax = {}".format(hex(rax),hex(eax),hex(ax)))

	r8 = dbg.get_register("r8")
	print("Получить регистры серии R: {}".format(hex(r8)))

	dbg.close()
```

**set_register():** Эта реализует установку указанных параметров регистра Аналогично, 64-битная версия будет поддерживать изменение параметров большего количества регистров.

- Параметр 1: входящая строка регистра
- Параметр 2: Десятичное значение

Доступные диапазоны: "DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX" , "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI", " ЭСИ», «СИ», «ЭБП», «БП», «ЭСП», «СП», «ЭИП»

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eax = dbg.get_register("eax")
		
	dbg.set_register("eax",100)

	print("eax = {}".format(hex(eax)))

	dbg.close()
```

**get_flag_register():** Используется для получения битового параметра флага, возвращаемое значение может быть только истинным или ложным.

- Параметр 1: регистровая строка

Доступные диапазоны регистров: "ZF", "OF", "CF", "PF", "SF", "TF", "AF", "DF", "IF"

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	cf = dbg.get_flag_register("cf")
	print("Знак: {}".format(cf))
		
	dbg.close()
```

**set_flag_register():** Используется для установки параметра флага, возвращаемое значение может быть только истинным или ложным.
 
- Параметр 1: регистровая строка
- Параметр 2: [установить значение True] / [установить значение False]

Доступные диапазоны регистров: "ZF", "OF", "CF", "PF", "SF", "TF", "AF", "DF", "IF"

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	zf = dbg.get_flag_register("zf")
	print (зф)

	dbg.set_flag_register("zf",False)

	zf = dbg.get_flag_register("zf")
	print (зф)

	dbg.close()
```
<br>

### Серия функций отладки

**set_debug():** Используется для воздействия на отладчик, например один раз вперед, один раз назад, приостановка отладки, завершение и т. д.

- Параметр 1: передать действие, которое нужно выполнить.

Доступный диапазон действий: [Пауза] [Выполнить Выполнить] [Перейти к входу] [Перешагнуть через выход] [Завершить шаг] [Стоп Стоп] [Подождите, подождите]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	пока верно:
	dbg.set_debug("Вход")
			
	eax = dbg.get_register("eax")
			
	if еах == 0:
	распечатать("Найден")
	ломать
			
	dbg.close()
```

**set_debug_count():** Эта является продолжением функции `set_debug()`, целью которой является выполнение автоматического подсчета шагов.

- Параметр 1: передать действие, которое необходимо выполнить.
- Параметр 2: количество повторений для выполнения

Доступный диапазон действий: [Пауза] [Выполнить Выполнить] [Перейти к входу] [Перешагнуть через выход] [Завершить шаг] [Стоп Стоп] [Подождите, подождите]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	dbg.set_debug_count("ШагВ",10)

	dbg.close()
```

**is_debugger() /is_running()/is_run_locked():** Функцию `is_debugger` можно использовать для проверки того, находится ли текущий отладчик в состоянии отладки, `is_running` используется для проверки того, работает ли он, ` is_run_locked()` используется для проверки того, заблокирован ли отладчик (приостановлен).

- параметры не передаются

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.is_debugger()
	print (ссылка)

	ссылка = dbg.is_running()
	print (ссылка)

	ссылка = dbg.is_run_locked()
	print (ссылка)

	dbg.close()
```

**set_breakpoint():** Установка точек останова и отмена точек останова разделены.Чтобы установить точки останова, вам нужно только передать десятичный адрес памяти.

- Параметр 1: входящий адрес памяти (десятичный)
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	ссылка = dbg.set_breakpoint(eip)

	print("Установить состояние: {}".format(ref))
	dbg.close()
```

****delete_breakpoint():** Эта передает адрес памяти для отмены точки останова памяти.

- Параметр 1: входящий адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	ссылка = dbg.set_breakpoint(eip)
	print("Установить состояние: {}".format(ref))

	del_ref = dbg.delete_breakpoint(eip)
	print("Статус отмены: {}".format(del_ref))

	dbg.close()
```

**check_breakpoint():** Используется для проверки того, сработала ли точка останова, if столкновение возвращает True, в противном случае возвращается False.

- Параметр 1: входящий адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	ссылка = dbg.set_breakpoint(eip)
	print("Установить состояние: {}".format(ref))

	is_check = dbg.check_breakpoint(4134331)
	print("Было ли попадание: {}".format(is_check))

	dbg.close()
```

**get_all_breakpoint():** Используется для получения всей информации о точках останова в текущем отладчике, включая информацию о том, включена ли она, количество попаданий и т. д.

- параметры не передаются

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	ссылка = dbg.get_all_breakpoint()
	print (ссылка)
	dbg.close()
```

**set_hardware_breakpoint():** используется для установки аппаратной точки останова, а в 32-разрядной системе можно установить не более 4 аппаратных точек останова.

- Параметр 1: адрес памяти (десятичный)
- параметр 2: тип точки останова

Тип точки останова Доступный диапазон: [Тип 0=HardwareAccess/1=HardwareWrite/2=HardwareExecute]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug (адрес = "127.0.0.1", порт = 6666)
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")

	ссылка = dbg.set_hardware_breakpoint(eip,2)
	print (ссылка)

	dbg.close()
```

**delete_hardware_breakpoint():** Используется для удаления аппаратной точки останова, нужно передать только адрес, не нужно передавать тип.

- Параметр 1: адрес памяти (десятичный)

Тип точки останова Доступный диапазон: [Тип 0=HardwareAccess/1=HardwareWrite/2=HardwareExecute]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug (адрес = "127.0.0.1", порт = 6666)
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")

	ссылка = dbg.set_hardware_breakpoint(eip,2)
	print (ссылка)

	# удалить точку останова
	ссылка = dbg.delete_hardware_breakpoint(eip)
	print (ссылка)

	dbg.close()
```

**is_bp_disable():** Эта используется для проверки того, отключена ли точка останова BP по указанному адресу.

- Параметр 1: адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	is_false = dbg.is_bp_disable(eip)
	print("статус точки останова bp: {}".format(is_false))

	dbg.close()
```

**get_xref_count_at():** Получает количество перекрестных ссылок по указанному адресу памяти.

- Параметр 1: адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	типы = dbg.get_xref_count_at (eip)
	print("Счетчик ссылок: {}".format(types))

	dbg.close()
```

**get_function_type_at():** Получить тип функции по указанному адресу памяти, тип перечисления функции FUNCTYPE.

- Параметр 1: адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	типы = dbg.get_function_type_at (eip)
	print("тип функции: {}".format(types))

	if (типы == 0):
	print("FUNC_NONE")
	elif (типы == 1):
	print ("FUNC_BEGIN")
	elif (типы == 2):
	print ("FUNC_MIDDLE")
	elif (типы == 3):
	распечатать("FUNC_END")
	elif (типы == 4):
	print ("FUNC_SINGLE")
	еще:
	распечатать("ошибка")

	dbg.close()
```

**get_bpx_type_at():** Получить тип точки останова BP по указанному адресу, перечисление типа `BPXTYPE`.

- Параметр 1: адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	типы = dbg.get_bpx_type_at (eip)
	print("Тип BPX: {}".format(types))

	if (типы == 0):
	print ("bp_none")
	elif (типы == 1):
	print("bp_нормальный")
	elif (типы == 2):
	print ("bp_hardware")
	elif (типы == 4):
	print("bp_memory")
	elif (типы == 8):
	print("bp_dll")
	elif (типы == 16):
	print ("bp_exception")
	еще:
	распечатать("ошибка")

	dbg.close()
```

**get_xref_type_at():** Получить тип перекрестной ссылки по указанному адресу памяти, перечислив тип `XREFTYPE`.

- Параметр 1: адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Состояние подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	типы = dbg.get_xref_type_at (eip)
	print("тип ссылки: {}".format(types))

	if (типы == 0):
	print("ССЫЛКА_ССЫЛКИ_НЕТ")
	elif (типы == 1):
	print("ССЫЛКА_ДАННЫХ")
	elif (типы == 2):
	print("ССЫЛКА_JMP")
	elif (типы == 3):
	print("ССЫЛКА_ЗВОНОК")
	еще:
	распечатать("ошибка")

	dbg.close()
```
<br>

### Функции серии модулей

**get_module_base():** Эту функцию можно использовать для получения базового адреса указанного модуля, загруженного программой.

- Параметр 1: Строка имени модуля

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
		
	user32_base = dbg.get_module_base("user32.dll")
	print (user32_base)

	dbg.close()
```

**get_all_module():** Используется для вывода всей информации о модулях текущего загрузчика, возвращаемой в виде словаря.

- параметры: нет параметров

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.get_all_module()

	для я в ссылке:
	print (я)

	print (ссылка [0])
	print (ссылка [1]. получить («имя»))
	print (ссылка [1]. получить ("путь"))

	dbg.close()
```

**Серия функций get_local_():** Получить базовый адрес, длину и атрибуты памяти модуля, в котором находится текущий EIP. Эта передается без параметров и данных модуля, на который указывает текущий EIP. получается.

- dbg.get_local_base() для получения базового адреса модуля
- dbg.get_local_size() для получения длины модуля
- dbg.get_local_protect() для получения атрибутов защиты модуля

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.get_local_base()
	print (шестнадцатеричный (ссылка))

	ссылка2 = dbg.get_local_size()
	print (шестнадцатеричный (ref2))

	ссылка3 = dbg.get_local_protect()
	print (ref3)

	dbg.close()
```

**get_module_from_function():** Получить адрес памяти указанной функции в указанном модуле, который можно использовать для проверки виртуального адреса указанной функции в памяти текущей программы.

- Параметр 1: Имя модуля
- Параметр 2: имя функции

Возвращает адрес в случае успеха, false в случае неудачи

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.get_module_from_function("user32.dll","MessageBoxW")
	print (шестнадцатеричный (ссылка))

	ref2 = dbg.get_module_from_function("kernel32.dll", "тест")
	print (ref2)

	dbg.close()
```

**get_module_from_import():** Получить информацию из таблицы импорта указанного модуля в текущей программе, а на выходе получить список вложенных словарей.

- Параметр 1: имя входящего модуля

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.get_module_from_import("ucrtbase.dll")
	print (ссылка)

	ref1 = dbg.get_module_from_import("win32project1.exe")

	для я в ref1:
	print (i.get («имя»))

	dbg.close()
```

**get_module_from_export():** Эта используется для получения информации таблицы экспорта в текущем загрузчике.

- Параметр 1: имя входящего модуля

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.get_module_from_export("msvcr120d.dll")

	для я в ссылке:
	print(i.get("имя"), hex(i.get("va")))

	dbg.close()
```

**get_section():** Эта используется для вывода информации таблицы разделов в основной программе.

- параметры не передаются

```Python
from LyScript32 import MyDebug
 
if __name__ == "__main__":
	dbg = MyDebug (адрес = "127.0.0.1", порт = 6666)
	connect_flag = dbg.connect()

	ссылка = dbg.get_section()
	print (ссылка)

	dbg.close()
```

**get_base_from_address():** Получить первый адрес модуля в соответствии с входящим адресом памяти.

- Параметр 1: входящий адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	eip = dbg.get_register("eip")

	ссылка = dbg.get_base_from_address(eip)
	print("Первый адрес модуля: {}".format(hex(ref)))
```

**get_base_from_name():** Получить первый адрес памяти, где находится модуль, в соответствии с именем входящего модуля.

- Параметр 1: имя входящего модуля

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	eip = dbg.get_register("eip")

	ref_base = dbg.get_base_from_name("win32project.exe")
	print("Первый адрес модуля: {}".format(hex(ref_base)))

	dbg.close()
```

**get_oep_from_name():** В соответствии с именем входящего модуля получить фактическое местоположение загруженного OEP модуля.

- Параметр 1: имя входящего модуля

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	oep = dbg.get_oep_from_name("win32project.exe")
	print (шестнадцатеричный (ОЕ))

	dbg.close()
```

**get_oep_from_address():** В соответствии с входящим адресом памяти получить местоположение OEP адресного модуля.

- Параметр 1: входящий адрес памяти

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	eip = dbg.get_register("eip")

	oep = dbg.get_oep_from_address(eip)
	print (шестнадцатеричный (ОЕ))

	dbg.close()
```

**get_section_from_module_name():** Пользователь может передать имя загруженного в данный момент модуля, чтобы напрямую получить информацию о таблице разделов указанного модуля.

- параметр 1: имя модуля (строка)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	section_user32 = dbg.get_section_from_module_name("user32.dll")
	print (section_user32)

	section_ntdll = dbg.get_section_from_module_name("ntdll.dll")
	print (section_ntdll)

	dbg.close()
```

**size_from_address():** Передайте базовый адрес модуля, чтобы получить общий размер, занимаемый модулем.

- Параметр 1: Адрес модуля (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	база = dbg.get_local_base()
	print("Базовый адрес модуля: {}".format(hex(base)))

	размер = dbg.size_from_address (база)
	print("Длина модуля: {}".format(size))

	dbg.close()
```

**size_from_name():** Передайте имя модуля, чтобы получить общий размер модуля.

- параметр 1: имя модуля (строка)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	размер = dbg.size_from_name("win32.exe")
	print ("Длина: {}". формат (размер))

	dbg.close()
```

**section_count_from_name():** Передайте имя модуля, чтобы узнать, сколько разделов имеет модуль.

- параметр 1: имя модуля (строка)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	размер = dbg.section_count_from_name("win32.exe")
	print("Количество разделов: {}".format(size))

	dbg.close()
```

**section_count_from_address():** Передайте базовый адрес модуля, чтобы узнать, сколько разделов имеет модуль.

- Параметр 1: Адрес модуля (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	база = dbg.get_local_base()
	print("Базовый адрес модуля: {}".format(hex(base)))

	размер = dbg.section_count_from_address (база)
	print("Количество разделов: {}".format(size))

	dbg.close()
```

**path_from_name():** Передайте имя модуля, чтобы получить путь к модулю.

- параметр 1: имя модуля (строка)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	размер = dbg.path_from_name("win32.exe")
	print("Путь к модулю: {}".format(size))

	dbg.close()
```

**path_from_address():** Передайте адрес модуля, чтобы получить путь к модулю.

- Параметр 1: Адрес модуля (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	база = dbg.get_local_base()
	print("Базовый адрес модуля: {}".format(hex(base)))

	путь = dbg.path_from_address (база)
	print("Путь к модулю: {}".format(path))

	dbg.close()
```

**name_from_address():** Передайте адрес модуля, чтобы получить имя модуля.

- Параметр 1: Адрес модуля (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	база = dbg.get_local_base()
	print("Базовый адрес модуля: {}".format(hex(base)))

	путь = dbg.name_from_address(база)
	print("Имя модуля: {}".format(path))

	dbg.close()
```

**get_window_handle():** Извлекает дескриптор собственного модуля процесса.

- Аргументы: аргументы не передаются

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	база = dbg.get_window_handle()
	print("Дескриптор процесса: {}".format(base))

	dbg.close()
```

**get_module_at():** Получить имя модуля по указанному адресу памяти, полученное здесь имя модуля не имеет суффикса.

- Параметр 1: Адрес модуля (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	ссылка = dbg.get_module_at(eip)
	print("Имя модуля: {}".format(ref))

	dbg.close()
```

**get_local_module():** Эту серию функций можно использовать для получения сведений о модуле, в котором текущий загрузчик находится в местоположении EIP.

- get_local_module_size() для получения размера текущей программы
- get_local_module_section_Count() для получения количества собственных разделов
- get_local_module_path() для получения полного пути отлаживаемой программы
- get_local_module_name() получает собственное имя модуля
- get_local_module_entry() получает свою собственную запись модуля
- get_local_module_base() для получения базового адреса собственного модуля

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	print("Размер программы: {}".format(dbg.get_local_module_size()))
	print("Количество разделов: {}".format(dbg.get_local_module_section_Count()))
	print("Полный путь: {}".format(dbg.get_local_module_path()))
	print("Имя модуля: {}".format(dbg.get_local_module_name()))
	print("Запись модуля: {}".format(dbg.get_local_module_entry()))
	print("Базовый адрес модуля: {}".format(dbg.get_local_module_base()))

	dbg.close()
```
<br>

### Функции серии памяти

**Функции серии read_memory_():** Функции серии чтения памяти, включая три формата ReadByte, ReadWord, ReadDword, поддерживают только Qword до 64 бит.

- Параметр 1: Адрес памяти для чтения (десятичный)

В настоящее время поддерживает:
- read_memory_byte() читать байты
- read_memory_word() прочитать слово
- read_memory_dword() прочитать двойное слово
- read_memory_qword() читает qword (только 64-разрядная версия)
- read_memory_ptr() указатель чтения

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")

	ссылка = dbg.read_memory_byte(eip)
	print (шестнадцатеричный (ссылка))

	ref2 = dbg.read_memory_word(eip)
	print (шестнадцатеричный (ref2))

	ref3 = dbg.read_memory_dword(eip)
	print (шестнадцатеричный (ref3))

	ref4 = dbg.read_memory_ptr(eip)
	print (шестнадцатеричный (ref4))

	dbg.close()
```

**Функции серии write_memory_():** Функции серии записи памяти, WriteByte,WriteWord,WriteDWORD,WriteQword

- Параметр 1: память для записи
- Параметр 2: байт, который необходимо записать

В настоящее время поддерживает:
- write_memory_byte() записать байты
- write_memory_word() записать слово
- write_memory_dword() записать двойное слово
- write_memory_qword() запись qword (только 64-битная версия)
- write_memory_ptr() указатель записи

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	адрес = dbg.create_alloc(1024)
	print (шестнадцатеричный (адрес))

	ссылка = dbg.write_memory_byte (адрес, 10)

	print (ссылка)

	dbg.close()
```

**scan_memory_one():** Реализует сканирование памяти и автоматически выводит данные при сканировании первого подходящего объекта.

- Параметр 1: Поле подписи

Эта должна быть отмечена тем, что if наш инструмент x64dbg припаркован в системном воздушном пространстве, он будет искать функции в системном воздушном пространстве по умолчанию.if вы хотите искать данные в программном воздушном пространстве, вам нужно вырезать EIP работать.
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	ссылка = dbg.scan_memory_one("ff 25")
	print (ссылка)
	dbg.close()
```

**scan_memory_all():** выполняет сканирование всех подходящих полей функций и возвращает список при обнаружении.

- Параметр 1: Поле подписи

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.scan_memory_all ("ff 25")

	для индекса в ссылке:
	print (шестнадцатеричный (индекс))

	dbg.close()
```

**scan_memory_any():** Эта может сканировать поле функции определенной длины для определенного местоположения.

- Параметр 1: адрес начала сканирования (десятичный)
- Параметр 2: длина сканирования (десятичное число)
- Параметр 3: Поле подписи

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	# инициализировать
	dbg = MyDebug()

	# подключаемся к отладчику
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	# Сканирование произвольного адреса
	eip = dbg.get_register("eip")
	ссылка = dbg.scan_memory_any(eip,1024,"8b 50 04 8b fe")
	print("Получить результат сканирования: {}".format(hex(ref)))

	dbg.close()
```

** get_local_protect(): ** Получите атрибут памяти и передайте значение, эта обновляет, отменяет атрибут памяти, который может получить только местоположение, на которое указывает EIP, и пользователь может проверить его по своему желанию.

- Параметр 1: адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	print (ип)

	ссылка = dbg.get_local_protect(eip)
	print (ссылка)
```

**set_local_protect():** Добавьте функцию для установки атрибутов памяти, передайте адрес памяти eIP, установите атрибут 32 и установите длину памяти на 1024.

- Параметр 1: адрес памяти (десятичный)
- параметр 2: тип разрешения (32=выполнение/чтение 30=выполнение 2=чтение/запись)
- Параметр 3: Длина атрибута (десятичная)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
		
	eip = dbg.get_register("eip")
	print (ип)

	б = dbg.set_local_protect(eip,32,1024)
	print("Установить статус свойства: {}".format(b))

	dbg.close()
```

**get_local_page_size():** Используется для получения размера страницы памяти pagesize в воздушном пространстве, на которое указывает текущий EIP.

- параметры не передаются

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	размер = dbg.get_local_page_size()
	print ("размер страницы = {}". формат (размер))

	dbg.close()
```

**get_memory_section():** Эта в основном используется для получения данных таблицы разделов памяти текущего отладчика в образе памяти.

- параметры не передаются
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.get_memory_section()
	print (ссылка)
	dbg.close()
```

**is_jmp_going_to_execute():** определяет, переходит ли адрес памяти к исполняемому блоку памяти.

- Параметр 1: адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	флаг = dbg.is_jmp_going_to_execute(eip)
	print("Является ли это переходом (является ли исполняемым): {}".format(flag))

	dbg.close()
```

**mem_find_base_addr():** возвращает базовый адрес и размер модуля памяти в определенном месте в виде словаря.

- Параметр 1: адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	dic = dbg.mem_find_base_addr(eip)

	print("Адрес базы памяти: {}".format(hex(dic.get("base"))))
	print("Размер памяти: {}".format(dic.get("размер")))

	dbg.close()
```

**mem_get_page_size():** Получить длину страницы памяти в указанном месте.

- Параметр 1: адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	адрес = dbg.mem_get_page_size (eip)

	print("Длина страницы памяти: {}".format(hex(addr)))

	dbg.close()
```

**mem_is_valid():** Проверяет, что адрес памяти в указанном месте доступен для чтения.

- Параметр 1: адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	is_read = dbg.mem_is_valid(eip)
	print("Атрибут адреса памяти: {}".format(is_read))

	dbg.close()
```
<br>

### функции серии стека

**create_alloc():** `create_alloc()` может удаленно открывать пространство кучи и успешно возвращать первый адрес памяти.

- Параметр 1: длина кучи для открытия (десятичное число)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.create_alloc(1024)
	print("Открыть адрес: ", hex(ref))

	dbg.close()
```

**delete_alloc():** `delete_alloc()` используется для удаления удаленного пространства кучи.

- Параметр 1: передать адрес памяти области кучи, которую нужно удалить.

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.create_alloc(1024)
	print("Открыть адрес: ", hex(ref))

	флаг = dbg.delete_alloc (ссылка)
	print("Статус удаления: ",пометить)

	dbg.close()
```

**push_stack():** помещает десятичное число в стек, по умолчанию наверху стека.

- Параметр 1: Десятичные данные

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.push_stack (10)

	print (ссылка)

	dbg.close()
```

**pop_stack():** pop используется для выталкивания элемента из стека, который по умолчанию извлекается из вершины стека.

- параметры не передаются

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	тт = dbg.pop_stack()
	print (тт)

	dbg.close()
```

****peek_stack(): ** peek используется для проверки параметров в стеке, и может быть установлено значение смещения, if оно не установлено, то по умолчанию первым является вершина стека.

- Параметр 1: десятичное смещение

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	# без проверки параметров
	проверить = dbg.peek_stack()
	распечатать (проверить)

	# Перенести проверку параметров
	check_1 = dbg.peek_stack(2)
	распечатать (check_1)

	dbg.close()
```
<br>

### Функции серий потоков обработки

**get_thread_list():** Эта может выводить всю информацию о запущенных потоках текущего процесса.

- параметры не передаются

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.get_thread_list()
	print (ссылка [0])
	print (ссылка [1])

	dbg.close()
```

**get_process_handle():** Используется для получения информации о текущем дескрипторе процесса.

- параметры не передаются

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.get_process_handle()
	print (ссылка)

	dbg.close()
```

**get_process_id():** Используется для получения PID текущего загрузчика.

- параметры не передаются

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.get_process_id()
	print (ссылка)

	dbg.close()
```

Серия функций **get_teb_address() / get_peb_address():** Используется для получения текущего блока среды процесса и среды потока.

- Входящий параметр get_teb_address() - это идентификатор потока.
- Входящий параметр get_peb_address() - это идентификатор процесса.

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.get_teb_address(6128)
	print (ссылка)

	ссылка = dbg.get_peb_address(9012)
	print (ссылка)

	dbg.close()
```
<br>

### Дизассемблировать серию функций

**get_disasm_code():** Эта в основном используется для дизассемблирования определенного адреса памяти и передачи двух параметров.

- Параметр 1: адрес для дизассемблирования (десятичный)
- Параметр 2: длина разбираемой части

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	# получить местоположение EIP
	eip = dbg.get_register("eip")

	# Разобрать первые 100 строк
	disasm_dict = dbg.get_disasm_code(eip,100)

	для ds в disasm_dict:
	print("Адрес: {} Разборка: {}".format(hex(ds.get("addr")), ds.get("opcode")))

	dbg.close()
```

**get_disasm_one_code():** считывает инструкцию по сборке в позиции, указанной пользователем, и пользователь может оценить ее по мере необходимости.
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	print ("EIP = {}". формат (eip))

	disasm = dbg.get_disasm_one_code(eip)
	print("Разобрать один: {}".format(disasm))

	dbg.close()
```

**get_disasm_operand_code():** Используется для получения операнда в ассемблерной инструкции, например, `jmp 0x0401000`, операнд `0x0401000`.

- Параметр 1: входящий адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	print ("EIP = {}". формат (eip))

	код операции = dbg.get_disasm_operand_code(eip)
	print("Операнд: {}".format(hex(opcode)))

	dbg.close()
```

**get_disasm_operand_size():** Используется для получения длины машинного кода ассемблерного кода по текущему адресу памяти.

- Параметр 1: входящий адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	print ("EIP = {}". формат (eip))

	код операции = dbg.get_disasm_operand_size(eip)

	print("Длина машинного кода: {}".format(hex(opcode)))

	dbg.close()
```

**assemble_write_memory():** понимает, что пользователь передает правильную инструкцию по ассемблеру, и программа автоматически преобразует инструкцию в машинный код и записывает ее в указанное место.

- Параметр 1: записать адрес памяти (десятичный)
- Параметр 2: написать инструкцию по сборке

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	print (ип)

	ссылка = dbg.assemble_write_memory(eip,"mov eax,1")
	print("Писать ли: {}".format(ref))

	dbg.close()
```

**assemble_code_size():** Эта понимает, что пользователь передает ассемблерную инструкцию, и автоматически вычисляет, сколько байтов занимает инструкция.

- Параметр 1: Строка инструкции по сборке

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.assemble_code_size("sub esp, 0x324")
	print (ссылка)

	dbg.close()
```

**get_branch_destination():** Получить адрес перехода вызова или инструкцию перехода jx.

- Параметр 1: получить адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	print("Текущий адрес EIP: {}".format(hex(eip)))

	значение = dbg.get_branch_destination(eip)
	print("Операнд: {}".format(hex(значение)))

	dbg.close()
```

**get_disassembly():** Дизассемблирует инструкцию, эта напрямую выводит то, что она видит при отладке, включая символы.

- Параметр 1: получить адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	print("Текущий адрес EIP: {}".format(hex(eip)))

	dasm = dbg.get_disassembly(eip)
	print("Разобрать кусок: {}".format(dasm))

	dbg.close()
```

**assemble_at():** ассемблируйте серию функций, передайте ассемблерную инструкцию и напрямую запишите инструкцию в память.

- Параметр 1: получить адрес памяти (десятичный)
- Параметр 2: Инструкция по сборке (строка)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	print("Текущий адрес EIP: {}".format(hex(eip)))

	ссылка = dbg.assemble_at(eip,"nop")
	print("Статус записи: {}".format(ref))

	dbg.close()
```

**disasm_fast_at():** Эта также дизассемблирует строку и возвращает словарь, но может получить более корректные параметры.

- Параметр 1: получить адрес памяти (десятичный)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")
	print("Текущий адрес EIP: {}".format(hex(eip)))

	dasm = dbg.disasm_fast_at(eip)
	print("Адрес: {}".format(hex(dasm.get("addr"))))
	print("Инструкция по сборке: {}".format(dasm.get("disasm")))
	print("Длина сборки: {}".format(dasm.get("size")))
	print("Является ли ветвь: {}".format(dasm.get("is_branch")))
	print("Вызов: {}".format(dasm.get("is_call")))
	print("Тип: {}".format(dasm.get("тип")))

	dbg.close()
```
<br>

### Другие серии функций

**set_comment_notes():** Добавьте комментарий к указанному коду местоположения. Ниже показано, как добавить комментарий к местоположению eIP.

- Параметр 1: адрес памяти комментариев
- Параметр 2: содержание комментария

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	eip = dbg.get_register("eip")
	ref = dbg.set_comment_notes(eip,"привет лишарк")
	print (ссылка)

	dbg.close()
```

**run_command_exec():** выполнение встроенных команд, таких как bp, dump и т. д.

- Параметр 1: оператор команды

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	ссылка = dbg.run_command_exec("bp MessageBoxA")
	print (ссылка)

	dbg.close()
```

**set_loger_output():** Вывод журнала особенно важен. Этот модуль предоставляет пользовательскую функцию вывода журнала, которая может выводить указанный журнал в расположение журнала x64dbg.

- Параметр 1: содержимое журнала

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()

	для я в диапазоне (0,100):
	ref = dbg.set_loger_output("привет lyshark -> {} \n".format(i))
	print (ссылка)

	dbg.close()
```

**run_command_exe_ref():** Эта является расширением `run_command_exec()`, которая в основном добавляет функцию передачи параметров, и в настоящее время она может передавать целые типы.

- Параметр 1: оператор команды

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	ссылка = dbg.run_command_exe_ref("mod.base(eip)")
	print("Возвращаемый параметр: {}".format(hex(ref)))

	dbg.close()
```

**set_status_bar_message():** Эта может выводить строку, переданную пользователем, в строку состояния в нижней части x64dbg.

- Параметр 1: выходная строка
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	dbg.set_status_bar_message("EIP => {}".format(hex(eip)))

	dbg.close()
```

**script_loader():** Эта получает путь к встроенному скрипту, переданному пользователем, и загружает скрипт в x64dbg.

- параметр 1: путь к скрипту

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	флаг = dbg.script_loader("d://x64dbg_script.txt")
	print("Возвращаемое значение: {}".format(flag))

	dbg.close()
```

**script_unloader():** Эта используется для закрытия скрипта, открытого в x64dbg.

- Аргументы: аргументы не передаются

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	флаг = dbg.script_loader("d://x64dbg_script.txt")
	print("Возвращаемое значение: {}".format(flag))
		
	dbg.script_unloader()

	dbg.close()
```

**script_run():** Эта используется для запуска скрипта, загруженного в x64dbg.

- Параметр 1: количество бегущих баров (обнуляемый)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	флаг = dbg.script_loader("d://x64dbg_script.txt")
	print("Возвращаемое значение: {}".format(flag))

	dbg.script_run()

	dbg.close()
```

**script_set_ip():** Эта используется для указания, из какой строки запускать скрипт.

- Параметр 1: запустить индекс

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	флаг = dbg.script_loader("d://x64dbg_script.txt")
	print("Возвращаемое значение: {}".format(flag))

	dbg.script_set_ip(3)

	dbg.close()
```

**open_debug():** Эта используется для открытия отлаженной программы на диске.

- Параметр 1: Полный путь открываемой программы

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	флаг = dbg.open_debug("d://win32.exe")

	dbg.close()
```

**close_debug():** Эта используется для закрытия текущего открытого отладчика, закрытие программы не закрывает отладчик.

- Аргументы: аргументы не передаются

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	флаг = dbg.open_debug("d://win32.exe")
		
	if флаг == Истина:
	dbg.close_debug()
		
	dbg.close()
```

**detach_debug():** Эта используется для отключения отладчика от процесса, после чего процесс будет запущен.

- Аргументы: аргументы не передаются

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	флаг = dbg.open_debug("d://win32.exe")

	if флаг == Истина:
	dbg.detach_debug()

	dbg.close()
```

**message_box():** Эта предоставляет три диалоговых окна, одно для ввода текста, одно для проверки того, выделено ли оно, а другое представляет собой обычное всплывающее окно.

- Параметр 1: всплывающая подсказка

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	соединение = dbg.connect ()

	# всплывающее окно ввода
	flag = dbg.input_string_box("Пожалуйста, введите адрес записи для дизассемблирования?")
	print("Ввод пользователя: {}".format(flag))

	# открыть коробку
	flag = dbg.message_box_yes_no("Продолжить распаковку?")
	if флаг == Истина:
	распечатать("распаковать")
	еще:
	распечатать("выйти")

	# поле подсказки
	flag = dbg.message_box("Это {}й раз, исключение".format(1))
	print ("Статус: {}". формат (флаг))

	dbg.close()
```

**set_argument_brackets():** Эта добавляет круглые скобки к комментариям.

- Параметр 1: начальная позиция (десятичная)
- Параметр 2: Конечная позиция (десятичная)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	ссылка = dbg.set_argument_brackets(eip, eip +100)
	print("Добавлять ли комментарии: {}".format(ref))
		
	dbg.close()
```

**del_argument_brackets():** Эта очищает скобки, установленные с помощью `set_argument_brackets`.

- Параметр 1: начальная позиция (десятичная)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")
		
	dbg.del_argument_brackets(eip)

	dbg.close()
```

**set_function_brackets():** Эта может добавлять скобки в позиции «машинного кода».

- Параметр 1: начальная позиция (десятичная)
- Параметр 2: Конечная позиция (десятичная)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	флаг = dbg.set_function_brackets(eip,eip+10)

	dbg.close()
```

**del_function_brackets():** Эта очищает скобки, установленные с помощью `del_function_brackets`.

- Параметр 1: начальная позиция (десятичная)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")
		
	dbg.del_function_brackets(eip)

	dbg.close()
```

**set_loop_brackets():** Эта реализует добавление скобок в позиции `разборки`.

- Параметр 1: начальная позиция (десятичная)
- Параметр 2: Конечная позиция (десятичная)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	ссылка = dbg.set_loop_brackets (eip, eip + 10)
	print("Установить состояние: {}".format(ref))

	dbg.close()
```

**del_loop_brackets():** Эта очищает скобки, установленные с помощью `set_loop_brackets`.

- параметр 1: уровень очистки (по умолчанию 1)
- параметр 2: начальная позиция (десятичная)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")

	ссылка = dbg.del_loop_brackets(1,eip)
	print("Очистить статус: {}".format(ref))

	dbg.close()
```

**set_label_at():** Эта устанавливает метку в определенной позиции.

- Параметр 1: Установите адрес метки (десятичный)
- параметр 2: имя метки (строка)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")
		
	dbg.set_label_at(eip,"test1")
	dbg.set_label_at(eip+10,"test2")

	dbg.close()
```

**location_label_at():** Эта может найти местоположение по существующей метке и вернуть адрес памяти.

- параметр 1: имя метки (строка)

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	eip = dbg.get_register("eip")
		
	lab_addr = dbg.location_label_at("test2")
	print("Память, в которой находится метка: {}".format(hex(lab_addr)))

	dbg.close()
```

**clear_label():** Эта используется для очистки всех меток в текущей программе.

- Аргументы: аргументы не передаются

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	ссылка = dbg.clear_label()

	dbg.close()
```

**update_all_view():** попытки обновления и переключение положения процессора.

- Аргументы: аргументы не передаются
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
	dbg = MyDebug()
	connect_flag = dbg.connect()
	print("Статус подключения: {}".format(connect_flag))

	# попытка обновления
	dbg.update_all_view()
		
	# переключиться в окно процессора
	dbg.switch_cpu()
		
	# очистить все журналы
	dbg.clear_log()

	dbg.close()
```
<br>

<b>русский язык не полный.  полный комментарий, пожалуйста, прочитайте в китайском варианте. </b>
