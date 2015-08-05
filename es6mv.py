import os
import shutil
import sys

# GLOBALS
INSPECT_DIR = os.environ['ES6MV_INSPECT_DIR']

# helper functions
def extractFileFromFilepath(fp):
    return os.path.splitext(fp)[0]

def extractExtensionFromFilepath(fp):
    return os.path.splitext(fp)[1]

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

#rename to something better
def extractImportFromStatement(line):
    return line.split("'")[1]

def prefixDotSlash(fp):
    if (not (fp.startswith('./') or fp.startswith('../'))):
        return "./" + fp
    else:
        return fp

def getDir(filepath):
    if (os.path.isdir(filepath)):
        return filepath
    else:
        return os.path.dirname(filepath)

def realpathOfRelativeTargetFromSrc(src_realpath, target_relpath):
    save_cwd = os.getcwd()
    src_cwd = getDir(src_realpath)
    
    os.chdir(src_cwd)
    realpath = os.path.realpath(target_relpath)
    os.chdir(save_cwd)

    return realpath

def generateNewRelativePath(target_realpath, src_realdir):
    return os.path.relpath(target_realpath, src_realdir)

def generateNewImportStatement(line, dest_realdir):
    parsed = line.split("'")
    filepath = parsed[1]
    cwd = os.getcwd()
    os.chdir(src_realdir)
    newfilepath = os.path.relpath(os.path.realpath(filepath), dest_realdir)
    os.chdir(cwd)

    newfilepath = prefixDotSlash(newfilepath)

    parsed[1] = "'" + newfilepath + "'"
    return "".join(parsed)

def generateImportStatement(line, fp):
    ### add error handler
    parsed = line.split("'")
    fp = extractFileFromFilepath(fp)
    fp = prefixDotSlash(fp)
    parsed[1] = "'" + fp + "'"
    return "".join(parsed)

def getDirectoryOfFilepath(filepath):
    if (os.path.isdir(filepath)):
        return filepath
    else:
        return os.path.dirname(filepath)

# calculate realpaths, dirs, filenames, names
def moveFile(src_filepath, dest_filepath):
    src_realpath = os.path.realpath(src_filepath)
    dest_realpath = os.path.realpath(dest_filepath)

    src_filename = os.path.basename(src_realpath)
    dest_filename = os.path.basename(dest_realpath)

    src_realdir = getDirectoryOfFilepath(src_realpath)
    dest_realdir = getDirectoryOfFilepath(dest_realpath)

    output_filepath = os.path.join(dest_realdir, os.path.basename(src_realpath))

    src_name = os.path.splitext(src_filename)[0]
    dest_name = os.path.splitext(dest_filename)[0]
    #src_filepath, output_filepath, src_realpath, dest_realdir
    f = open(src_filepath, 'r')
    output_file = open(output_filepath, 'w')
    for line in f:
        if (not isRelativeImport(line)):
            output_file.write(line)
            continue

        target_relpath = line.split("'")[1]
        target_realpath = realpathOfRelativeTargetFromSrc(src_realpath, target_relpath)
        new_relpath = generateNewRelativePath(target_realpath, dest_realdir)
        newImportStatement = generateImportStatement(line, new_relpath)
        output_file.write(newImportStatement)
        print("Editing file: " + output_filepath)
        print("Old: " + line.rstrip())
        print("New: " + newImportStatement.rstrip())
        print("")
    output_file.close()

    #delete original file
    os.remove(src_filepath)

def inspectFileForChange(inspect_filepath, src_filepath, dest_filepath):
    src_realpath = os.path.realpath(src_filepath)
    dest_realpath = os.path.realpath(dest_filepath)

    src_filename = os.path.basename(src_realpath)
    dest_filename = os.path.basename(dest_realpath)

    src_realdir = getDirectoryOfFilepath(src_realpath)
    dest_realdir = getDirectoryOfFilepath(dest_realpath)

    output_filepath = os.path.join(dest_realdir, os.path.basename(src_realpath))

    src_name = os.path.splitext(src_filename)[0]
    dest_name = os.path.splitext(dest_filename)[0]

    changes_made = False
    inspect_file = open(inspect_filepath, 'r')
    inspect_output_file = open(inspect_filepath + ".tmp", 'w') 

    for line in inspect_file:
        if(not isRelativeImport(line)):
            inspect_output_file.write(line)
            continue

        save_cwd = os.getcwd()

        inspect_wd = getDir(inspect_filepath)
        os.chdir(inspect_wd)
        import_realpath = os.path.realpath(extractImportFromStatement(line))

        os.chdir(save_cwd)

        if (import_realpath[-3:] != ".js"):
            import_realpath = import_realpath + ".js"

        if (import_realpath == src_realpath):
            newfilepath = os.path.relpath(output_filepath, os.path.dirname(inspect_file.name))
            inspect_output_file.write(generateImportStatement(line, newfilepath))
            print("Editing file: " + inspect_filepath)
            print("Old: " + line.rstrip())
            print("New: " + generateImportStatement(line, newfilepath).rstrip())
            print("")
            changes_made = True
        else:
            inspect_output_file.write(line)

    inspect_output_file.close()
    if (changes_made):
        shutil.move(inspect_filepath + ".tmp", inspect_filepath)
    else:
        os.remove(inspect_filepath + ".tmp")

def moveAndInspectForChanges(src_filepath, dest_filepath):
    if(os.path.isdir(src_filepath)):
        if(os.path.isdir(dest_filepath)):
            #dest is dir, move src dir inside dest_filepath
            if (src_filepath[-1:] == '/'):
                src_filepath = src_filepath[:-1]
            if(dest_filepath[-1:] == '/'):
                dest_filepath = dest_filepath[:-1]

            dirname = os.path.basename(src_filepath)
            newdirname = os.path.join(dest_filepath, dirname)

            print("Making directory at: " + newdirname)

            os.mkdir(newdirname)
            
            for file in os.listdir(src_filepath):
                src_file = os.path.join(src_filepath, file)
                moveAndInspectForChanges(src_file, newdirname)

            shutil.rmtree(src_filepath)
        elif(os.path.isfile(dest_filepath)):
            #dest is regular file, error out
            print('ERROR: dest is a regular file')
            exit(1)
        elif(not os.path.exists(dest_filepath)):
            #dest DNE, create dir at dest_filepath
            os.mkdir(dest_filepath)
            for file in os.listdir(src_filepath):
                src_file = os.path.join(src_filepath, file)
                moveAndInspectForChanges(src_file, dest_filepath)
            shutil.rmtree(src_filepath)
        else:
            #some weird case like symbolic links, error out
            print('ERROR: unhandled file error')
            exit(1)
    else:
        moveFile(src_filepath, dest_filepath)

    inspect_files = getInspectFiles()
    for filepath in inspect_files:
        inspectFileForChange(filepath, src_filepath, dest_filepath)

# check args
if len(sys.argv) != 3:
    print("Invalid # of args")
    exit()

src_filepath = sys.argv[1]
dest_filepath = sys.argv[2]

moveAndInspectForChanges(src_filepath, dest_filepath)
