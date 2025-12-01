Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

' Get the folder where this script file is located
CurrentPath = FSO.GetParentFolderName(WScript.ScriptFullName)

' Set the shell's current directory to that folder
WshShell.CurrentDirectory = CurrentPath

' Run Streamlit hidden (The '0' at the end means hidden window)
WshShell.Run "python -m streamlit run app.py", 0, False