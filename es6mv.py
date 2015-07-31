import os
import shutil
import sys

#GLOBALS
INSPECT_DIR = "/home/reggi/play/components2/"

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

def appendDotSlash(fp):
    if (not (fp.startswith('./') or fp.startswith('../'))):
        return "./" + fp
    else:
        return fp

def generateNewImportStatement(line, dest_dir):
    parsed = line.split("'")
    filepath = parsed[1]
    cwd = os.getcwd()
    os.chdir(src_dir)
    newfilepath = os.path.relpath(os.path.realpath(filepath), os.path.dirname(dest_dir))
    os.chdir(cwd)

    newfilepath = appendDotSlash(newfilepath)

    parsed[1] = "'" + newfilepath + "'"
    return "".join(parsed)

def dumbGenerateImportStatement(line, fp):
    parsed = line.split("'")
    parsed[1] = "'" + fp + "'"
    return "".join(parsed)

output_file = open(output_filename, 'w')
for line in f:
    if (not isRelativeImport(line)):
        output_file.write(line)
        continue
    
    newImportStatement = generateNewImportStatement(line, dest_realpath)
    output_file.write(newImportStatement)
output_file.close()

inspect_files = getInspectFiles()
for filepath in inspect_files:
    changes_made = False
    inspect_file = open(filepath, 'r')
    inspect_output_file = open(filepath + ".tmp", 'w') 

    for line in inspect_file:
        if(not isRelativeImport(line)):
            inspect_output_file.write(line)
            continue
        
        if (os.path.basename(extractImportFilepath(line)) == src_basename):
            newfilepath = os.path.relpath(output_filename, os.path.dirname(inspect_file.name))
            print(dest_realpath)
            print(os.path.dirname(inspect_file.name))
            print(newfilepath)
            newfilepath = os.path.splitext(newfilepath)[0]
            print(newfilepath)
            inspect_output_file.write(dumbGenerateImportStatement(line, newfilepath))
            print(filepath)
            print("Old: " + line.rstrip())
            print("New: " + dumbGenerateImportStatement(line, newfilepath).rstrip())
            changes_made = True

    inspect_output_file.close()
    if (changes_made):
        shutil.move(filepath + ".tmp", filepath)
    else:
        os.remove(filepath + ".tmp")

#delete original file
os.remove(src_realpath)
