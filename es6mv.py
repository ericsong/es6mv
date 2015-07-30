import sys

# check args
if len(sys.argv) != 2:
    print("Invalid # of args")
    exit()

src_filename = sys.argv[0]
dest_filename = sys.argv[1]

f = open(src_filename, 'r')

for line in f:
    print(line)
