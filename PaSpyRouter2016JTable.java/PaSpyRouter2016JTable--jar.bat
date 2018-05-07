@echo off
set ProjName=PaSpyRouter2016JTable
echo Begin ...
echo --------------------
md classes
md classes\res
javac -d classes %ProjName%.java
echo --------------------
echo Done.

if exist %ProjName%.manifest.txt del /f %ProjName%.manifest.txt

echo Manifest-Version: 1.0> %ProjName%.manifest.txt
echo Created-By: 1.4.2_12 (Sun Microsystems Inc.)>> %ProjName%.manifest.txt
echo Main-Class: %ProjName%>> %ProjName%.manifest.txt

echo Release ...
echo --------------------
md Release
cd classes
jar cvfm ..\Release\%ProjName%.jar ..\%ProjName%.manifest.txt %ProjName%.class res/
cd ..
del %ProjName%.manifest.txt
echo --------------------
echo Done.

pause
