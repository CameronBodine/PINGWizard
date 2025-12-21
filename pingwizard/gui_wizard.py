
import sys, os
import time
import runpy
from pingwizard.version import __version__ as pwversion
from pingwizard.check_available_updates import check

from pingmapper.version import __version__ as pmversion

PySimpleGUI_License = 'e3yAJ9MVaOWANplCbmndNNl2VwHvlCwpZTSjIl6DIjkiRGpYc53aRty8aBWpJF1qdwGLlzv9bUiHILs3Inkyxpp5Yq2OVku8cg2ZVrJ7RNCQI66bMcTLcnyKMbTRMK57OCTPMGxGNtS8whirTBGTlLjxZEWg5DzWZdUXRUlLcDGfxnv7eiWB1jlOb6nqR8WTZ2XsJVzbabW19ouWI6j0oXiKN0Si4AwtI7iFw8iGTBmtFftjZEUxZMpYcLncNk0rIJj4oyisQq2uFCtqZnXWJvvqbEiCICsSIbkC5jhKbvWTVqM2YtX6Ni0XIJjloji1QEmU9Ak5ayWp5nlnIwi3wiiOQK279ytqcKGwFGuvepS6IH6iIOiYIGs7I4kYNQ13cY33RkvIbqWkVyypSKUOQoiZO2ijIFzaMNTEAp0bNxyWI1sLIwkRRjhZdNGBVoJkcZ3MNN1yZMWTQtihOiieIYyXMDDIIF0ILaTyAt36LKTREj5JI1iYwcixRgGuFk0BZGU5VZ4dciGUl3ykZ3XtMbilOMiBIhy1M5DtId1mL6T1A935LYTLEN5iI3iJwoirR8Wa12h5a0WtxkBNZdGiRJyYZXX9N5zZI2jSoZizYpmp9YkHaIWz5YluLTmcNXzNQmGZd0twYGW6l3sALZmTNWvubcSEItsPITk6lFQgQUWZRrkfcEmAVxz0c9y7IG6sILjZEYyzO8Cf4c0WLDj3QCwSLwjPEt2BMMi0J69p854e39898f71ea82d3a530f7a6ed8a02a4eea9ffd2c7b1279074b491c71b411f392e6d726a2d2f9dbf63388356cf4e083e358fe428852d676073e128607b9ad194c15e34a4feb463a749fd3295606caa293b823d102e854cd845b79b5ec5eaec0b2ef7f9cf0c87b2dfcad3f14cd0d66a2da97e6b38a535eb8707b4486c9802a4bfeb09703382e157449096f0e3551af9f444197cacb3f3d42187cea97ab61978985ddeecd086b9cb86c4ec1c08082d47b3ed0ae9c044d9aa65e5c9bf6e00238f78ed858cfdaf0021fb95d636e0cce84d84d2c2da7ac57f2e54fe793fce44a8b8abf96ce7c381f4b7eeb55dc4b68768e8172a4dffc1b683e62a108b2dfc2ef340dab058e6ee5c1f525f93e89d39258862f099987a8ec7022db5aecb5a58e81d02370d5717d18498ae58749aa5e463cf757ab7fa84efe49c1b770da397eef22423696ad433e7232646e279906bef084b21714ac5fc2af564a03ebc789123aed44531765b3e72c6165131feab68e35e0276a64760ee9abf043bece1e3cd148bcec97ab835395391387ff9d2b74a835a15ea5bac9c7e1218c217481a3999a91e037a138aaf5dddadb2247141242140b130e273aab5e1e6855fae8b7ee80d64be2d09a46f3d49555f53a7a849138fc3b9d2323658ea7e86a0039c40f3c15fd3647f99ec98232d9734a5933177c48c6575a1415e2808640cfb27773e728fe128b99757'
import PySimpleGUI as sg

# Script directory
# Add 'pingmapper' to the path, may not need after pypi package...
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.append(PACKAGE_DIR)

# Logo's
env_dir = os.environ['CONDA_PREFIX']
pingmapper_logo_name = "PINGMapper_Logo_small.png"
pingmapper_logo = os.path.join(env_dir, 'pingmapper_config', pingmapper_logo_name)
if not os.path.isfile(pingmapper_logo):
    pingmapper_logo = os.path.join(SCRIPT_DIR, "assets", pingmapper_logo_name)

