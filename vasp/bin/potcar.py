#!/usr/bin/python
# coding: UTF-8

import sys
import argparse

parser = argparse.ArgumentParser(
    prog='potcar.py',
    description='POTCAR creater for VASP',
)
parser.add_argument("-a", nargs='*', help="atoms about which you want to create POTCAR (order is important)", required=True)
parser.add_argument("-o", type=str, help="output path (optional, default: current directory)", default="")
parser.add_argument("-p", type=str, help="pseudopotential directory path", required=True)

args = parser.parse_args()

potential_path = args.p
output_path = args.o
atoms = args.a
output_name = 'POTCAR' if output_path == "" else output_path.rstrip('/') + '/POTCAR'

output = ''
length = len(atoms)
if (length == 0):
    print('More than one atom is needed!!')

for i in range(length):
    potcar_path = potential_path + '/{0}/POTCAR'.format(atoms[i])
    # ファイルの中身の読み込み
    potcar_file = open(potcar_path, "r")
    output += potcar_file.read()
    potcar_file.close()

    if (i == (length-1)):
        # POTCARの作成
        with open(output_name, 'w') as f:
            f.write(output)
