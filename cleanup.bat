@echo off
echo Cleaning up project structure...
echo Removing duplicate files and directories

rem Remove unnecessary src directory and its contents
if exist src\bhis.db del /F src\bhis.db
if exist src rmdir /S /Q src

echo Cleanup complete 