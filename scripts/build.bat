@echo off
for /f "delims=" %%i in ('python -c "import site; print(site.getsitepackages()[0])"') do set SITE_PACKAGES=%%i

set SELENIUM_JS=--add-data "%SITE_PACKAGES%\selenium_stealth\js;selenium_stealth/js"
set SELENIUM_DATA=--add-data "%SITE_PACKAGES%\selenium_stealth\js\utils.js;selenium_stealth\js"
set IMPORTS=--hidden-import=undetected_chromedriver --hidden-import=selenium
set DATA=--add-data "src;src" --add-data "src/external;external" --add-data "src/engine;engine" --add-data "requirements.txt;."
set ICON=--icon=assets/icon.ico
set NAME=--name=LosSaltosDeBana

pyinstaller --onedir %IMPORTS% %SELENIUM_DATA% %SELENIUM_JS% %DATA% %ICON% %NAME% --paths src src/main.py %*
