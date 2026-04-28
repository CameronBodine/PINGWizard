
import sys, os
import time
import runpy
from pingwizard.version import __version__ as pwversion
from pingwizard.check_available_updates import check

from pingmapper.version import __version__ as pmversion

import FreeSimpleGUI as sg

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
            # Launch installer in a new window from base environment
            # The ping environment must be closed to allow updates to proceed
            print("\nStarting PINGMapper update...")
            print("A new window will open to run the installer from base.")
            print("The wizard will close to release environment locks.")
            
            import subprocess
            import tempfile
            
            conda_base = os.environ.get('CONDA_PREFIX', '').split('envs')[0].rstrip(os.sep)
            
            # Create a temporary batch file to run the installer in a new window
            with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False) as f:
                f.write(f'''@echo off
setlocal enabledelayedexpansion
cd /d {conda_base}
                   call {conda_base}\\condabin\\conda.bat activate base
if errorlevel 1 (
    echo Failed to activate base environment
    pause
    exit /b 1
)
python -m pinginstaller
pause
''')
                batch_file = f.name
            
            # Launch the batch file in a new window
            try:
                # Use 'start' command to open in a new console window
                subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', batch_file])
                print("Installer window launched successfully.")
                print("Closing PINGWizard in 2 seconds...")
                
                time.sleep(2)  # Brief delay to ensure window opens
                break  # Exit the wizard loop to close the application
            except Exception as e:
                print(f"Error launching installer: {e}")
                print(f"Attempted to run: {batch_file}")
                print("Please run 'python -m pinginstaller' manually from base environment.")
                try:
                    os.remove(batch_file)
                except:
                    pass
                continue

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