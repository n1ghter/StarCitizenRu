#!/usr/bin/python

import os
import sys
import base64
import codecs
import hashlib
from functools import partial

def FileSize(filename):
    return os.stat(filename).st_size

def FileMD5(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.digest()

def AppendFile(indexFile, filename):
    print(f'Add file: {filename}')
    fileSize = FileSize(filename)
    fileHash = FileMD5(filename)
    fileBase64Hash = base64.b64encode(fileHash).decode()     
    indexFile.write(f'{filename}:{fileSize}:{fileBase64Hash}\r\n')

def AppendDirectory(indexFile, path):
    for root, subdirs, files in os.walk(path):
        for filename in files:
            AppendFile(indexFile, os.path.join(root, filename))

def main(args):
    print('Create files index...')
    try:
        with codecs.open('index.txt', 'w', 'utf-8') as indexFile:
            AppendDirectory(indexFile, 'data')
    except Exception as err:
        print(f'Create files index failed:\n{err}')
        return 1
    print("Done")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
