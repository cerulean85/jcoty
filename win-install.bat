@echo off

SETLOCAL

SET PROJECT_PATH=%cd%
SET CLIENT_PATH=%PROJECT_PATH%\client
SET SERVER_PATH=%PROJECT_PATH%\server

CD %CLIENT_PATH%
@START npm install

SETX PYTHON38 "%LOCALAPPDATA%\Programs\Python\Python38" /M
SETX PATH "%python38%;%PATH%" /M

SETX PYTHON38_SCRIPTS "%LOCALAPPDATA%\Programs\Python\Python38\Scripts" /M
SETX PATH "%python38_scripts%;%PATH%" /M

pip install -r %SERVER_PATH%\requirements.txt

ENDLOCAL



