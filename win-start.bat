@echo off
CALL win-start-server.bat
CALL win-start-client.bat

::&& npm install && @START node %BIN_FOREVER%\forever %APP% 
::cd %CLIENT_PATH% && npm start && cd POJECT_PATH