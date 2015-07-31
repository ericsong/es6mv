import os
import sys

#GLOBALS
INSPECT_DIR = "/home/reggi/c0dez/thm-dev/THM/frontend_v2/js/components/"

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

src_basename = os.path.splitext(os.path.basename(src_realpath))[0]

if (os.path.isdir(dest_realpath)):
    dest_dir = dest_realpath
    output_filename = os.path.join(dest_dir, os.path.basename(src_realpath))
else:
    dest_dir = os.path.dirname(dest_realpath)
    output_filename = dest_realpath

output_file = open(output_filename, 'w')

def getInspectFiles():
    inspect_files = []
    for path, subdirs, files in os.walk(INSPECT_DIR):
        for name in files:
            inspect_files.append(os.path.join(path, name))
    return inspect_files

def isRelativeImport(line):
    if (not line.startswith('import ')):
        return False

    splits = line.split("'")
    if(len(splits) < 2):
        return False
    
    filepath = splits[1]

    if (not(filepath.startswith('./') or filepath.startswith('../'))):
        return False

    return True

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

inspect_files = getInspectFiles()
for filepath in inspect_files:
    inspect_file = open(filepath, 'r')

    for line in inspect_file:
        if(not isRelativeImport(line)):
            continue

        if (os.path.basename(extractImportFilepath(line)) == src_basename):
            print(inspect_file.name)
            print(line)
