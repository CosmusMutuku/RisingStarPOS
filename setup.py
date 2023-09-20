import sys
from PyInstaller.__main__ import run

if __name__ == '__main__':
    # Specify the path to your Python script
    script = 'shopping.py'

    # Specify the additional options for PyInstaller
    options = [
        '--name=shopping',  # Specify the name of the output executable
        '--onefile',        # Create a single executable file
        '--noconsole',      # Run the executable without a console window
    ]

    # Run PyInstaller
    sys.argv = ['pyinstaller', *options, script]
    run()
