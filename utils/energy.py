"""VASP OUTCARからエネルギーを抽出"""

#!/usr/bin/python
# coding: UTF-8

# 使い方
# python ene.py OUTCARのPATH

import sys

args = sys.argv
# args[1]:  第一引数

class Energy():
    def __init__(self, content):
        self.content = content

    def print(self):
        print(self.content)



if __name__ == '__main__':
    with open(args[1], 'r') as f:
        outcar = f.read()

    energy = Energy(outcar)
    energy.print()
