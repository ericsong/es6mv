#!/bin/bash

rm -r ./testfolder
cp -r ./backup_folder ./testfolder

export ES6_INSPECT_DIR="./testfolder/js/components/"
python es6mv.py ./testfolder/js/components/modules/Icon.js ./testfolder/js/components/
python es6mv.py ./testfolder/js/components/CourseLayout.js ./testfolder/js/components/CourseContent/
python es6mv.py ./testfolder/js/components/modules/ModalTrigger.js ./testfolder/js/components/modules/modals/
python es6mv.py ./testfolder/js/components/modules/Modal.js ./testfolder/js/components/modules/modals/Modal.js
python es6mv.py ./testfolder/js/components/modules/ModalConfirmation.js ./testfolder/js/components/modules/modals/ModalConfirmation.js
python es6mv.py ./testfolder/js/components/PresentMode ./testfolder/js/components/CourseContent
python es6mv.py ./testfolder/js/components/modules/forms ./testfolder/js/components/CourseContent/forms
cd ./testfolder
npm test
