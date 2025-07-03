@echo off
set dbPath=%1

if %dbPath%=="" goto missingPath
if not %dbPath:~0,1%%dbPath:~-1%=="" goto missingQuote
if not exist %dbPath% goto notFound
if not "%dbPath:~-3,-1%"=="db" goto notDBPath
if "%dbPath:~0,1%"=="""" IF "%dbPath:~-1%"=="""" (
    :: Remove the first and last double quotes
    set "dbPath=%dbPath:~1,-1%"
)

set itemType=test123
set fileName="test"

sqlite3 %dbPath% ^
"INSERT INTO modelhistory(date_created,date_updated,item,file_name,label_file_name) ^
values ('2025-05-01 08:15:00','2025-05-01 08:15:00','%itemType%','%fileName%.h5','%fileName%.txt');"

IF errorlevel 1 goto end
echo "Success: Injected completed."
goto end 

:missingPath
echo Error: Missing db path argument.
goto end

:missingQuote
echo Error: Path does not contain quotation marks.
goto end

:notFound
echo Error: db Path does not exists.
goto end

:notDBPath
echo Error: Path provided is not db extension.
goto end

:end
exit /b 1