"""Full width chars to half width chars"""

__author__ = "Daniel (danielw10001@gmail.com)"

import argparse
import re
import os
import os.path
import stat
import random
import string

ARGS = argparse.Namespace()
FULL_WIDTH_CAHRS = ('ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'
                    'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
                    '１２３４５６７８９０｀”’“‘＿－～＝＋＼｜／'
                    '（）［］【】｛｝＜＞《》．，、；：！＾％＃＠＄＆？＊。　'
                   )
HALF_WIDTH_CHARS = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                    '1234567890`"\'"\'_-~=+\|/()[][]{}<>"".,,;:!^%#@$&?*. '
                   )

parser = argparse.ArgumentParser(description=
                                 "Full width chars to half width chars "
                                 "recursively")
parser.add_argument('target', help="Target dir")
parser.add_argument('--no-hidden', action='store_true', help=
                    "No hidden dirs or files")
parser.parse_args(namespace=ARGS)

def is_hidden(path: str) -> bool:
    name = os.path.split(path)[1]
    return re.search(r'^[._]', name) or \
            os.stat(path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN

def trans(origin: str) -> str:
    origin = re.sub(r'｀([^｀\n]*)｀', r'`\1`', origin)
    origin = re.sub(r'”(?=\w)', '" ', origin)
    origin = re.sub(r'(?<=\w)“', ' "', origin)
    origin = re.sub(r'》(?=\w)', '" ', origin)
    origin = re.sub(r'(?<=\w)《', ' "', origin)
    origin = re.sub(r'’(?=\w)', '\' ', origin)
    origin = re.sub(r'(?<=\w)‘', ' \'', origin)
    origin = re.sub(r'(?<=\w)（', ' (', origin)
    origin = re.sub(r'）(?=\w)', ') ', origin)
    origin = re.sub(r'(?<=\w)[［【]', ' [', origin)
    origin = re.sub(r'[］】](?=\w)', '] ', origin)
    origin = re.sub(r'(?<=\w)｛', ' {', origin)
    origin = re.sub(r'｝(?=\w)', '} ', origin)
    origin = re.sub(r'，(?=\w)', ', ', origin)
    origin = re.sub(r'、(?=\w)', ', ', origin)
    origin = re.sub(r'；(?=\w)', '; ', origin)
    origin = re.sub(r'：(?=\w)', ': ', origin)
    origin = re.sub(r'！(?=\w)', '! ', origin)
    origin = re.sub(r'？(?=\w)', '? ', origin)
    origin = re.sub(r'[．。](?=\w)', '. ', origin)
    return origin.translate(
        str.maketrans(FULL_WIDTH_CAHRS, HALF_WIDTH_CHARS))

for root, subdirs, filenames in os.walk(ARGS.target):
    for subdir in subdirs:
        subdirpath = os.path.join(root, subdir)
        if ARGS.no_hidden and is_hidden(subdirpath):
            subdirs.remove(subdir)
    for filename in filenames:
        filepath = os.path.join(root, filename)
        if (not ARGS.no_hidden or not is_hidden(filepath)) and \
           re.search(r'\.(?:txt|md)$', filename):
            with open(filepath, encoding='utf-8') as file:
                tempfile_name = ''.join(random.choices(
                    string.ascii_letters + string.digits, k=32))
                tempfile_path = os.path.join(root, tempfile_name)
                with open(tempfile_path, mode='w', encoding='utf-8') as \
                        tfile:
                    tfile.write(trans(file.read()))
            os.replace(tempfile_path, filepath)

