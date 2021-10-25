@echo off

SETLOCAL

SET PROJECT_PATH=%cd%
SET CLIENT_PATH=%PROJECT_PATH%\client
SET SERVER_PATH=%PROJECT_PATH%\server

CD %CLIENT_PATH%
@START npm install

SET PYTHON38=%LOCALAPPDATA%\Programs\Python\Python38
SET PYTHON38_SCRIPTS=%LOCALAPPDATA%\Programs\Python\Python38\Scripts

SETX PATH "%PYTHON38%;%PYTHON38_SCRIPTS%;%PATH%" /M

%PYTHON38_SCRIPTS%\pip install %SERVER_PATH%\JPype1-1.1.2-cp38-cp38-win_amd64.whl
%PYTHON38_SCRIPTS%\pip install -r %SERVER_PATH%\requirements.txt

ENDLOCAL



