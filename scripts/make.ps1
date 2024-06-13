# Virtual environment creating
function Setup-Venv {
    $venvPath = "venv\Scripts\activate.ps1"
    if (-Not (Test-Path venv)) {
        python -m venv venv
    }
    return $venvPath
}

# Install app dependencies
function Install-Dependencies {
    $activate = Setup-Venv
    & $activate
    pip install -r requirements.txt
}

# Install dev dependencies
function Install-DevDependencies {
    $activate = Setup-Venv
    & $activate
    pip install -r requirements-dev.txt
}

# App running
function Run-App {
    $activate = Setup-Venv
    & $activate
    cd src
    python app.py
}

# Tests running
function Run-Tests {
    $activate = Setup-Venv
    & $activate
    pytest
}

# Help
function Show-Help {
    Write-Host "Available commands:"
    Write-Host "Install-Dependencies    - Setup virtual environment and install dependencies"
    Write-Host "Run-App                 - Run the application"
}

# Args handling
switch ($args[0]) {
    "install" {
        Install-Dependencies
    }
    "run" {
        Run-App
    }
    default {
        Show-Help
    }
}
