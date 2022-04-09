# модуль автоматического управления X64dbg 

<br>
<div align=center>
  <img width="100" src="https://cdn.lyshark.com/archive/LyScript/bug_black.png"/><tr>
    <img width="100" src="https://cdn.lyshark.com/archive/LyScript/python.png"/>
 <br><br><br>
  
  [简体中文](README.md) | [ENGLISH](README-EN.md) | [русский язык ](README-RU.md)

  <br>
  
[![Build status](https://cdn.lyshark.com/archive/LyScript/build.svg)](https://github.com/lyshark/LyScript) [![Open Source Helpers](https://cdn.lyshark.com/archive/LyScript/users.svg)](https://github.com/lyshark/LyScript) [![Crowdin](https://cdn.lyshark.com/archive/LyScript/email.svg)](mailto:me@lyshark.com) [![Download x64dbg](https://cdn.lyshark.com/archive/LyScript/x64dbg.svg)](https://sourceforge.net/projects/x64dbg/files/latest/download)

<br><br>
модуль автоматизированного управления X64dbg, управляемый Python X64dbg, обеспечивает удалённую динамическую отладку, устраняет пробелы в анализе обратного персонала, ищет фрагменты команд, оригинальные сценарии недостаточно сильны, благодаря сочетанию с Python использует гибкость синтаксиса Python и богатую базу данных третьей стороны, повышает эффективность анализа и обеспечивает автоматизацию аналитического кода. 
  
</div>
<br>

 - установить пакет Python ：`pip install LyScript32` или  `pip install LyScript64`
 - 32битный модуль загрузки ：https://cdn.lyshark.com/software/LyScript32.zip
 - 64битный модуль загрузки ：https://cdn.lyshark.com/software/LyScript64.zip

после загрузки модуля, пожалуйста, скопируйте этот модуль в каталог plugins x64dbg, который будет загружен автоматически после запуска программы. 

![](https://img2022.cnblogs.com/blog/1379525/202203/1379525-20220327190905044-1815692787.png)

После успешной загрузки модуля в журнале будет показана информация о привязке и отладке вывода, которая не отображается в панели модулей. 

![image](https://user-images.githubusercontent.com/52789403/161062658-0452fe0c-3e11-4df4-a83b-b026f74884d0.png)

 Если требуется дистанционное отладка, то достаточно только инициализировать `MyDebug()` класс "для ввода IP - адресов в конец, а если параметр не заполнен, то по умолчанию используется" адрес `127.0.0.1`, пожалуйста, убедитесь, что в конце указан" порт `6589`, иначе соединение не может быть установлено. 

![image](https://user-images.githubusercontent.com/52789403/161062393-df04aabb-2d70-4434-80b9-a46974bccf8a.png)

 запустить программу x64dbg и вручную загрузить исполняемый файл, требующий анализа, и затем мы можем подключиться к отладчику через `connect()`, соединение будет создано после продолжительного сеанса, пока не закончится сценарий python, соединение будет принудительно отключено, в течение этого периода можно позвонить `is_connect()` проверить наличие ссылки, как указано ниже. 
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