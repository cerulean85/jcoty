@echo off


SETLOCAL

:_loop
	FOR /F "tokens=2 delims= " %%p IN ('tasklist ^| findstr "python.exe"') DO (
		SET result=%%p
        goto _break
	)
    :_break
	IF NOT "%result%"=="" (
		TASKKILL /F /PID %result%
        ECHO Killed %result%
        SET result=
	) ELSE (
        goto _break
    )
	timeout 1
goto _loop
:_break

:_loop
	FOR /F "tokens=5 delims= " %%p IN ('netstat -ano ^| findstr "3000"') DO (
		SET result=%%p
        goto _break
	)
    :_break
	IF NOT "%result%"=="" (
		TASKKILL /F /PID %result%
        ECHO Killed %result%
        SET result=
	) ELSE (
        goto _break
    )
	timeout 1
goto _loop
:_break

:_loop
	FOR /F "tokens=5 delims= " %%p IN ('netstat -ano ^| findstr "3001"') DO (
		SET result=%%p
        goto _break
	)
    :_break
	IF NOT "%result%"=="" (
		TASKKILL /F /PID %result%
        ECHO Killed %result%
        SET result=
	) ELSE (
        goto _break
    )
	timeout 1
goto _loop
:_break

SET KAFKA_PATH=%cd%\kafka
@START /B CMD /C %KAFKA_PATH%\bin\windows\kafka-server-stop.bat
@START /B CMD /C %KAFKA_PATH%\bin\windows\zookeeper-server-stop.bat

ENDLOCAL

