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

    ref = GetScriptValue(dbg,"teb()")
    print(hex(ref))

    ref = GetScriptValue(dbg,"peb()")
    print(hex(ref))

    # 得到当前EIP所指向位置模块基地址
    eax = dbg.get_register("eax")
    kbase = GetScriptValue(dbg,f"mod.base({eax})")
    print("模块基地址: {}".format(hex(kbase)))

    dbg.close()
