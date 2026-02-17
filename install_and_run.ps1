<#
install_and_run.ps1
Administrator olaraq işlədin. Skript aşağıdakıları edəcək:

İstifadə: PowerShell-i Administrator olaraq açın və:
Set-ExecutionPolicy Bypass -Scope Process -Force; .\install_and_run.ps1
#>

function Write-Log { param($m) Write-Host "[install] $m" }

Write-Log "Checking for python..."
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Log "Python not found. Trying to install via winget..."
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Log "winget found — installing Python 3... (may ask for confirmation)"
        winget install --id Python.Python.3 -e --silent | Out-Null
    } else {
        Write-Log "winget not found. Please install Python manually from https://www.python.org/downloads/ and re-run this script. Exiting."
        exit 1
    }
}

Write-Log "Enabling long paths support (requires admin)."
try {
    reg add HKLM\System\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f | Out-Null
} catch {
    Write-Log "Failed to set registry key for long paths: $_"
}

Write-Log "Creating virtualenv and installing requirements..."
$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $root

if (-not (Test-Path .\venv)) {
    Write-Log "Creating venv..."
    python -m venv venv
}

Write-Log "Using venv python to install pip and requirements..."
$pythonExe = Join-Path $PWD 'venv\Scripts\python.exe'
if (-not (Test-Path $pythonExe)) { $pythonExe = 'python' }

& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install -r requirements.txt

Write-Log "Ensure .env exists. If you need to edit token or admin ids, open .env before running the bot."
if (-not (Test-Path .\.env)) {
    Copy-Item .\.env.example .\.env -ErrorAction SilentlyContinue
}

Write-Log "Starting bot in background (windows process)."

Start-Process -FilePath $pythonExe -ArgumentList 'bot.py' -NoNewWindow -WindowStyle Hidden
Write-Log "Bot process started. Check console logs or Telegram for bot account message."
