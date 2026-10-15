# Automated SSH Password Initializer for Hetzner Server
Add-Type -AssemblyName System.Windows.Forms
$wshell = New-Object -ComObject WScript.Shell

Write-Host "Opening SSH connection to Hetzner server 89.167.22.10..." -ForegroundColor Cyan

# Start an interactive SSH session in a new window
$process = Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "ssh -o StrictHostKeyChecking=no root@89.167.22.10" -PassThru
Start-Sleep -Seconds 3

# Bring to foreground and send initial temporary password
$wshell.AppActivate($process.Id)
Start-Sleep -Milliseconds 800
[System.Windows.Forms.SendKeys]::SendWait("RghWXRivRMLjWp3jCd9U{ENTER}")
Start-Sleep -Seconds 3

# If prompted for current password:
[System.Windows.Forms.SendKeys]::SendWait("RghWXRivRMLjWp3jCd9U{ENTER}")
Start-Sleep -Seconds 2

# Send new password
[System.Windows.Forms.SendKeys]::SendWait("@Wei2Shi4Lin2{ENTER}")
Start-Sleep -Seconds 2

# Retype new password
[System.Windows.Forms.SendKeys]::SendWait("@Wei2Shi4Lin2{ENTER}")
Start-Sleep -Seconds 2

# Check if logged in by sending a marker command
[System.Windows.Forms.SendKeys]::SendWait("echo 'INITIAL_LOGIN_SUCCESSFUL' > /root/initialized.txt; exit{ENTER}")
