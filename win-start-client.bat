@echo off
set PROJECT_PATH=%cd%
set CLIENT_PATH=%cd%\client
set PROXY_PATH=%cd%\client\proxy
set NODE_MODULES=%cd%\client\node_modules
set BIN_FOREVER=%cd%\client\node_modules\forever\bin

echo %NODE_MODULES%
echo %BIN_FOREVER%

set APP=client\proxy\app.js
echo %APP%

::cd %CLIENT_PATH% && npm install
@START /B CMD /C  node %BIN_FOREVER%\forever %APP% 
CD %CLIENT_PATH%
npm start
CD %POJECT_PATH%

::&& npm install && @START node %BIN_FOREVER%\forever %APP% 
::cd %CLIENT_PATH% && npm start && cd POJECT_PATH