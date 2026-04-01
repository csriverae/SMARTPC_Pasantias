#!/usr/bin/env python
"""Start FastAPI server."""
import os
import sys
import subprocess

# Change to the correct directory
os.chdir(r'c:\Users\Lenovo\Downloads\SMARTPC_Pasantias\CODIGO\fronte_plantilla\starter-kit\starter-kit')

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

# Start Uvicorn
subprocess.run([
    sys.executable, '-m', 'uvicorn',
    'app.main:app',
    '--host', '0.0.0.0',
    '--port', '8000',
    '--log-level', 'info'
])
