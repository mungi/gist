$ErrorActionPreference = "Stop"

Set-TimeZone -Id "UTC"
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope LocalMachine -Force

iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex
choco feature enable -n allowEmptyChecksums

winrm quickconfig -force
winrm set winrm/config/service/auth @{Basic="true"}
winrm set winrm/config/service @{AllowUnencrypted="true"}
winrm set winrm/config/client/auth @{Basic="true"}
#winrm set winrm/config/client @{TrustedHosts = "172.16.10.1"}

$file = $env:SystemRoot + "\Temp\" + (Get-Date).ToString("MM-dd-yy-hh-mm")
winrm get winrm/config > $file
