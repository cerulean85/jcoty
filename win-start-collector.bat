@echo off

SETLOCAL

SET SERVER_PATH=%cd%\server

@START /B CMD /C python %SERVER_PATH%\url_collector_daemon.py
ECHO URL COLLECTOR started.

@START /B CMD /C python %SERVER_PATH%\html_downloader.py
ECHO HTML DOWNLOADER started.

@START /B CMD /C python %SERVER_PATH%\text_extractor.py
ECHO TEXT EXTRACTOR started.

@START /B CMD /C python %SERVER_PATH%\monitor.py
ECHO MONITOR started.

ENDLOCAL
