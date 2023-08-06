import os, sys, hashlib, zipfile
from glob import glob as re

file = 'python_threeten'
prefix = file.replace('.zip','') + '_broken_up_'
hash_file = file + '.sums'
CHUNK_SIZE =  1_000_000  #1MB for testing #100_000_000 #100MB
hash_function = hashlib.sha1

def create_zip_file(source_file, zip_file_name):
    with zipfile.ZipFile(zip_file_name, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(source_file, source_file)

def build():
    hash()
    split()

def hash():
    hashing = hash_function()
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashing.update(chunk)
    with open(hash_file, 'a') as f:
        f.write(hashing.hexdigest() + '  ' + file + '\n')

def verify():
    print('Verifying the sums file')
    with open(hash, 'r') as f:
        if not hash_function(open(file, 'rb').read()).hexdigest() == f.readline().split()[0]:
            print("Hash doesn't match")
            return
    print("Hash matches")

def split():
    #https://www.tutorialspoint.com/How-to-spilt-a-binary-file-into-multiple-files-using-Python
    failure = False
    file_number = 1
    with open(file,'rb') as f:
        print("Starting to split")
        try:
            chunk = f.read(CHUNK_SIZE)
            while chunk:

                current_file = prefix + str(str(file_number).zfill(6))

                with open(current_file, "wb+") as chunk_file:
                    chunk_file.write(chunk)

                create_zip_file(current_file, current_file+".zip")
                os.remove(current_file)
                file_number += 1
                chunk = f.read(CHUNK_SIZE)
        except Exception as e:
            print(f"Exception :> {e}")
            failure = True

    if not failure:
        os.remove(file)

"""
with open('Output.bin', 'wb') as fp:
    fp.write(input1)
"""

def join():
    foils = re(prefix + "*.zip")
    foils.sort()
    #https://stackoverflow.com/questions/62050356/merge-two-binary-files-into-third-binary-file

    current_binary = None
    for foil in foils:
        raw_foil = foil.replace('.zip','')
        print(foil)
        print(raw_foil)

        with zipfile.ZipFile(foil,"r") as f:
            f.extractall(members = [raw_foil])

        if current_binary is None:
            current_binary = open(raw_foil, 'rb').read()
        else:
            current_binary += open(raw_foil, 'rb').read()

        [os.remove(x) for x in [foil, raw_foil]]


    with open(file, 'wb') as fp:
        fp.write(current_binary)