@echo off
:: Set file paths
set TESTFILE=steps\verify_ticket_steps.py
set FEATUREFILE=ticket_verification.feature
set LOGFILE=combined_test_and_error_log.txt
set TEMPFILE=output.txt

:: Navigate to the directory containing the feature files
cd /d D:\University-Master\Term-1\Adv Software Engineering\PR01\Code1\Online_Railway_Ticket_Booking_System-main\train-ticket\app\features

:: Run behave and save the output to a temporary file
behave %FEATUREFILE% > %TEMPFILE% 2>&1

:: Start writing to the combined log file
echo In my test: > %LOGFILE%
echo # Test code >> %LOGFILE%
type %TESTFILE% >> %LOGFILE%

:: Check if the output contains "0 failed"
findstr /r /c:"0 failed" %TEMPFILE% > nul
if %errorlevel% equ 0 (
    echo. >> %LOGFILE%
    echo Everything is OK. Test passed successfully. >> %LOGFILE%
    echo Everything is OK. Test passed successfully.
) else (
    echo. >> %LOGFILE%
    echo I have this error: >> %LOGFILE%
    echo # Error message >> %LOGFILE%
    type %TEMPFILE% >> %LOGFILE%
    echo Errors found. Combined log saved to %LOGFILE%.
)

:: Clean up the temporary output file
del %TEMPFILE%
