#!/bin/sh

# pyrcc5 gui/icons.qrc > icons.py

for i in `ls -1 *.ui`; do
    file=`basename ${i} .ui`
    pyuic5 $i > ${file}Ui.py
done
