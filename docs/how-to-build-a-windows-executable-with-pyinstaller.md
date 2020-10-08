# How to build a Windows Executable with Pyinstaller

## Create a virtualenv and install dependencies

Create a virtual environment with only the dependencies needed for installation. Please note that I've downgraded matplotlib in the `requirements.txt` to a version that works with pyinstaller.

In the `"Studer  Datalog  Viewer"` directory we create a virtualenv called `venv` and install the requirements into it:

    python -m venv 
    .\venv\Scripts\activate
    pip install -r requirements.txt
    pip install pyinstaller==4.0

## Build the executable

Run pyinstaller to build the executable

    pyinstaller tkinter_GUI_datalogviewer.spec 

A directory with the executable should now be available in the `dist` directory.
