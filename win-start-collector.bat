@echo off

SETLOCAL

SET SERVER_PATH=%cd%\server

@START /B CMD /C python %SERVER_PATH%\collector_daemon.py
ECHO COLLECTOR started.

::@START /B CMD /C python %SERVER_PATH%\text_extractor.py
::ECHO TEXT EXTRACTOR started.

@START /B CMD /C python %SERVER_PATH%\monitor.py
ECHO MONITOR started.

ENDLOCAL
