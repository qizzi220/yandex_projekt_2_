import subprocess
a = ['pygame', 'pytmx', 'win32api']
subprocess.check_call(["python", '-m', 'pip', 'install', 'pytmx']) # install pkg
# subprocess.check_call(["python", '-m', 'pip', 'install',"--upgrade", 'pygame']) # upgrade pkg