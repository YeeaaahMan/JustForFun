@echo off

if not exist paths.xml ( 
color fc
echo ��������� paths.xml. ������� remove_mods.bat � ����� � ��ன � ������� bat-䠩� ����୮. 
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
echo ��⮢�! ����䨪�樨 ��६�饭�:
echo - �� ����� ./mods/      �  ./mods/backup/%t_ver%-%b_date% 
echo - �� ����� ./res_mods/  �  ./res_mods/backup/%t_ver%-%b_date%
@pause && exit )

echo ��⮢�! ����䨪�樨 ��६�饭� � ����� ./res_mods/backup/%t_ver%-%b_date%
@pause