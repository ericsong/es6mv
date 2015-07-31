import os
import sys

#flags
WRITE_ENABLED = False
PRINT_ENABLED = False

# check args
if len(sys.argv) != 3:
    print("Invalid # of args")
    exit()

src_filename = sys.argv[1]
dest_filename = sys.argv[2]

f = open(src_filename, 'r')
dest_file = open(dest_filename, 'w')

dest_realpath = os.path.realpath(dest_filename)

def isRelativeImport(line):
    if (line.startswith('import ')):
        filepath = line.split("'")[1]
        if (filepath.startswith('./') or 
            filepath.startswith('../')):
                return True

    return False

def extractImportFilepath(line):
    return line.split("'")[1]

def generateNewImportStatement(line, dest_dir):
    parsed = line.split("'")
    filepath = parsed[1]
    newfilepath = os.path.relpath(filepath, dest_dir)
    parsed[1] = "'" + newfilepath + "'"
    return "".join(parsed)

for line in f:
    if (not isRelativeImport(line)):
        dest_file.write(line)
        continue
    
    newImportStatement = generateNewImportStatement(line, dest_realpath)
    dest_file.write(newImportStatement)
