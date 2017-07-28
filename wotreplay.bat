@ECHO off

if exist WorldOfTanks.exe (

REG DELETE "HKEY_CLASSES_ROOT\.wotreplay" /f
REG DELETE "HKEY_CLASSES_ROOT\wotreplay_auto_file" /f

REG DELETE "HKEY_CURRENT_USER\Software\Classes\.wotreplay" /f
REG DELETE "HKEY_CURRENT_USER\Software\Classes\wotreplay_auto_file" /f
REG DELETE "HKEY_CURRENT_USER\Software\Classes\Applications\WorldOfTanks.exe" /f

REG DELETE "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.wotreplay" /f
REG DELETE "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs\.wotreplay" /f

REG DELETE "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\.wotreplay" /f
REG DELETE "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\wotreplay_auto_file" /f


REG ADD "HKEY_CLASSES_ROOT\.wotreplay" /d "World of Tanks Battle Replay" /f
REG ADD "HKEY_CLASSES_ROOT\.wotreplay\DefaultIcon" /d "\"%CD%\WorldOfTanks.exe\",1" /f
REG ADD "HKEY_CLASSES_ROOT\.wotreplay\shell\open\command" /d "\"%CD%\WorldOfTanks.exe\" \"%%1\"" /f
REG ADD "HKEY_CLASSES_ROOT\Applications\WorldOfTanks.exe\DefaultIcon" /d "\"%CD%\WorldOfTanks.exe\",1" /f
REG ADD "HKEY_CLASSES_ROOT\Applications\WorldOfTanks.exe\shell\open\command" /d "\"%CD%\WorldOfTanks.exe\" \"%%1\"" /f


REG ADD "HKEY_CURRENT_USER\Software\Classes\.wotreplay" /d "World of Tanks Battle Replay" /f
REG ADD "HKEY_CURRENT_USER\Software\Classes\.wotreplay\DefaultIcon" /d "\"%CD%\WorldOfTanks.exe\",1" /f
REG ADD "HKEY_CURRENT_USER\Software\Classes\.wotreplay\shell\open\command" /d "\"%CD%\WorldOfTanks.exe\" \"%%1\"" /f
REG ADD "HKEY_CURRENT_USER\Software\Classes\Applications\WorldOfTanks.exe\DefaultIcon" /d "\"%CD%\WorldOfTanks.exe\",1" /f
REG ADD "HKEY_CURRENT_USER\Software\Classes\Applications\WorldOfTanks.exe\shell\open\command" /d "\"%CD%\WorldOfTanks.exe\" \"%%1\"" /f


REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.wotreplay\OpenWithList" /ve /f
REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.wotreplay\OpenWithList" /v "a" /d "WorldOfTanks.exe" /f
REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.wotreplay\OpenWithList" /v "MRUList" /d "a" /f

REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.wotreplay\OpenWithProgids" /ve /f
REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.wotreplay\OpenWithProgids" /v "World of Tanks Battle Replay" /t REG_NONE /f

@ECHO.
@ECHO Записи внесены в реестр. Перезагрузите компьтер.

) else  ( 
ECHO Запустите скрипт из папки с установленной игрой.
)

@pause