def wizard():

    print("Welcome to the PING Wizard!")

    # Default to debug verbosity for installer runs unless explicitly overridden
    if 'PINGINSTALLER_VERBOSITY' not in os.environ:
        os.environ['PINGINSTALLER_VERBOSITY'] = 'debug'

    # Save the original sys.argv
    original_argv = sys.argv

    ##########################
    # Define the layout blocks

    # Title #
    title = sg.Text("PING Wizard", font=("Helvetica", 24), justification="center", size=(25, 1))
    version = sg.Text("ver. {}".format(pwversion), font=("Helvetica", 8), justification="center", size=(75, 1))

    # PINGMapper #
    ## Title
    pm_title = sg.Text("PINGMapper", font=("Helvetica", 16), justification="center")
    
    ## Description
    pm_desc = sg.Text("PINGMapper (ver. {}) - Open-source interface for processing recreation-grade side scan sonar datasets and reproducibly mapping benthic habitat.".format(pmversion), font=("Helvetica", 10), justification="left", size=(30, 5))

    ## Logo
    pm_logo = sg.Image(pingmapper_logo, size=(200, 120))

    ## Launch GUI Buttons
    pm_gui_text = sg.Text("Process\nSonar Log", font=("Helvetica", 10, "bold"), size=(11, 2))
    pm_gui_btn = sg.Button("Single Log", key="launch_pingmapper_gui", button_color="green", size=(10, 2))
    pm_batch_gui_btn = sg.Button("Batch\nSonar Logs", key="launch_pingmapper_batch_gui", button_color="darkgreen", size=(10, 2))

    ## Test Buttons
    pm_test_text = sg.Text("Test\nPINGMapper", font=("Helvetica", 10, "bold"),size=(11, 2))
    pm_test_single_btn = sg.Button("Small\nDataset", key="test", button_color="navy", size=(10, 2))
    pm_test_batch_btn = sg.Button("Large\nDataset", key="test_large", size=(10, 2))

    ## Update Installation Buttons
    pm_install_text = sg.Text("Update\nPINGMapper", font=("Helvetica", 10, "bold"),size=(11, 2))
    pm_install_btn = sg.Button("Update", key="pinginstaller", button_color="darkorange", size=(10, 2))
    pm_check_btn = sg.Button("Check for Updates", key="check_updates", button_color="grey", size=(10, 2))


    #############
    # Exit Button
    exit_btn = sg.Button("Quit", key="exit_pingwizard", font=("Helvetica", 12, "bold"), button_color="darkred", size=(10, 1))

    layout = [
        [title],
        [version],
        [sg.HorizontalSeparator()],
        [sg.HorizontalSeparator()],
        [pm_logo, pm_desc],
        # [pm_title],
        # [pm_desc],
        [pm_gui_text, sg.VerticalSeparator(), pm_gui_btn, pm_batch_gui_btn],
        [pm_test_text, sg.VerticalSeparator(), pm_test_single_btn, pm_test_batch_btn],
        [pm_install_text, sg.VerticalSeparator(), pm_install_btn, pm_check_btn],
        [sg.HorizontalSeparator()],
        [sg.HorizontalSeparator()],
        [exit_btn],
    ]


    layout2 =[[sg.Column(layout, scrollable=True,  vertical_scroll_only=True, size_subsample_height=1)]]
    window = sg.Window('PING Wizard', layout2, resizable=True)


    #################
    # Open the wizard
    while True:
        event, values = window.read()
        if event == "exit_pingwizard" or event == "Submit":
            break
    

        # Launch PINGMapper GUI
        if event == "launch_pingmapper_gui":
            print("Launching PINGMapper GUI...")
            # Set the arguments for the PINGMapper GUI
            module_name = "pingmapper"
            module_args = ["gui"]

        elif event == "launch_pingmapper_batch_gui":
            print("Launching PINGMapper Batch GUI...")
            # Set the arguments for the PINGMapper Batch GUI
            module_name = "pingmapper"
            module_args = ["gui_batch"]

        elif event == "test":
            print("Testing PINGMapper...")
            # Set the arguments for the PINGMapper GUI
            module_name = "pingmapper"
            module_args = ["test"]

        elif event == "test_large":
            print("Testing PINGMapper Batch...")
            # Set the arguments for the PINGMapper Batch GUI
            module_name = "pingmapper"
            module_args = ["test_large"]

        elif event == "pinginstaller":
            # Update pinginstaller first to ensure latest installer is used
            try:
                from pinginstaller.Install_Update import update_pinginstaller
                update_pinginstaller()
            except Exception as e:
                print(f"Warning: failed to update pinginstaller: {e}")

            print("Updating PINGMapper...")
            # Set the arguments for the PINGMapper Batch GUI
            module_name = "pinginstaller"
            module_args = []

        elif event == "check_updates":
            print("Checking for updates...")
            # Set the arguments for the PINGMapper Batch GUI
            module_name = "pinginstaller"
            module_args = ["check"]

        window.Disappear()
        sys.argv = [module_name, *module_args]
        
        # Ensure environment is properly set for installer (mamba/conda detection)
        # The installer relies on CONDA_PREFIX to find mamba
        if 'CONDA_PREFIX' not in os.environ:
            os.environ['CONDA_PREFIX'] = os.environ.get('CONDA_DEFAULT_ENV', '')

        runpy.run_module(module_name, run_name="__main__")
        time.sleep(1)
        window.Reappear()

    # window.close()

    if event == "Quit":
        window.close()
        sys.exit()

if __name__ == "__main__":

    wizard()