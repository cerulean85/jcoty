@echo off

SETLOCAL

SET KAFKA_PATH=%cd%\kafka
@START /B CMD /C %KAFKA_PATH%\bin\windows\zookeeper-server-start.bat %KAFKA_PATH%\config\zookeeper.properties

:_loop
	FOR /F "tokens=4 delims= " %%p IN ('netstat -ano ^| findstr "2181"') DO (
		SET result=%%p
	)
	IF "%result%"=="LISTENING" (
		ECHO Jupyter Started.
		@START /B CMD /C %KAFKA_PATH%\bin\windows\kafka-server-start.bat %KAFKA_PATH%\config\server.properties
		goto _break
	)
	timeout 3
goto _loop
:_break

:_loop
	FOR /F "tokens=4 delims= " %%p IN ('netstat -ano ^| findstr "9092"') DO (
		SET result=%%p
	)
	IF "%result%"=="LISTENING" (
		ECHO Kafka Started.
		goto _break
	)
	timeout 3
goto _loop
:_break

ENDLOCAL
