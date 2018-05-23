$file = "C:\Test_" + (Get-Date).ToString("MM-dd-yy-hh-mm") + ".txt"
winrm get winrm/config > $file
