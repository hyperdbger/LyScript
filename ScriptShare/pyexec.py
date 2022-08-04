from LyScript32 import MyDebug
import traceback
import sys,string

DESC = "Non interactive python shell [immlib already imported]"

def usage(dbg):
    dbg.set_loger_output("!pyexec code")
    dbg.set_loger_output("%s" % DESC)

def main(args):
    dbg = MyDebug()
    connect_flag = dbg.connect()
    if connect_flag == False:
        exit()

    if args:
        commands = string.joinfields(args, "")
        try:
            exec(commands)
        except:
            error = traceback.format_exception_only(sys.exc_type, sys.exc_value)
            dbg.set_loger_output("Error on: %s" % commands)
            for line in error:
                line = line.strip()
                dbg.set_loger_output(line)
            return line
    else:
        return "No python command given"
    dbg.close()

if __name__ == "__main__":
    main("cmd")