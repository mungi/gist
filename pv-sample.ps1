# $ErrorActionPreference = "Stop"

Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope LocalMachine -Force
Set-TimeZone -Id "UTC"

iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex
choco feature enable -n allowEmptyChecksums

winrm quickconfig -force
# Enable-PSRemoting -Force
Start-Sleep -s 5
Set-Item -Force WSMan:\localhost\Service\AllowUnencrypted $True
Set-Item -Force WSMan:\localhost\Client\AllowUnencrypted $True
Set-Item -Force WSMan:\localhost\Service\Auth\Basic $True
Set-Item -Force WSMan:\localhost\Client\Auth\Basic $True

# Set-Item -Force WSMan:\localhost\Client\TrustedHosts -Value "172.16.10.1"

iwr https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1 -UseBasicParsing | iex

$file = $env:SystemRoot + "\Temp\" + (Get-Date).ToString("MM-dd-yy-hh-mm")
winrm get winrm/config > $file

Exit(0)
