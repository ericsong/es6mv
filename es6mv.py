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

src_realpath = os.path.realpath(src_filename)
dest_realpath = os.path.realpath(dest_filename)

src_dir = os.path.dirname(src_realpath)

if (os.path.isdir(dest_realpath)):
    dest_dir = dest_realpath
    output_filename = os.path.join(dest_dir, os.path.basename(src_realpath))
else:
    dest_dir = os.path.dirname(dest_realpath)
    output_filename = dest_realpath

output_file = open(output_filename, 'w')

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
    cwd = os.getcwd()
    os.chdir(src_dir)
    newfilepath = os.path.relpath(os.path.realpath(filepath), os.path.dirname(dest_dir))
    os.chdir(cwd)

    if (not (newfilepath.startswith('./') or newfilepath.startswith('../'))):
        newfilepath = "./" + newfilepath

    parsed[1] = "'" + newfilepath + "'"
    return "".join(parsed)

for line in f:
    if (not isRelativeImport(line)):
        output_file.write(line)
        continue
    
    newImportStatement = generateNewImportStatement(line, dest_realpath)
    output_file.write(newImportStatement)
