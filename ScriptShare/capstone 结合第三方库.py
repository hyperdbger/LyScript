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