## Prerequisites

- Python 3.10+ installed and added to your system PATH

## Setup Instructions

1. Open PowerShell in the project directory.

2. Run the setup script to create a virtual environment and install dependencies:

    ```powershell
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\setup.ps1
    ```

3. Activate the virtual environment:

    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

4. Now you can run your Python scripts within the virtual environment.