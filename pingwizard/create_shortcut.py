
import os, sys
import platform
import subprocess

from pathlib import Path
home_path = os.path.join(Path.home())

def windows_shortcut(conda_env: str, f: str):

    to_write = "set conda_env={}\n".format(conda_env)+\
               "\n"+\
               '''call conda activate %conda_env%\n\n'''+\
               "call conda env list\n\n"+\
               "echo Launching PINGWizard\n"+\
               "python -m pingwizard\n"
                
    print('\n\n', to_write)

    with open(f, 'w') as f:
        f.write(to_write)

    return

def linux_shortcut(conda_base: str, f: str):

    to_write = "#!/bin/bash\n"+\
               """conda_base="{}"\n""".format(conda_base)+\
               "\n"+\
               '''source $conda_base/bin/activate ping\n'''+\
               "\n"+\
               "echo Launching PINGWizard\n"+\
               "python -m pingwizard\n"
    
    print('\n\n', to_write)

    with open(f, 'w') as file:
        file.write(to_write)

    # Make executable
    subprocess.run('''chmod u+x "{}"'''.format(f), shell=True)

    # Print instructions
    print('\n\nLaunch PINGWizard from the console by passing')
    print(f)
    print('OR')
    print('./PINGWizard.sh')
    print('after navigating console to Desktop.\n\n')

    pass

def create_shortcut():

    # Make the file
    if "Windows" in platform.system():
        # Set conda_env and file_path
        conda_env = os.environ['CONDA_PREFIX']
        file_path = os.path.join(home_path, "Desktop", "PINGWizard.bat")

        windows_shortcut(conda_env=conda_env, f=file_path)

    else:
        # Get ping Environment Path
        conda_env = os.environ['CONDA_PREFIX']

        # Get Conda base path from ping environment path
        conda_base = conda_env.split('envs')[0]

        file_path = os.path.join(home_path, "Desktop", "PINGWizard.sh")
        linux_shortcut(conda_base=conda_base, f=file_path)


if __name__ == "__main__":
    create_shortcut()