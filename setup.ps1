Write-Host "Checking for Python..."

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not found in your PATH. Please install Python and add it to PATH."
    exit 1
}

Write-Host "Python found."

if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
} else {
    Write-Host "Virtual environment already exists."
}

Write-Host "Installing dependencies..."
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Setup complete!"
