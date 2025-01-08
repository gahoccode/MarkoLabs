' Run the batch file in headless mode
Set WshShell = CreateObject("WScript.Shell")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
' Run the batch file with choice 1 (Run Dashboard) and hide the window
WshShell.Run "cmd /c echo 1 | " & strPath & "\manage.bat", 0, False
