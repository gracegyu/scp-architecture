@echo off
REM Windows 용 래퍼. sec.py 를 python 으로 실행한다.
REM   sec check
REM   sec vulns vt-api-gateway
where python >nul 2>&1
if errorlevel 1 (
  echo Python 을 찾을 수 없다. https://www.python.org/downloads/ 에서 설치할 것.
  echo 설치 시 "Add python.exe to PATH" 를 반드시 체크할 것.
  exit /b 1
)
python "%~dp0sec.py" %*
