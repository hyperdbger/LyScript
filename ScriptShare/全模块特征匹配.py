from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    for entry in dbg.get_all_module():
        eip = entry.get("entry")

        if eip != 0:
            dbg.set_register("eip",eip)

            search = dbg.scan_memory_one("ff 25 ??")
            print(hex(search))

    dbg.close()