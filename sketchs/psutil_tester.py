import psutil

for process in psutil.process_iter():
    if len(process.cmdline())>=2:
        if "scripts/" in process.cmdline()[1]:
            print(process.pid)
