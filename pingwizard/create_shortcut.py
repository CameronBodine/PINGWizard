
import os, sys
import platform
import subprocess

PySimpleGUI_License = 'e3yAJ9MVaOWANplCbmndNNl2VwHvlCwpZTSjIl6DIjkiRGpYc53aRty8aBWpJF1qdwGLlzv9bUiHILs3Inkyxpp5Yq2OVku8cg2ZVrJ7RNCQI66bMcTLcnyKMbTRMK57OCTPMGxGNtS8whirTBGTlLjxZEWg5DzWZdUXRUlLcDGfxnv7eiWB1jlOb6nqR8WTZ2XsJVzbabW19ouWI6j0oXiKN0Si4AwtI7iFw8iGTBmtFftjZEUxZMpYcLncNk0rIJj4oyisQq2uFCtqZnXWJvvqbEiCICsSIbkC5jhKbvWTVqM2YtX6Ni0XIJjloji1QEmU9Ak5ayWp5nlnIwi3wiiOQK279ytqcKGwFGuvepS6IH6iIOiYIGs7I4kYNQ13cY33RkvIbqWkVyypSKUOQoiZO2ijIFzaMNTEAp0bNxyWI1sLIwkRRjhZdNGBVoJkcZ3MNN1yZMWTQtihOiieIYyXMDDIIF0ILaTyAt36LKTREj5JI1iYwcixRgGuFk0BZGU5VZ4dciGUl3ykZ3XtMbilOMiBIhy1M5DtId1mL6T1A935LYTLEN5iI3iJwoirR8Wa12h5a0WtxkBNZdGiRJyYZXX9N5zZI2jSoZizYpmp9YkHaIWz5YluLTmcNXzNQmGZd0twYGW6l3sALZmTNWvubcSEItsPITk6lFQgQUWZRrkfcEmAVxz0c9y7IG6sILjZEYyzO8Cf4c0WLDj3QCwSLwjPEt2BMMi0J69p854e39898f71ea82d3a530f7a6ed8a02a4eea9ffd2c7b1279074b491c71b411f392e6d726a2d2f9dbf63388356cf4e083e358fe428852d676073e128607b9ad194c15e34a4feb463a749fd3295606caa293b823d102e854cd845b79b5ec5eaec0b2ef7f9cf0c87b2dfcad3f14cd0d66a2da97e6b38a535eb8707b4486c9802a4bfeb09703382e157449096f0e3551af9f444197cacb3f3d42187cea97ab61978985ddeecd086b9cb86c4ec1c08082d47b3ed0ae9c044d9aa65e5c9bf6e00238f78ed858cfdaf0021fb95d636e0cce84d84d2c2da7ac57f2e54fe793fce44a8b8abf96ce7c381f4b7eeb55dc4b68768e8172a4dffc1b683e62a108b2dfc2ef340dab058e6ee5c1f525f93e89d39258862f099987a8ec7022db5aecb5a58e81d02370d5717d18498ae58749aa5e463cf757ab7fa84efe49c1b770da397eef22423696ad433e7232646e279906bef084b21714ac5fc2af564a03ebc789123aed44531765b3e72c6165131feab68e35e0276a64760ee9abf043bece1e3cd148bcec97ab835395391387ff9d2b74a835a15ea5bac9c7e1218c217481a3999a91e037a138aaf5dddadb2247141242140b130e273aab5e1e6855fae8b7ee80d64be2d09a46f3d49555f53a7a849138fc3b9d2323658ea7e86a0039c40f3c15fd3647f99ec98232d9734a5933177c48c6575a1415e2808640cfb27773e728fe128b99757'
import PySimpleGUI as sg

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