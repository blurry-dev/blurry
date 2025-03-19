import subprocess
import sys
import os

def test_uv_install():
    # Check if virtual environment exists, create if not
    venv_dir = ".venv"
    if not os.path.exists(venv_dir):
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])

    # Activate virtual environment
    if os.name == "nt":  # Windows
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
    else:  # POSIX (Linux, macOS)
        activate_script = os.path.join(venv_dir, "bin", "activate")

    # Construct the pip install command, ensuring it's executed within the venv
    pip_install_command = f"source {activate_script} && uv pip install ."
    
    # Execute the command using subprocess
    process = subprocess.Popen(pip_install_command, shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Check for errors during pip install
    assert process.returncode == 0, f"uv pip install failed with error:\n{stderr.decode()}"

    # Verify installation by attempting to import a key dependency
    try:
        import Jinja2
        assert Jinja2 is not None
    except ImportError:
        assert False, "Jinja2 import failed, indicating dependencies were not installed correctly."
