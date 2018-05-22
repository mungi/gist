#$ErrorActionPreference = "Stop"

Set-TimeZone -Id "UTC"
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope LocalMachine -Force

iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex
choco feature enable -n allowEmptyChecksums

winrm quickconfig -force
#Enable-PSRemoting -Force
Start-Sleep -s 15
#Set-Item -Force WSMan:\localhost\Client\TrustedHosts -Value "172.16.10.1"
Set-Item -Force WSMan:\localhost\Service\AllowUnencrypted $True
Set-Item -Force WSMan:\localhost\Client\AllowUnencrypted $True
Set-Item -Force WSMan:\localhost\Service\Auth\Basic $True
Set-Item -Force WSMan:\localhost\Client\Auth\Basic $True

$file = $env:SystemRoot + "\Temp\" + (Get-Date).ToString("MM-dd-yy-hh-mm")
winrm get winrm/config > $file
