@echo off

SETLOCAL

SET PROJECT_PATH=%cd%
SET CLIENT_PATH=%PROJECT_PATH%\client
SET SERVER_PATH=%PROJECT_PATH%\server

CD %CLIENT_PATH%
@START npm install

SETX python38 "%LOCALAPPDATA%\Programs\Python\Python38" -m
SETX PATH "%python38%;%PATH%" -m

SETX python38_scripts "%LOCALAPPDATA%\Programs\Python\Python38\Scripts" -m
SETX PATH "%python38_scripts%;%PATH%" -m

pip install -r %SERVER_PATH%\requirements.txt

ENDLOCAL



