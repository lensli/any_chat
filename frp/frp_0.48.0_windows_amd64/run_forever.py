import os
import shutil
import subprocess

while True:
    if not os.path.exists("frpc.exe"):
        if os.path.exists("back/frpc.exe"):
            shutil.copy("back/frpc.exe", ".")
        else:
            print("frpc.exe not found in back folder. Please add it and restart the script.")
            break

    subprocess.run(["frpc.exe", "-c", "frpc.ini"])
