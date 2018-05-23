$file = "C:\Test_" + (Get-Date).ToString("MM-dd-yy-hh-mm")
winrm get winrm/config > $file
