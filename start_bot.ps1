# start_bot.ps1 - activates venv and runs bot.py
Set-Location -Path "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)"
if (Test-Path .\venv\Scripts\Activate.ps1) {
    . .\venv\Scripts\Activate.ps1
}
python bot.py
