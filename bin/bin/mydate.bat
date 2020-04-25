@echo off
rem For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
rem For /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
rem For /f "tokens=1-2 delims=/:" %%a in ("%TIME%") do (set mytime=%%a%%b)
rem echo %mydate%_%mytime%
rem WMIC Path Win32_LocalTime Get Year,Month,Day,Hour,Minute,Second /Format:table
for /f %%a in ('wmic os get LocalDateTime ^| findstr ^[0-9]') do (set ts=%%a) & set datetime=%ts:~0,8%-%ts:~8,4%
echo %datetime%
rem for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j 
rem		set ldt=%ldt:~0,4%-%ldt:~4,2%-%ldt:~6,2% %ldt:~8,2%:%ldt:~10,2%:%ldt:~12,6%
rem echo Local date is [%ldt%]