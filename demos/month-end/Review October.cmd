@echo off
setlocal
pushd "%~dp0"
echo Choose the project-cost export:
echo 1. Week ending 24 October
echo 2. Month ending 31 October
choice /c 12 /n
if errorlevel 2 (
  python pack.py --export project-costs.json
) else (
  python pack.py --export stale-project-costs.json
)
pause
popd
