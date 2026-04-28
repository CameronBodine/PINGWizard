
import os, sys
import platform
import subprocess

import FreeSimpleGUI as sg

# Get user's home directory
home_path = os.path.expanduser('~')

def get_shortcut_location(home_p: str):

    # Set start path
    start_path = os.path.join(home_p, 'Desktop')

    # Check if start_path valid
    ## 'Desktop' name different based on os language
    if not os.path.exists(start_path):
        start_path = home_p

    ###################
    # Create simple gui
    title = sg.Text('Save shortcut at this location:')
    path_input = sg.Input(key='shortcut_path', default_text=start_path, size=(80, 1))
    path_browse = sg.FolderBrowse(initial_folder=start_path)

    layout = [
        [title],
        [path_input, path_browse],
        [sg.Submit(), sg.Quit()],
    ]

    layout2 =[[sg.Column(layout, scrollable=False)]]
    window = sg.Window('Set Shortcut Location', layout2, resizable=True)

    ##########
    # Open Gui
    while True:
        event, values = window.read()

        if event == "Quit" or event == "Submit":
            break

    window.close()

    if event == "Quit":
        sys.exit()

    return values['shortcut_path']
    

def windows_shortcut(conda_base: str, conda_env: str, f: str):

    to_write = """set conda_base="{}"\n""".format(conda_base)+\
               """set conda_env="{}"\n""".format(conda_env)+\
               "\n"+\
               '''call %conda_base%\\Scripts\\activate %conda_env%\n\n'''+\
               "call conda env list\n\n"+\
               "echo Launching PINGWizard\n"+\
               "python -m pingwizard\n"+\
               "pause"
                
    print('\n\n', to_write)

    with open(f, 'w') as file:
        file.write(to_write)

    print('\n\nShortcut saved here:', f)

    return

def linux_shortcut(conda_base: str, conda_env: str, f: str):

    to_write = "#!/bin/bash\n"+\
               """conda_base="{}"\n""".format(conda_base)+\
               """conda_env="{}"\n""".format(conda_env)+\
               "\n"+\
               '''source $conda_base/bin/activate $conda_env\n'''+\
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
    print('after navigating console to {}.\n\n'.format(os.path.dirname(f)))

    pass

def create_shortcut():

    # Get ping Environment Path
    conda_env = os.environ['CONDA_PREFIX']

    # Get Conda base path from ping environment path
    conda_base = conda_env.split('envs')[0]

    # Reset conda_env
    conda_env = 'ping'

    # Get shorcut location
    file_path = get_shortcut_location(home_path)

    # Make the file
    if "Windows" in platform.system():
        # Set file_path
        file_path = os.path.join(file_path, "PINGWizard.bat")
        windows_shortcut(conda_base=conda_base, conda_env=conda_env, f=file_path)

    else:
        # Set file_path
        file_path = os.path.join(file_path, "PINGWizard.sh")
        linux_shortcut(conda_base=conda_base, conda_env=conda_env, f=file_path)


if __name__ == "__main__":
    create_shortcut()