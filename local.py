import subprocess

def local(cmd):
    
    process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if process.returncode == 0:
        print(process.stdout)
    else:
        print(process.returncode)
    return process.stdout

def local_real_time(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line = process.stdout.readline() or process.stderr.readline()
        if not line:
            break
        yield line.decode('utf-8')
    

def local_real_time_main(command):
    output = ""
    for path in local_real_time(command):
        print(path,end="")
        output = output + path
    return output