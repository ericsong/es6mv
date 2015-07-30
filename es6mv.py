import sys

# check args
if len(sys.argv) != 2:
    print("Invalid # of args")
    exit()

src_filename = sys.argv[0]
dest_filename = sys.argv[1]

f = open(src_filename, 'r')
dest_file = open(dest_filename, 'w')

for line in f:
    dest_file.write(line)
    print(line)
