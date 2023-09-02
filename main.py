import subprocess
from time import sleep

txt_files = ["F1.txt", "F4.txt", "F5.txt", "F6.txt", "F7.txt"]
for txt_file in txt_files:
    open(txt_file, "w").close()

files = ["distortion.py", "solver.py", "pi_controller.py", "all_graphs_2str_v3.py"]
for file in files:
    subprocess.Popen(args=["start", "python", file], shell=True, stdout=subprocess.PIPE)
