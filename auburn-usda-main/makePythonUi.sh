#1/bin/bash

# This script generates python files based on ui files created from 
# Qt Designer, which can then be used in PySide6 Qt classes to define
# their UI. 

echo 'Generating python files from ui files'
for filename in resources/ui/*.ui; do
    file="${filename%.*}"
    echo "${filename##*/}"
    pyside6-uic "${filename}" -o "./package/ui_python/${file##*/}_ui.py"
done 