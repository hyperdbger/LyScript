# модуль автоматического управления X64dbg 

<br>
<div align=center>
	<img width="150" src="https://cdn.lyshark.com/archive/LyScript/lyscript_png.jpg" />
<!--
  <img width="100" src="https://cdn.lyshark.com/archive/LyScript/bug_black.png"/><tr>
    <img width="100" src="https://cdn.lyshark.com/archive/LyScript/python.png"/>
-->
 <br><br>
  
  [简体中文](README.md) | [ENGLISH](README-EN.md) | [русский язык ](README-RU.md)

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

<b>русский язык не полный.  полный комментарий, пожалуйста, прочитайте в китайском варианте. </b>
