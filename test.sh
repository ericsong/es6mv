#!/bin/bash

rm -r ./testfolder
cp -r ./backup_folder ./testfolder

export ES6_INSPECT_DIR="./testfolder/js/components/"
python es6mv.py ./testfolder/js/components/modules/Icon.js ./testfolder/js/components/
python es6mv.py ./testfolder/js/components/CourseLayout.js ./testfolder/js/components/CourseContent/
cd ./testfolder
npm test
