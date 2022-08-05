# -*- coding: utf-8 -*-
import time
from LyScript64 import MyDebug

# ----------------------------------------------------------------------
# 纯脚本封装
# ----------------------------------------------------------------------
# 模块类
class LyScriptModule(object):
    def GetScriptValue(self, dbg, script):
        try:
            ref = dbg.run_command_exec("push rax")
            if ref != True:
                return None
            ref = dbg.run_command_exec(f"rax={script}")
            if ref != True:
                dbg.run_command_exec("pop rax")
                return None
            time.sleep(0.1)
            reg = dbg.get_register("rax")
            ref = dbg.run_command_exec("pop rax")
            if ref != True:
                return None
            return reg
        except Exception:
            return None
        return None

    # 获取模块基址
    def base(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mod.base({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 获取模块的模式编号, addr = 0则是用户模块,1则是系统模块
    def party(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mod.party({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 返回模块大小
    def size(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mod.size({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 返回模块hash
    def hash(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mod.hash({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 返回模块入口
    def entry(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mod.entry({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 如果addr是系统模块则为true否则则是false
    def system(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mod.system({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 如果是用户模块则返回true 否则为false
    def user(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mod.user({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 返回主模块基地址
    def main(self, dbg):
        try:
            ref = self.GetScriptValue(dbg, "mod.main()")
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 如果addr不在模块则返回0,否则返回 addr所位于模块的 RVA偏移
    def rva(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mod.rva({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 获取地址所对应的文件偏移量,如果不在模块则返回0
    def offset(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mod.offset({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 判断该地址是否是从模块导出的函数,true是 false则不是
    def isexport(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mod.isexport({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False


# 反汇编类封装
class LyScriptDisassemble(object):
    def GetScriptValue(self, dbg, script):
        try:
            ref = dbg.run_command_exec("push rax")
            if ref != True:
                return None
            ref = dbg.run_command_exec(f"rax={script}")
            if ref != True:
                dbg.run_command_exec("pop rax")
                return None
            time.sleep(0.1)
            reg = dbg.get_register("rax")
            ref = dbg.run_command_exec("pop rax")
            if ref != True:
                return None
            return reg
        except Exception:
            return None
        return None

    # 获取addr处的指令长度
    def len(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.len({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 判断当前addr位置是否是条件指令(比如jxx) 返回值: 是的话True 否则False
    def iscond(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.iscond({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 判断当前地址是否是分支指令   返回值: 同上
    def isbranch(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.isbranch({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 判断是否是ret指令          返回值: 同上
    def isret(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.isret({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 判断是否是call指令         返回值: 同上
    def iscall(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.iscall({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 判断是否是内存操作数        返回值: 同上
    def ismem(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.ismem({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 判断是否是nop             返回值: 同上
    def isnop(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.isnop({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 判断当前地址是否指示为异常地址 返回值: 同上
    def isunusual(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.isunusual({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 将指令的分支目标位于（如果按 Enter 键）
    def branchdest(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.branchdest({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 如果 分支 at 要执行，则为 true。addr
    def branchexec(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.branchexec({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 获取当前指令位置的立即数(这一行指令中出现的立即数)
    def imm(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.imm({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 指令在分支目标。
    def brtrue(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.brtrue({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 下一条指令的地址（如果指令 at 是条件分支）。
    def brfalse(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.brfalse({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 获取addr的下一条地址
    def next(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.next({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 获取addr上一条低地址
    def prev(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.prev({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 判断当前指令是否是系统模块指令
    def iscallsystem(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "dis.iscallsystem({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False


# 内存操作类
class LyScriptMemory(object):
    def GetScriptValue(self, dbg, script):
        try:
            ref = dbg.run_command_exec("push rax")
            if ref != True:
                return None
            ref = dbg.run_command_exec(f"rax={script}")
            if ref != True:
                dbg.run_command_exec("pop rax")
                return None
            time.sleep(0.1)
            reg = dbg.get_register("rax")
            ref = dbg.run_command_exec("pop rax")
            if ref != True:
                return None
            return reg
        except Exception:
            return None
        return None

    # 获取PEB的地址
    def peb(self, dbg):
        try:
            ref = self.GetScriptValue(dbg, "peb()")
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 获取TEB的地址
    def teb(self, dbg):
        try:
            ref = self.GetScriptValue(dbg, "teb()")
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 获取当前线程的ID
    def tid(self, dbg):
        try:
            ref = self.GetScriptValue(dbg, "tid()")
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 查询X64Dbg 应该是获取用户共享数据 地址
    def kusd(self, dbg):
        try:
            ref = self.GetScriptValue(dbg, "kusd()")
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 判断addr是否有效,有效则返回True
    def valid(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mem.valid({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 获取当前addr的基址
    def base(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mem.base({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 获取当前addr内存的大小
    def size(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mem.size({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 判断当前 addr是否是可执行页面,成功返回TRUE
    def iscode(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mem.iscode({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 解密指针,相当于调用了API. DecodePointer ptr
    def decodepointer(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "mem.decodepointer({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 从addr或者寄存器中读取一个字节内存并且返回
    def read_byte(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "ReadByte({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 同上
    def byte(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "byte({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 同上 读取两个字节
    def read_word(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "ReadWord({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 同上 读取四个字节
    def read_dword(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "ReadDword({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 读取8字节
    def read_qword(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "ReadQword({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 从地址中读取指针(4/8字节)并返回读取的指针值
    def read_ptr(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "ReadPtr({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    def read_pointer(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "ReadPointer({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    def ptr(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "ptr({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    def pointer(self, dbg, address):
        try:
            ref = self.GetScriptValue(dbg, "Pointer({})".format(address))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

# 其他类封装
class LyScriptOther(object):
    def GetScriptValue(self, dbg, script):
        try:
            ref = dbg.run_command_exec("push rax")
            if ref != True:
                return None
            ref = dbg.run_command_exec(f"rax={script}")
            if ref != True:
                dbg.run_command_exec("pop rax")
                return None
            time.sleep(0.1)
            reg = dbg.get_register("rax")
            ref = dbg.run_command_exec("pop rax")
            if ref != True:
                return None
            return reg
        except Exception:
            return None
        return None

    # 获取当前函数堆栈中的第几个参数,假设返回地址在堆栈上,并且我们在函数内部.
    def get(self, dbg, index):
        try:
            ref = self.GetScriptValue(dbg, "arg.get({})".format(index))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 设置的索引位置的值
    def set(self, dbg, index, value):
        try:
            ref = self.GetScriptValue(dbg, "arg.set({},{})".format(index, value))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 最后一个异常是否为第一次机会异常。
    def firstchance(self, dbg):
        try:
            ref = self.GetScriptValue(dbg, "ex.firstchance()")
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 最后一个异常地址。例如，导致异常的指令的地址。
    def addr(self, dbg):
        try:
            ref = self.GetScriptValue(dbg, "ex.addr()")
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 最后一个异常代码。
    def code(self, dbg):
        try:
            ref = self.GetScriptValue(dbg, "ex.code()")
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 最后一个异常标志。
    def flags(self, dbg):
        try:
            ref = self.GetScriptValue(dbg, "ex.flags()")
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 上次异常信息计数（参数数）。
    def infocount(self, dbg):
        try:
            ref = self.GetScriptValue(dbg, "ex.infocount()")
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

    # 最后一个异常信息，如果索引超出范围，则为零。
    def info(self, dbg, index):
        try:
            ref = self.GetScriptValue(dbg, "ex.info({})".format(index))
            if ref != None:
                return ref
            return False
        except Exception:
            return False
        return False

# ----------------------------------------------------------------------
# 模块类封装
# ----------------------------------------------------------------------
class Module(object):
    def __init__(self, ptr):
        self.dbg = ptr

    # 得到程序自身完整路径
    def get_local_full_path(self):
        try:
            module = self.dbg.get_all_module()
            if module == False:
                return False
            return module[0].get("path")
        except Exception:
            return False

    # 获得名称
    def get_local_program_name(self):
        try:
            module = self.dbg.get_all_module()
            if module == False:
                return False
            return module[0].get("name")
        except Exception:
            return False

    # 得到长度
    def get_local_program_size(self):
        try:
            module = self.dbg.get_all_module()
            if module == False:
                return False
            return module[0].get("size")
        except Exception:
            return False

    # 得到基地址
    def get_local_program_base(self):
        try:
            module = self.dbg.get_all_module()
            if module == False:
                return False
            return module[0].get("base")
        except Exception:
            return False

    # 得到入口地址
    def get_local_program_entry(self):
        try:
            module = self.dbg.get_all_module()
            if module == False:
                return False
            return module[0].get("entry")
        except Exception:
            return False

    # 验证程序是否导入了指定模块
    def check_module_imported(self, module_name):
        try:
            module = self.dbg.get_all_module()
            if module == False:
                return False

            for index in range(0, len(module)):
                if module[index].get("name") == module_name:
                    return True
            return False
        except Exception:
            return False

    # 根据基地址得到模块名
    def get_name_from_module(self, address):
        try:
            module = self.dbg.get_all_module()
            if module == False:
                return False

            for index in range(0, len(module)):
                if str(module[index].get("base")) == address:
                    return module[index].get("name")
            return False
        except Exception:
            return False

    # 根据模块名得到基地址
    def get_base_from_module(self, module_name):
        try:
            module = self.dbg.get_all_module()
            if module == False:
                return False

            for index in range(0, len(module)):
                if module[index].get("name") == module_name:
                    return module[index].get("base")
            return False
        except Exception:
            return False

    # 根据模块名得到模块OEP入口
    def get_oep_from_module(self, module_name):
        try:
            module = self.dbg.get_all_module()
            if module == False:
                return False

            for index in range(0, len(module)):
                if module[index].get("name") == module_name:
                    return module[index].get("entry")
            return False
        except Exception:
            return False

    # 得到所有模块信息
    def get_all_module_information(self):
        try:
            ref = self.dbg.get_all_module()
            if ref != False:
                return ref
            return False
        except Exception:
            return False

    # 得到特定模块基地址
    def get_module_base(self, module_name):
        try:
            ref = self.dbg.get_module_base(module_name)
            if ref != False:
                return ref
            return False
        except Exception:
            return False

    # 得到当前OEP位置处模块基地址
    def get_local_base(self):
        try:
            ref = self.dbg.get_local_base()
            if ref != False:
                return ref
            return False
        except Exception:
            return False

    # 获取当前OEP位置长度
    def get_local_size(self):
        try:
            ref = self.dbg.get_local_size()
            if ref != False:
                return ref
            return False
        except Exception:
            return False

    # 获取当前OEP位置保护属性
    def get_local_protect(self):
        try:
            ref = self.dbg.get_local_protect()
            if ref != False:
                return ref
            return False
        except Exception:
            return False

    # 获取指定模块中指定函数内存地址
    def get_module_from_function(self, module, function):
        try:
            ref = self.dbg.get_module_from_function(module, function)
            if ref != False:
                return ref
            return False
        except Exception:
            return False

    # 根据传入地址得到模块首地址,开头4D 5A
    def get_base_from_address(self, address):
        try:
            ref = self.dbg.get_base_from_address(int(address))
            if ref != False:
                return ref
            return False
        except Exception:
            return False

    # 得到当前.text节基地址
    def get_base_address(self):
        try:
            module_base = self.dbg.get_local_base()
            ref = self.dbg.get_base_from_address(int(module_base))
            if ref != False:
                return ref
            return False
        except Exception:
            return False

    # 根据名字得到模块基地址
    def get_base_from_name(self, module_name):
        try:
            ref = self.dbg.get_base_from_address(module_name)
            if ref != False:
                return ref
            return False
        except Exception:
            return False

    # 传入模块名得到OEP位置
    def get_oep_from_name(self, module_name):
        try:
            ref = self.dbg.get_oep_from_name(module_name)
            if ref != False:
                return ref
            return False
        except Exception:
            return False

    # 传入模块地址得到OEP位置
    def get_oep_from_address(self, address):
        try:
            ref = self.dbg.get_oep_from_address(int(address))
            if ref != False:
                return ref
            return False
        except Exception:
            return False

    # 得到指定模块的导入表
    def get_module_from_import(self, module_name):
        try:
            ref = self.dbg.get_module_from_import(str(module_name))
            if ref != False:
                return ref
            return False
        except Exception:
            return False

    # 检查指定模块内是否存在特定导入函数
    def get_import_inside_function(self, module_name, function_name):
        try:
            ref = self.dbg.get_module_from_import(str(module_name))
            if ref != False:
                for index in range(0, len(ref)):
                    if ref[index].get("name") == str(function_name):
                        return True
                return False
            return False
        except Exception:
            return False

    # 根据导入函数名得到函数iat_va地址
    def get_import_iatva(self, module_name, function_name):
        try:
            ref = self.dbg.get_module_from_import(str(module_name))
            if ref != False:
                for index in range(0, len(ref)):
                    if ref[index].get("name") == str(function_name):
                        return ref[index].get("iat_va")
                return False
            return False
        except Exception:
            return False

    # 根据导入函数名得到函数iat_rva地址
    def get_import_iatrva(self, module_name, function_name):
        try:
            ref = self.dbg.get_module_from_import(str(module_name))
            if ref != False:
                for index in range(0, len(ref)):
                    if ref[index].get("name") == str(function_name):
                        return ref[index].get("iat_rva")
                return False
            return False
        except Exception:
            return False

    # 传入模块名,获取模块导出表
    def get_module_from_export(self, module_name):
        try:
            ref = self.dbg.get_module_from_export(str(module_name))
            if ref != False:
                return ref
            return False
        except Exception:
            return False

    # 传入模块名以及导出函数名,得到va地址
    def get_module_export_va(self, module_name, function_name):
        try:
            ref = self.dbg.get_module_from_export(str(module_name))
            if ref != False:
                for index in range(0, len(ref)):
                    if ref[index].get("name") == str(function_name):
                        return ref[index].get("va")
                return False
            return False
        except Exception:
            return False

    # 传入模块名以及导出函数,得到rva地址
    def get_module_export_rva(self, module_name, function_name):
        try:
            ref = self.dbg.get_module_from_export(str(module_name))
            if ref != False:
                for index in range(0, len(ref)):
                    if ref[index].get("name") == str(function_name):
                        return ref[index].get("rva")
                return False
            return False
        except Exception:
            return False

    # 得到程序节表信息
    def get_local_section(self):
        try:
            ref = self.dbg.get_section()
            if ref != False:
                return ref
            return False
        except Exception:
            return False

    # 根据节名称得到地址
    def get_local_address_from_section(self, section_name):
        try:
            ref = self.dbg.get_section()
            if ref != False:
                for index in range(0, len(ref)):
                    if ref[index].get("name") == str(section_name):
                        return ref[index].get("addr")
                return False
            return False
        except Exception:
            return False

    # 根据节名称得到节大小
    def get_local_size_from_section(self, section_name):
        try:
            ref = self.dbg.get_section()
            if ref != False:
                for index in range(0, len(ref)):
                    if ref[index].get("name") == str(section_name):
                        return ref[index].get("size")
                return False
            return False
        except Exception:
            return False

    # 根据地址得到节名称
    def get_local_section_from_address(self, address):
        try:
            ref = self.dbg.get_section()
            if ref != False:
                for index in range(0, len(ref)):
                    if ref[index].get("addr") == int(address):
                        return ref[index].get("name")
                return False
            return False
        except Exception:
            return False

# ----------------------------------------------------------------------
# 反汇编类封装
# ----------------------------------------------------------------------
class Disassemble(object):
    def __init__(self, ptr):
        self.dbg = ptr

    # 是否是跳转指令
    def is_call(self, address = 0):
        try:
            if(address == 0):
                address = self.dbg.get_register("rip")

            dis = self.dbg.get_disasm_one_code(int(address))
            if dis != False or dis != None:
                if dis.split(" ")[0].replace(" ", "").lower() == "call":
                    return True
                return False
            return False
        except Exception:
            return False
        return False

    # 是否是jmp
    def is_jmp(self, address = 0):
        try:
            if(address == 0):
                address = self.dbg.get_register("rip")

            dis = self.dbg.get_disasm_one_code(int(address))
            if dis != False or dis != None:
                if dis.split(" ")[0].replace(" ", "").lower() == "jmp":
                    return True
                return False
            return False
        except Exception:
            return False
        return False

    # 是否是ret
    def is_ret(self, address = 0):
        try:
            if(address == 0):
                address = self.dbg.get_register("rip")

            dis = self.dbg.get_disasm_one_code(int(address))
            if dis != False or dis != None:
                if dis.split(" ")[0].replace(" ", "").lower() == "ret":
                    return True
                return False
            return False
        except Exception:
            return False
        return False

    # 是否是nop
    def is_nop(self, address = 0):
        try:
            if(address == 0):
                address = self.dbg.get_register("rip")

            dis = self.dbg.get_disasm_one_code(int(address))
            if dis != False or dis != None:
                if dis.split(" ")[0].replace(" ", "").lower() == "nop":
                    return True
                return False
            return False
        except Exception:
            return False
        return False

    # 是否是条件跳转指令
    def is_cond(self, address = 0):
        try:
            if(address == 0):
                address = self.dbg.get_register("rip")
            dis = self.dbg.get_disasm_one_code(int(address))
            if dis != False or dis != None:
                if dis.split(" ")[0].replace(" ", "").lower() in ["je","jne","jz","jnz","ja","jna","jp","jnp","jb","jnb","jg","jng","jge","jl","jle"]:
                    return True
            return False
        except Exception:
            return False
        return False

    # 是否cmp比较指令
    def is_cmp(self, address = 0):
        try:
            if(address == 0):
                address = self.dbg.get_register("rip")
            dis = self.dbg.get_disasm_one_code(int(address))
            if dis != False or dis != None:
                if dis.split(" ")[0].replace(" ", "").lower() == "cmp":
                    return True
            return False
        except Exception:
            return False
        return False

    # 是否是test比较指令
    def is_test(self,address = 0):
        try:
            if(address == 0):
                address = self.dbg.get_register("rip")
            dis = self.dbg.get_disasm_one_code(int(address))
            if dis != False or dis != None:
                if dis.split(" ")[0].replace(" ", "").lower() == "test":
                    return True
            return False
        except Exception:
            return False
        return False

    # 自定义判断条件
    def is_(self,address, cond):
        try:
            dis = self.dbg.get_disasm_one_code(int(address))
            if dis != False or dis != None:
                if dis.split(" ")[0].replace(" ", "").lower() == str(cond.replace(" ","")):
                    return True
            return False
        except Exception:
            return False
        return False

    # 得到指定位置汇编指令,不填写默认获取rip位置处
    def get_assembly(self,address=0):
        try:
            if(address == 0):
                address = self.dbg.get_register("rip")

            dis = self.dbg.get_disasm_one_code(int(address))
            if dis != False or dis != None:
                return dis
            return False
        except Exception:
            return False
        return False

    # 得到指定位置机器码
    def get_opcode(self,address=0):
        try:
            ref_opcode = []
            if(address == 0):
                address = self.dbg.get_register("rip")
            # 得到汇编指令
            dis = self.dbg.get_disasm_one_code(int(address))
            if dis != False or dis != None:
                # 转机器码
                addr = self.dbg.create_alloc(1024)
                asm_size = self.dbg.assemble_code_size(dis)
                self.dbg.assemble_write_memory(addr, dis)
                for index in range(0, asm_size):
                    read = self.dbg.read_memory_byte(addr + index)
                    ref_opcode.append(read)
                self.dbg.delete_alloc(addr)
                return ref_opcode
            return False
        except Exception:
            return False
        return False

    # 获取反汇编代码长度
    def get_disasm_operand_size(self,address=0):
        try:
            if(address == 0):
                address = self.dbg.get_register("rip")

            dis = self.dbg.get_disasm_operand_size(int(address))
            if dis != False or dis != None:
                return dis
            return False
        except Exception:
            return False
        return False

    # 计算用户传入汇编指令长度
    def assemble_code_size(self, assemble):
        try:
            dis = self.dbg.assemble_code_size(str(assemble))
            if dis != False or dis != None:
                return dis
            return False
        except Exception:
            return False
        return False

    # 用户传入汇编指令返回机器码
    def get_assemble_code(self,assemble):
        try:
            ref_opcode = []

            # 转机器码
            addr = self.dbg.create_alloc(1024)
            asm_size = self.dbg.assemble_code_size(assemble)
            self.dbg.assemble_write_memory(addr, assemble)
            for index in range(0, asm_size):
                read = self.dbg.read_memory_byte(addr + index)
                ref_opcode.append(read)
            self.dbg.delete_alloc(addr)
            return ref_opcode
        except Exception:
            return False
        return False

    # 将汇编指令写出到指定内存位置
    def write_assemble(self,address,assemble):
        try:
            opcode = []
            # 转机器码
            addr = self.dbg.create_alloc(1024)
            asm_size = self.dbg.assemble_code_size(assemble)
            self.dbg.assemble_write_memory(addr, assemble)
            for index in range(0, asm_size):
                read = self.dbg.read_memory_byte(addr + index)
                opcode.append(read)
            self.dbg.delete_alloc(addr)

            # 写出到内存
            for index in range(0,len(opcode)):
                self.dbg.write_memory_byte(address + index,opcode[index])
            return True
        except Exception:
            return False
        return False

    # 反汇编指定行数
    def get_disasm_code(self,address,size):
        try:
            dis = self.dbg.get_disasm_code(int(address),int(size))
            if dis != False or dis != None:
                return dis
            return False
        except Exception:
            return False
        return False

    # 向下反汇编一行
    def get_disasm_one_code(self,address = 0):
        try:
            if address == 0:
                address = self.dbg.get_register("rip")

            dis = self.dbg.get_disasm_one_code(int(address))
            if dis != False or dis != None:
                return dis
            return False
        except Exception:
            return False
        return False

    # 得到当前内存地址反汇编代码的操作数
    def get_disasm_operand_code(self,address=0):
        try:
            if address == 0:
                address = self.dbg.get_register("rip")

            dis = self.dbg.get_disasm_operand_code(int(address))
            if dis != False or dis != None:
                return dis
            return False
        except Exception:
            return False
        return False

    # 获取当前rip指令的下一条指令
    def get_disasm_next(self, rip):
        next = 0

        # 检查当前内存地址是否被下了绊子
        check_breakpoint = self.dbg.check_breakpoint(rip)

        # 说明存在断点，如果存在则这里就是一个字节了
        if check_breakpoint == True:

            # 接着判断当前是否是rip，如果是rip则需要使用原来的字节
            local_rip = self.dbg.get_register("rip")

            # 说明是rip并且命中了断点
            if local_rip == rip:
                dis_size = self.dbg.get_disasm_operand_size(rip)
                next = rip + dis_size
                next_asm = self.dbg.get_disasm_one_code(next)
                return next_asm
            else:
                next = rip + 1
                next_asm = self.dbg.get_disasm_one_code(next)
                return next_asm
            return None

        # 不是则需要获取到原始汇编代码的长度
        elif check_breakpoint == False:
            # 得到当前指令长度
            dis_size = self.dbg.get_disasm_operand_size(rip)
            next = rip + dis_size
            next_asm = self.dbg.get_disasm_one_code(next)
            return next_asm
        else:
            return None

    # 获取当前rip指令的上一条指令
    def get_disasm_prev(self, rip):
        prev_dasm = None
        # 得到当前汇编指令
        local_disasm = self.dbg.get_disasm_one_code(rip)

        # 只能向上扫描10行
        rip = rip - 10
        disasm = self.dbg.get_disasm_code(rip, 10)

        # 循环扫描汇编代码
        for index in range(0, len(disasm)):
            # 如果找到了,就取出他的上一个汇编代码
            if disasm[index].get("opcode") == local_disasm:
                prev_dasm = disasm[index - 1].get("opcode")
                break
        return prev_dasm

# ----------------------------------------------------------------------
# 控制类封装
# ----------------------------------------------------------------------
class DebugControl(object):
    def __init__(self, ptr):
        self.dbg = ptr

    # 寄存器读写
    def GetEAX(self):
        return self.dbg.get_register("eax")

    def SetEAX(self,decimal_value):
        return self.dbg.set_register("eax",decimal_value)

    def GetAX(self):
        return self.dbg.get_register("ax")

    def SetAX(self,decimal_value):
        return self.dbg.set_register("ax",decimal_value)

    def GetAH(self):
        return self.dbg.get_register("ah")

    def SetAH(self,decimal_value):
        return self.dbg.set_register("ah",decimal_value)

    def GetAL(self):
        return self.dbg.get_register("al")

    def SetAL(self,decimal_value):
        return self.dbg.set_register("al",decimal_value)

    def GetEBX(self):
        return self.dbg.get_register("ebx")

    def SetEBX(self,decimal_value):
        return self.dbg.set_register("ebx",decimal_value)

    def GetBX(self):
        return self.dbg.get_register("bx")

    def SetBX(self,decimal_value):
        return self.dbg.set_register("bx",decimal_value)

    def GetBH(self):
        return self.dbg.get_register("bh")

    def SetBH(self,decimal_value):
        return self.dbg.set_register("bh",decimal_value)

    def GetBL(self):
        return self.dbg.get_register("bl")

    def SetBL(self,decimal_value):
        return self.dbg.set_register("bl",decimal_value)

    def GetECX(self):
        return self.dbg.get_register("ecx")

    def SetECX(self,decimal_value):
        return self.dbg.set_register("ecx",decimal_value)

    def GetCX(self):
        return self.dbg.get_register("cx")

    def SetCX(self,decimal_value):
        return self.dbg.set_register("cx",decimal_value)

    def GetCH(self):
        return self.dbg.get_register("ch")

    def SetCH(self,decimal_value):
        return self.dbg.set_register("ch",decimal_value)

    def GetCL(self):
        return self.dbg.get_register("cl")

    def SetCL(self,decimal_value):
        return self.dbg.set_register("cl",decimal_value)

    def GetEDX(self):
        return self.dbg.get_register("edx")

    def SetEDX(self,decimal_value):
        return self.dbg.set_register("edx",decimal_value)

    def GetDX(self):
        return self.dbg.get_register("dx")

    def SetDX(self,decimal_value):
        return self.dbg.set_register("dx",decimal_value)

    def GetDH(self):
        return self.dbg.get_register("dh")

    def SetDH(self,decimal_value):
        return self.dbg.set_register("dh",decimal_value)

    def GetDL(self):
        return self.dbg.get_register("dl")

    def SetDL(self,decimal_value):
        return self.dbg.set_register("dl",decimal_value)

    def GetEDI(self):
        return self.dbg.get_register("edi")

    def SetEDI(self,decimal_value):
        return self.dbg.set_register("edi",decimal_value)

    def GetDI(self):
        return self.dbg.get_register("di")

    def SetDI(self,decimal_value):
        return self.dbg.set_register("di",decimal_value)

    def GetESI(self):
        return self.dbg.get_register("esi")

    def SetESI(self,decimal_value):
        return self.dbg.set_register("esi",decimal_value)

    def GetSI(self):
        return self.dbg.get_register("si")

    def SetSI(self,decimal_value):
        return self.dbg.set_register("si",decimal_value)

    def GetEBP(self):
        return self.dbg.get_register("ebp")

    def SetEBP(self,decimal_value):
        return self.dbg.set_register("ebp",decimal_value)

    def GetBP(self):
        return self.dbg.get_register("bp")

    def SetBP(self,decimal_value):
        return self.dbg.set_register("bp",decimal_value)

    def GetESP(self):
        return self.dbg.get_register("esp")

    def SetESP(self,decimal_value):
        return self.dbg.set_register("esp",decimal_value)

    def GetSP(self):
        return self.dbg.get_register("sp")

    def SetSP(self,decimal_value):
        return self.dbg.set_register("sp",decimal_value)

    def GetEIP(self):
        return self.dbg.get_register("eip")

    def SetEIP(self,decimal_value):
        return self.dbg.set_register("eip",decimal_value)

    def GetDR0(self):
        return self.dbg.get_register("dr0")

    def SetDR0(self,decimal_value):
        return self.dbg.set_register("dr0",decimal_value)

    def GetDR1(self):
        return self.dbg.get_register("dr1")

    def SetDR1(self,decimal_value):
        return self.dbg.set_register("dr1",decimal_value)

    def GetDR2(self):
        return self.dbg.get_register("dr2")

    def SetDR2(self,decimal_value):
        return self.dbg.set_register("dr2",decimal_value)

    def GetDR3(self):
        return self.dbg.get_register("dr3")

    def SetDR3(self,decimal_value):
        return self.dbg.set_register("dr3",decimal_value)

    def GetDR6(self):
        return self.dbg.get_register("dr6")

    def SetDR6(self,decimal_value):
        return self.dbg.set_register("dr6",decimal_value)

    def GetDR7(self):
        return self.dbg.get_register("dr7")

    def SetDR7(self,decimal_value):
        return self.dbg.set_register("dr7",decimal_value)

    # 64位寄存器
    def GetRAX(self):
        return self.dbg.get_register("rax")

    def SetRAX(self,decimal_int):
        return self.dbg.set_register("rax",decimal_int)

    def GetRBX(self):
        return self.dbg.get_register("rbx")

    def SetRBX(self,decimal_int):
        return self.dbg.set_register("rbx",decimal_int)

    def GetRCX(self):
        return self.dbg.get_register("rcx")

    def SetRCX(self,decimal_int):
         return self.dbg.set_register("rcx",decimal_int)

    def GetRDX(self):
        return self.dbg.get_register("rdx")

    def SetRDX(self,decimal_int):
         return self.dbg.set_register("rdx",decimal_int)

    def GetRSI(self):
        return self.dbg.get_register("rsi")

    def SetRSI(self,decimal_int):
         return self.dbg.set_register("rsi",decimal_int)

    def GetSIL(self):
        return self.dbg.get_register("sit")

    def SetSIL(self,decimal_int):
         return self.dbg.set_register("sit",decimal_int)

    def GetRDI(self):
        return self.dbg.get_register("rdi")

    def SetRDI(self,decimal_int):
         return self.dbg.set_register("rdi",decimal_int)

    def GetDIL(self):
        return self.dbg.get_register("dit")

    def SetDIL(self,decimal_int):
         return self.dbg.set_register("dit",decimal_int)

    def GetRBP(self):
        return self.dbg.get_register("rbp")

    def SetRBP(self,decimal_int):
         return self.dbg.set_register("rbp",decimal_int)

    def GetBPL(self):
        return self.dbg.get_register("bpl")

    def SetBPL(self,decimal_int):
         return self.dbg.set_register("bpl",decimal_int)

    def GetRSP(self):
        return self.dbg.get_register("rsp")

    def SetRSP(self,decimal_int):
         return self.dbg.set_register("rsp",decimal_int)

    def GetSPL(self):
        return self.dbg.get_register("spl")

    def SetSPL(self,decimal_int):
         return self.dbg.set_register("spl",decimal_int)

    def GetRIP(self):
        return self.dbg.get_register("rip")

    def SetRIP(self,decimal_int):
         return self.dbg.set_register("rip",decimal_int)

    def GetR8(self):
        return self.dbg.get_register("r8")

    def SetR8(self,decimal_int):
         return self.dbg.set_register("r8",decimal_int)

    def GetR8D(self):
        return self.dbg.get_register("r8d")

    def SetR8D(self,decimal_int):
         return self.dbg.set_register("r8d",decimal_int)

    def GetR8W(self):
        return self.dbg.get_register("r8w")

    def SetR8W(self,decimal_int):
         return self.dbg.set_register("r8w",decimal_int)

    def GetR8B(self):
        return self.dbg.get_register("r8b")

    def SetR8B(self,decimal_int):
         return self.dbg.set_register("r8b",decimal_int)

    def GetR9(self):
        return self.dbg.get_register("r9")

    def SetR9(self,decimal_int):
         return self.dbg.set_register("r9",decimal_int)

    def GetR9D(self):
        return self.dbg.get_register("r9d")

    def SetR9D(self,decimal_int):
         return self.dbg.set_register("r9d",decimal_int)

    def GetR9W(self):
        return self.dbg.get_register("r9w")

    def SetR9W(self,decimal_int):
         return self.dbg.set_register("r9w",decimal_int)

    def GetR9B(self):
        return self.dbg.get_register("r9b")

    def SetR9B(self,decimal_int):
         return self.dbg.set_register("r9b",decimal_int)

    def GetR10(self):
        return self.dbg.get_register("r10")

    def SetR10(self,decimal_int):
         return self.dbg.set_register("r10",decimal_int)

    def GetR10D(self):
        return self.dbg.get_register("r10d")

    def SetR10D(self,decimal_int):
         return self.dbg.set_register("r10d",decimal_int)

    def GetR10W(self):
        return self.dbg.get_register("r10w")

    def SetR10W(self,decimal_int):
         return self.dbg.set_register("r10w",decimal_int)

    def GetR10B(self):
        return self.dbg.get_register("r10b")

    def SetR10B(self,decimal_int):
         return self.dbg.set_register("r10b",decimal_int)

    def GetR11(self):
        return self.dbg.get_register("r11")

    def SetR11(self,decimal_int):
         return self.dbg.set_register("r11",decimal_int)

    def GetR11D(self):
        return self.dbg.get_register("r11d")

    def SetR11D(self,decimal_int):
         return self.dbg.set_register("r11d",decimal_int)

    def GetR11W(self):
        return self.dbg.get_register("r11w")

    def SetR11W(self,decimal_int):
         return self.dbg.set_register("r11w",decimal_int)

    def GetR11B(self):
        return self.dbg.get_register("r11b")

    def SetR11B(self,decimal_int):
         return self.dbg.set_register("r11b",decimal_int)

    def GetR12(self):
        return self.dbg.get_register("r12")

    def SetR12(self,decimal_int):
         return self.dbg.set_register("r12",decimal_int)

    def GetR12D(self):
        return self.dbg.get_register("r12d")

    def SetR12D(self,decimal_int):
         return self.dbg.set_register("r12d",decimal_int)

    def GetR12W(self):
        return self.dbg.get_register("r12w")

    def SetR12W(self,decimal_int):
         return self.dbg.set_register("r12w",decimal_int)

    def GetR12B(self):
        return self.dbg.get_register("r12b")

    def SetR12B(self,decimal_int):
         return self.dbg.set_register("r12b",decimal_int)

    def GetR13(self):
        return self.dbg.get_register("r13")

    def SetR13(self,decimal_int):
         return self.dbg.set_register("r13",decimal_int)

    def GetR13D(self):
        return self.dbg.get_register("r13d")

    def SetR13D(self,decimal_int):
         return self.dbg.set_register("r13d",decimal_int)

    def GetR13W(self):
        return self.dbg.get_register("r13w")

    def SetR13W(self,decimal_int):
         return self.dbg.set_register("r13w",decimal_int)

    def GetR13B(self):
        return self.dbg.get_register("r13b")

    def SetR13B(self,decimal_int):
         return self.dbg.set_register("r13b",decimal_int)

    def GetR14(self):
        return self.dbg.get_register("r14")

    def SetR14(self,decimal_int):
         return self.dbg.set_register("r14",decimal_int)

    def GetR14D(self):
        return self.dbg.get_register("r14d")

    def SetR14D(self,decimal_int):
         return self.dbg.set_register("r14d",decimal_int)

    def GetR14W(self):
        return self.dbg.get_register("r14w")

    def SetR14W(self,decimal_int):
         return self.dbg.set_register("r14w",decimal_int)

    def GetR14B(self):
        return self.dbg.get_register("r14b")

    def SetR14B(self,decimal_int):
         return self.dbg.set_register("r14b",decimal_int)

    def GetR15(self):
        return self.dbg.get_register("r15")

    def SetR15(self,decimal_int):
         return self.dbg.set_register("r15",decimal_int)

    def GetR15D(self):
        return self.dbg.get_register("r15d")

    def SetR15D(self,decimal_int):
         return self.dbg.set_register("r15d",decimal_int)

    def GetR15W(self):
        return self.dbg.get_register("r15w")

    def SetR15W(self,decimal_int):
         return self.dbg.set_register("r15w",decimal_int)

    def GetR15B(self):
        return self.dbg.get_register("r15b")

    def SetR15B(self,decimal_int):
         return self.dbg.set_register("r15b",decimal_int)

    # 标志位读写
    def GetZF(self):
        return self.dbg.get_flag_register("zf")

    def SetZF(self,decimal_bool):
        return self.dbg.set_flag_register("zf",decimal_bool)

    def GetOF(self):
        return self.dbg.get_flag_register("of")

    def SetOF(self,decimal_bool):
        return self.dbg.set_flag_register("of",decimal_bool)

    def GetCF(self):
        return self.dbg.get_flag_register("cf")

    def SetCF(self,decimal_bool):
        return self.dbg.set_flag_register("cf",decimal_bool)

    def GetPF(self):
        return self.dbg.get_flag_register("pf")

    def SetPF(self,decimal_bool):
        return self.dbg.set_flag_register("pf",decimal_bool)

    def GetSF(self):
        return self.dbg.get_flag_register("sf")

    def SetSF(self,decimal_bool):
        return self.dbg.set_flag_register("sf",decimal_bool)

    def GetTF(self):
        return self.dbg.get_flag_register("tf")

    def SetTF(self,decimal_bool):
        return self.dbg.set_flag_register("tf",decimal_bool)

    def GetAF(self):
        return self.dbg.get_flag_register("af")

    def SetAF(self,decimal_bool):
        return self.dbg.set_flag_register("af",decimal_bool)

    def GetDF(self):
        return self.dbg.get_flag_register("df")

    def SetDF(self,decimal_bool):
        return self.dbg.set_flag_register("df",decimal_bool)

    def GetIF(self):
        return self.dbg.get_flag_register("if")

    def SetIF(self,decimal_bool):
        return self.dbg.set_flag_register("if",decimal_bool)

    # 传入文件路径,载入被调试程序
    def Script_InitDebug(self, path):
        try:
            return self.dbg.run_command_exec(f"InitDebug {path}")
        except Exception:
            return False
        return False

    # 终止当前被调试进程
    def Script_CloseDebug(self):
        try:
            return self.dbg.run_command_exec("StopDebug")
        except Exception:
            return False
        return False

    # 让进程脱离当前调试器
    def Script_DetachDebug(self):
        try:
            return self.dbg.run_command_exec("DetachDebugger")
        except Exception:
            return False
        return False

    # 让进程运行起来
    def Script_RunDebug(self):
        try:
            self.dbg.run_command_exec("run")
            return True
        except Exception:
            return False
        return False

    # 释放锁并允许程序运行，忽略异常
    def Script_ERun(self):
        try:
            self.dbg.run_command_exec("erun")
            return True
        except Exception:
            return False
        return False

    # 释放锁并允许程序运行，跳过异常中断
    def Script_SeRun(self):
        try:
            self.dbg.run_command_exec("serun")
            return True
        except Exception:
            return False
        return False

    # 暂停调试器运行
    def Script_Pause(self):
        try:
            self.dbg.run_command_exec("pause")
            return True
        except Exception:
            return False
        return False

    # 步进
    def Script_StepInto(self):
        try:
            self.dbg.run_command_exec("StepInto")
            return True
        except Exception:
            return False
        return False

    # 步进,跳过异常
    def Script_EStepInfo(self):
        try:
            self.dbg.run_command_exec("eStepInto")
            return True
        except Exception:
            return False
        return False

    # 步进,跳过中断
    def Script_SeStepInto(self):
        try:
            self.dbg.run_command_exec("seStepInto")
            return True
        except Exception:
            return False
        return False

    # 步过到结束
    def Script_StepOver(self):
        try:
            self.dbg.run_command_exec("StepOver")
            return True
        except Exception:
            return False
        return False

    # 普通步过F8
    def Script_StepOut(self):
        try:
            self.dbg.run_command_exec("StepOut")
            return True
        except Exception:
            return False
        return False

    # 普通步过F8，忽略异常
    def Script_eStepOut(self):
        try:
            self.dbg.run_command_exec("eStepOut")
            return True
        except Exception:
            return False
        return False

    # 跳过执行
    def Script_Skip(self):
        try:
            self.dbg.run_command_exec("skip")
            return True
        except Exception:
            return False
        return False

    # 递增寄存器
    def Script_Inc(self,register):
        try:
            self.dbg.run_command_exec(f"inc {register}")
            return True
        except Exception:
            return False
        return False

    # 递减寄存器
    def Script_Dec(self,register):
        try:
            self.dbg.run_command_exec(f"dec {register}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器进行add运算
    def Script_Add(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"add {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器进行sub运算
    def Script_Sub(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"sub {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器进行mul乘法
    def Script_Mul(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"mul {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器进行div除法
    def Script_Div(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"div {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器进行and与运算
    def Script_And(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"and {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器进行or或运算
    def Script_Or(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"or {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器进行xor或运算
    def Script_Xor(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"xor {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器参数进行neg反转
    def Script_Neg(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"neg {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器进行rol循环左移
    def Script_Rol(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"rol {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器进行ror循环右移
    def Script_Ror(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"ror {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器进行shl逻辑左移
    def Script_Shl(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"shl {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器进行shr逻辑右移
    def Script_Shr(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"shr {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器进行sal算数左移
    def Script_Sal(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"sal {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器进行sar算数右移
    def Script_Sar(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"sar {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器进行not按位取反
    def Script_Not(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"not {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 进行字节交换，也就是反转。
    def Script_Bswap(self,register,decimal_int):
        try:
            self.dbg.run_command_exec(f"bswap {register},{decimal_int}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器入栈
    def Script_Push(self,register_or_value):
        try:
            self.dbg.run_command_exec(f"push {register_or_value}")
            return True
        except Exception:
            return False
        return False

    # 对寄存器弹出元素
    def Script_Pop(self,register_or_value):
        try:
            self.dbg.run_command_exec(f"pop {register_or_value}")
            return True
        except Exception:
            return False
        return False

    # 内置API暂停
    def Pause(self):
        try:
            self.dbg.set_debug("Pause")
            return True
        except Exception:
            return False
        return False

    # 内置API运行
    def Run(self):
        try:
            self.dbg.set_debug("Run")
            return True
        except Exception:
            return False
        return False

    # 内置API步入
    def StepIn(self):
        try:
            self.dbg.set_debug("StepIn")
            return True
        except Exception:
            return False
        return False

    # 内置API步过
    def StepOut(self):
        try:
            self.dbg.set_debug("StepOut")
            return True
        except Exception:
            return False
        return False

    # 内置API到结束
    def StepOut(self):
        try:
            self.dbg.set_debug("StepOut")
            return True
        except Exception:
            return False
        return False

    # 内置API停止
    def Stop(self):
        try:
            self.dbg.set_debug("Stop")
            return True
        except Exception:
            return False
        return False

    # 内置API等待
    def Wait(self):
        try:
            self.dbg.set_debug("Wait")
            return True
        except Exception:
            return False
        return False

    # 判断调试器是否在调试
    def IsDebug(self):
        try:
            return self.dbg.is_debugger()
        except Exception:
            return False
        return False

    # 判断调试器是否在运行
    def IsRunning(self):
        try:
            return self.dbg.is_running()
        except Exception:
            return False
        return False
