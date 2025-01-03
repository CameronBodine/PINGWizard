
import os, sys

from pathlib import Path
home_path = os.path.join(Path.home())

def windows_shortcut(conda_env, conda_key, bat_file):

    to_write = "@echo off\n"+\
               "set conda_base={}\n".format(conda_env)+\
               "set conda_key={}\n".format(conda_key)+\
               "\n\n"+\
               "call conda activate %conda_base%\n"+\
               "if ERRORLEVEL 1 (echo Error! Cannot load Conda environment.)\n"+\
               "goto run_script\n\n"+\
               ":run_script\n"+\
               "echo Launching PINGWizard\n"+\
               "python -m pingwizard\n"
                
    print('\n\n', to_write)

    with open(bat_file, 'w') as f:
        f.write(to_write)

    return

def linux_shortcut(conda_env, conda_key):

    # Need to update, skipping for now

    to_write = "#!/bin/bash\n"+\
               """set conda_base="{}"\n""".format(conda_env)+\
               "set conda_key={}\n".format(conda_key)+\
               "\n\n"+\
               "call conda activate %conda_base%\n"+\
               "if ERRORLEVEL 1 (echo Error! Cannot load Conda environment.)\n"+\
               "goto run_script\n\n"+\
               ":run_script\n"+\
               "echo Launching PINGWizard\n"+\
               "python -m pingwizard\n"

    pass

def create_shortcut():

    # Get Conda Info
    conda_env = os.environ['CONDA_PREFIX']
    print("\n\nConda Env:\t\t", conda_env)

    if 'miniforge' in conda_env:
        conda_key = 'mamba'
    else:
        conda_key = 'conda'
    print("Conda Key:\t\t", conda_key)

    bat_file_path = os.path.join(home_path, "Desktop", "Launch PINGWizard.bat")

    if "Windows" in os.environ['OS']:
        print("Creating Windows Shortcut")
        windows_shortcut(conda_env, conda_key, bat_file_path)

    else:
        print("Creating Linux Shortcut")
        linux_shortcut(conda_env, conda_key)

    pass

if __name__ == "__main__":
    create_shortcut()