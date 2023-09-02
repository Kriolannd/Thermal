import os
import time
import subprocess

txt_files = ["F1.txt", "F4.txt", "F5.txt", "F6.txt", "F7.txt"]
for txt_file in txt_files:
    open(txt_file, "w").close()


filename = 'launch.txt'
scripts = ["distortion.py", "solver.py", "pi_controller.py"]

initial_timestamp = os.path.getmtime(filename)

while True:
    current_timestamp = os.path.getmtime(filename)
    if current_timestamp > initial_timestamp:
        initial_timestamp = current_timestamp
        

        with open(filename, 'r') as file:
            contents = file.read()

        if '1' in contents:
            for script in scripts:
                subprocess.Popen(['python', script])
        else:
            sys.exit()
    time.sleep(1)
