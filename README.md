# es6mv
CLI tool for cleanly moving es6 javascript files

### What does it do?
* Edits module imports in all affected files so that they refer to the new location
* Follows the same behavior as `mv` for moving files (mainly arguments)

### How to use
* Set environment variable `ES6MV_INSPECT_DIR` to the project directory to listen to  
  example... `export ES6MV_INSPECT_DIR='/home/user/es6project/'`
* Run command `python es6mv.py {YOUR_SOURCE_FILE} {YOUR_DESTINATION_FILE}`
* (Optional) Set an alias `alias es6mv='python es6mv.py'`  
  Run command `es6mv.py {YOUR_SOURCE_FILE} {YOUR_DESTINATION_FILE}`

#### Misc
* Tested on Linux and Mac OS
* Untested on Windows
