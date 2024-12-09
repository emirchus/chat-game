#!/bin/bash

SITE_PACKAGES=$(python -c "import site; print(site.getsitepackages()[0])")

SELENIUM_JS="--add-data ${SITE_PACKAGES}/selenium_stealth/js:selenium_stealth/js"
SELENIUM_DATA="--add-data ${SITE_PACKAGES}/selenium_stealth/js/utils.js:selenium_stealth/js"
IMPORTS="--hidden-import=undetected_chromedriver --hidden-import=selenium"
DATA="--add-data src:src --add-data src/external:external --add-data src/engine:engine --add-data requirements.txt:."
ICON="--icon=assets/icon.ico"
NAME="--name=LosSaltosDeBana"

pyinstaller --onedir $IMPORTS $SELENIUM_DATA $SELENIUM_JS $DATA $ICON $NAME --paths src src/main.py "$@"
