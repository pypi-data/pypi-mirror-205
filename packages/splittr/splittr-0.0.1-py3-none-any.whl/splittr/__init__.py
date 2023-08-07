import os, sys, hashlib, zipfile, jsons, shutil
from glob import glob as re

def build():
    hash()
    split()

def hash(foil, hash_function = hashlib.sha1):
    hashing = hash_function()
    with open(foil, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashing.update(chunk)
    with open(foil + '.sums', 'a') as f:
        json.dumps(
            str({
                "hash":hashing.hexdigest()
            }),
            f
        )

def verify(foil, hash_function = hashlib.sha1):
    verified, set_hash = False, 0

    with open(foil + '.sums', 'r') as f:
        set_hash = json.loads(f)['hash']

    with open(hash, 'r') as f:
        verified = hash_function(open(foil, 'rb').read()).hexdigest() == set_hash:

    if verified:
        os.remove(foil + '.sums')

    return verified

def split(foil, CHUNK_SIZE = 100_000_000): #100MB
    #https://www.tutorialspoint.com/How-to-spilt-a-binary-file-into-multiple-files-using-Python
    failure = False
    file_number = 1
    with open(foil,'rb') as f:
        try:
            chunk = f.read(CHUNK_SIZE)
            while chunk:

                current_file = foil.replace('.zip','') + '_broken_up_' + str(str(file_number).zfill(10))

                with open(current_file, "wb+") as chunk_file:
                    chunk_file.write(chunk)

                with zipfile.ZipFile(current_file+".zip", 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
                    zip_file.write(current_file, current_file)

                os.remove(current_file)
                file_number += 1
                chunk = f.read(CHUNK_SIZE)
        except Exception as e:
            print(f"Exception :> {e}")
            failure = True

    if not failure:
        os.remove(foil)

def join(foil):
    mini_foils,current_binary = re(prefix + "*.zip"),None
    mini_foils.sort()
    #https://stackoverflow.com/questions/62050356/merge-two-binary-files-into-third-binary-file

    for mini_foil in mini_foils:
        raw_foil = mini_foil.replace('.zip','')

        with zipfile.ZipFile(mini_foil,"r") as f:
            f.extractall(members = [raw_foil])

        if current_binary is None:
            current_binary = open(raw_foil, 'rb').read()
        else:
            current_binary += open(raw_foil, 'rb').read()

        [os.remove(x) for x in [mini_foil, raw_foil]]

    with open(foil, 'wb') as fp:
        fp.write(current_binary)

def arguments():
    import argparse
	parser = argparse.ArgumentParser(description=f"Enabling the capability to stretch a single large file into many smaller files")

	parser.add_argument("-f","--file", help="The name of the file", nargs='*')
	parser.add_argument("--split", help="Split the file up", action="store_true",default=False)
	parser.add_argument("--join", help="Recreate the file", action="store_true",default=False)
	parser.add_argument("--template", help="Create a copy of this file specific to a large file", action="store_true",default=False)

	return parser.parse_args()

def main(foil:str,splitfile:bool=False, joinfile:bool=False):
    if splitfile:
        hash(foil)
        split(foil)
    elif joinfile:
        join(foil)
        verify(foil)

if __name__ == '__main__':
    argz = arguments()
    workingfoil = args.file[0]

    if args.template:
        contents = []
        with open(__file__, "r") as reader:
            contents = reader.readlines()

        with open(foil + ".py", "w+") as writer:
            for line in contents:
                line = line.rstrip()
                if "workingfoil = args.file[0]" in line:
                    line = line.replace("args.file[0]", "\""+foil+"\"")
        
        print(foil + ".py")
    else:
        if args.split and args.join:
            print("Cannot use both both split and join")
            return
        elif not os.path.exists(args.file[0])
            print("The file {file} does not exist".format(file=args.file[0]))
            return

        main(
            workingfoil,
            splitfile=args.split,
            joinfile=args.join,
        )