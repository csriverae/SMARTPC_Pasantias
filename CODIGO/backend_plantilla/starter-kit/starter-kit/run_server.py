#!/usr/bin/env python3
import os
import sys
import subprocess

# Change to the correct directory
os.chdir(r'c:\Users\Lenovo\Downloads\SMARTPC_Pasantias\CODIGO\backend_plantilla\starter-kit\starter-kit')

# Add the current directory to the path
sys.path.insert(0, os.getcwd())

# Run uvicorn
subprocess.run([
    sys.executable, '-m', 'uvicorn',
    'app.main:app',
    '--reload',
    '--port', '8000',
    '--host', '127.0.0.1'
])
