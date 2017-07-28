@echo off

if not exist paths.xml ( 
color fc
echo Отсутствует paths.xml. Поместите remove_mods.bat в папку с игрой и запустите bat-файл повторно. 
color
@pause && exit )

findstr "res_mods" paths.xml > mods.txt
set /p t_ver= < mods.txt
del /f /q mods.txt

set t_ver="%t_ver: =%"
set t_ver=%t_ver:<Path>res_mods/=%
set t_ver=%t_ver:<Path>./res_mods/=%
set t_ver=%t_ver:</Path>=%

set b_date=%date:~6,4%_%date:~3,2%_%date:~0,2%

if exist mods (
mkdir mods\backup\%t_ver%-%b_date%
xcopy mods\%t_ver% mods\backup\%t_ver%-%b_date% /E /K /Y
rmdir /s /q mods\%t_ver%
mkdir mods\%t_ver%
)

if exist res_mods (
mkdir res_mods\backup\%t_ver%-%b_date%
xcopy res_mods\%t_ver% res_mods\backup\%t_ver%-%b_date% /E /K /Y
rmdir /s /q res_mods\%t_ver%
mkdir res_mods\%t_ver%
)

cls
if exist mods (
echo Готово! Модификации перемещены:
echo - из папки ./mods/      в  ./mods/backup/%t_ver%-%b_date% 
echo - из папки ./res_mods/  в  ./res_mods/backup/%t_ver%-%b_date%
@pause && exit )

echo Готово! Модификации перемещены в папку ./res_mods/backup/%t_ver%-%b_date%
@pause