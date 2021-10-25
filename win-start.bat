@echo off
CALL win-start-server.bat

TIMEOUT 10
CALL win-start-client.bat
