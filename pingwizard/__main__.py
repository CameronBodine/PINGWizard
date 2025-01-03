
import os, sys

# Add 'pingwizard' to the path, may not need after pypi package...
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.append(PACKAGE_DIR)

def main():

    # Launch the wizard
    from pingwizard.gui_wizard import wizard
    wizard()

if __name__ == "__main__":
    main()