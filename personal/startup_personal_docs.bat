@echo off

REM Open VSCode in the personal directory using WSL paths
code --folder-uri "vscode-remote://wsl+Ubuntu/home/jl43/Documents/personal"

REM Open Google Chrome to the local docs site
start chrome http://127.0.0.1:8000"

exit
