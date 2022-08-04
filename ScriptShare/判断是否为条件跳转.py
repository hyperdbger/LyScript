from LyScript32 import MyDebug

# 是否是条件跳转指令
def is_cond(dbg,address):
    try:
        dis = dbg.get_disasm_one_code(address)
        if dis != False or dis != None:

            if dis.split(" ")[0].replace(" ","") in ["je","jne","jz","jnz","ja","jna","jp","jnp","jb","jnb","jg","jng","jge","jl","jle"]:
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