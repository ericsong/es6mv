# es6mv
CLI util for moving es6 javascript files and renaming imports

### What does it do?

* Follows the same behavior as `mv` for moving files (mainly arguments)
* Edits module imports in the moved file so that the old and new import statements refer to the same location
* Listens on a project directory and updates all import statements that refer to moved file

### How to use
* Set environment variable `ES6MV_INSPECT_DIR` to the project directory to listen to  
  example... `export ES6MV_INSPECT_DIR='/home/user/es6project/'`
* Run command `python es6mv.py {YOUR_SOURCE_FILE} {YOUR_DESTINATION_FILE}`
* (Optional) Set an alias `alias es6mv='python es6mv.py'`  
  Run command `es6mv.py {YOUR_SOURCE_FILE} {YOUR_DESTINATION_FILE}`

#### Misc
* Tested on Linux and Mac OS
* Untested on Windows
