from x86smt.sequenceanalyzer import MyDebugger
from deplib.deplib20 import DeplibFinder
from deplib.libgadgets import GadgetsDB
import getopt
from immlib import *

def usage(imm):
    imm.log("!findpivot")
    imm.log("Defaults between square brackets")
    imm.log("  -e               = An expression for memory controlled by the attacker to pivot to.")
    imm.log("  -t sqlite3|mysql = Type of DB [sqlite3]")
    imm.log("  -n dbname        = DB name ['gadgets.sq3' if sqlite3 or 'gadgets' if mysql]")
    imm.log("  -h host          = host for the DB connection [127.0.0.1]")
    imm.log("  -u username      = username for the DB connection")
    imm.log("  -p password      = password for the DB connection")
    imm.log("  -m module        = Module to use [use all modules in the DB]")
    imm.log("  -d               = Activate debugging")
    imm.log("  -l               = Log everything in a file")
    imm.log("")
    imm.log("multiple -m options are accepted")
    imm.log("a module option can receive the version to use too, for example: ntdll.dll|5.1.2600.5512")
    imm.log("")
    imm.log("Expression examples (basically a python expression using PrettySolver):")
    imm.log("EAX: means we control the memory area pointed by EAX")
    imm.log("mem(EBP)+4: we control the memory area found after dereferencing EBP and adding 4")

def main( args ):
    imm = Debugger()
    
    try:
        opts, argo = getopt.getopt(args, "e:t:n:h:u:p:m:dl")
    except getopt.GetoptError, reason:
        imm.log("[!] Exception when parsing arguments: %s" % reason)
        usage(imm)
        return "Error parsing arguments. See log for details"

    dbtype = dbname = host = username = passwd = exp = None
    debug = logfile = False
    modules=[]
    for o, a in opts:
        if o == "-e":
            exp = a
        elif o == "-t":
            dbtype = a
        elif o == "-n":
            dbname = a
        elif o == "-h":
            host = a
        elif o == "-u":
            username = a
        elif o == "-p":
            passwd = a
        elif o == "-m":
            modules.append(a.split("|"))
        elif o == "-d":
            debug=True
        elif o == "-l":
            logfile=True
        else:
            usage(imm)
            return "Unknown option"
    
    if not exp:
        usage(imm)
        imm.log("[!] -e is mandatory")
        return "Error, check script usemode"
    
    if logfile:
        imm = MyDebugger(template="findpivot-log-")
    
    gdb = GadgetsDB(imm, dbtype, dbname, host, username, passwd, quiet=True)
    gdb.debug=debug
    
    if not gdb.db_connection:
        imm.log("[!] Could not connect to db, exiting...")
        return "Failed to connect to DB"
    
    if not modules:
        modules=gdb.get_all_module_ids()
    else:
        modules=gdb.get_module_ids(modules)
    
    gdb.db_connection.close()
    
    dep=DeplibFinder({"stackpage":4, "roparea":("ESP",0), "dbtype":dbtype, "dbname":dbname, "host":host, "username":username, "passwd":passwd, "modules":modules})
    
    if debug:
        imm.log("[*] RAW Expression: %s"%str(exp))
    
    exp=parseExpression(exp, dep.sea)
    
    if exp == None:
        imm.log("[!] Expression could not be parsed, please review it")
        return "Error, check usemode"
    
    imm.log("[*] Parsed Expression: %s"%str(exp))
    
    findings=[]
    
    #simulate a XCHG ESP, EXP/RETN
    dep.sea.regs["ESP"]=exp
    dep.sea.EIP=dep.sea.readMemory(dep.sea.regs["ESP"], 4)
    dep.sea.regs["ESP"]+=4
    
    if debug:
        dep.sea.printState(imm)
    
    #first search by hashes
    imm.log("[*] Exact search (by hashes)")
    hashes=dep.sea.hashState()
    
    if debug:
        for k,v in hashes.iteritems():
            imm.log("HASH %s=%08X"%(k,v))
    
    for info in dep.gdb.search_by_hashes(hashes, dep.hashes):
        imm.log("modid=%d, offset=0x%x, complexity=%d"%(info[0], info[1], info[2]), dep.bases[info[0]]+info[1])
        findings.append(info)
    
    #then by properties
    imm.log("[*] Heuristic search (by gadget's properties). Only new findings are showed.")
    tmp=dep.sea.calcProperties()
    searchProps={}
    for k,v in tmp[0].iteritems():
        if v: searchProps[k]=v
    if tmp[1]:
        searchProps["FLAGS"]=(tmp[1], tmp[1]) #we only care about the flags that changed
    
    if debug:
        for k,v in searchProps.iteritems():
            imm.log("PROP %s=%s"%(k,v))
    
    if searchProps:
        for info in dep.gdb.search_by_properties(searchProps, dep.props):
            if info in findings:
                continue
            findings.append(info)
            gadget_sm=dep.gdb.get_gadget_by_offset(info[0], info[1])
            
            try:
                gEIP=gadget_sm.solver.exprString(gadget_sm.solver.simplify(gadget_sm.solver.extractExpr(gadget_sm.EIP, 0, 7)))
                tmp1=gadget_sm.memory.getIndexes(gEIP.replace("VAL","MEM"), recursive=False)
                tmp2=dep.sea.memory.getIndexes(str(dep.sea.EIP[0:8]).replace("VAL","MEM"), recursive=False)
            except:
                continue
    
            if tmp1 != tmp2: #confirm EIP follows the wanted structure
                continue
            
            tmp1 = set(gadget_sm.solver.getVarDependency(gadget_sm.regs["ESP"], return_name=True))
            tmp2 = set(dep.sea.solver.getVarDependency(dep.sea.regs["ESP"], return_name=True))
            
            if tmp1 != tmp2: #confirm ESP follows the wanted structure
                continue
            
            imm.log("modid=%d, offset=0x%x, complexity=%d"%(info[0], info[1], info[2]), dep.bases[info[0]]+info[1])
    
    return "Finished"

def parseExpression(exp, sm):
    loc={}
    loc.update(sm.regs)
    loc.update(sm.flags)
    loc["EIP"]=sm.EIP
    loc["mem"]=lambda exp: sm.readMemory(exp, 4)

    try:
        return eval(exp, globals(), loc)
    except:
        return None
