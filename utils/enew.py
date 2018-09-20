#!/usr/bin/python
# coding: UTF-8

# 使い方
# $ enew.py -flag -p 探したいディレクトリ
# vaspの時
# $ enew.py -v -p ~/test
# espressoの時
# $ enew.py -e -p ~/test

import os
import re
import argparse
# https://github.com/gregbanks/python-tabulate からtabulate.pyを同じ階層に持ってくる
from tabulate import *

class Parcer(object):
    def __init__(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()

        self.path = path
        self.content = lines

    def reverse_list(self, list_data):
        tmp_list = list_data
        return tmp_list[::-1]

class EspressoParcer(Parcer):
    def __init__(self, path):
        super(EspressoParcer, self).__init__(path)
        self.conv_flag = False
        self.energy = []
        self.scf_count = 0

    def getEnergyAndIteration(self):
        tmp_content = self.content

        # 後ろから処理する
        scf_count = 0
        for line in self.reverse_list(tmp_content):
            # 行の前後のspaceの削除
            line = line.strip()
            # 数値の正規表現
            pattern=r'([+-]?[0-9]+\.?[0-9]*)'
            if line.find("End of BFGS Geometry Optimization") != -1:
                self.conv_flag = True

            if re.match(r"total energy|!", line):
                self.energy.append(re.findall(pattern, line))

            if re.match("Self-consistent Calculation", line):
                scf_count += 1

            # 終了条件
            # if (self.conv_flag and len(self.energy) > 0):
            #     break;

        self.scf_count = scf_count
        self.energy = self.energy[0] if len(self.energy) > 0 else ['']

    def getData(self):
        home = os.environ['HOME']
        tmp_path = self.path
        conv = "ok" if self.conv_flag else "not ok"
        if re.search('espresso.out', tmp_path):
            path = tmp_path.lstrip(home).rstrip('/espresso.out')

        if re.search('espresso.opt.out', tmp_path):
            path = tmp_path.lstrip(home).rstrip('/espresso.opt.out')

        return [path] + [conv] + [self.scf_count] + self.energy

class OutcarParcer(Parcer):
    def __init__(self, path):
        super(OutcarParcer, self).__init__(path)
        self.iteration= []
        self.energy = []

    def getEnergyAndIteration(self):
        tmp_content = self.content

        # 後ろから処理する
        for line in self.reverse_list(tmp_content):
            # 数値の正規表現
            pattern=r'([+-]?[0-9]+\.?[0-9]*)'
            if line.find("Iteration") != -1:
                tmp_iteration = re.findall(pattern, line)
                iteration = tmp_iteration[0] + '(' + tmp_iteration[1] + ')'
                self.iteration.append([iteration])

            if line.find("TOTEN") != -1:
                self.energy.append(re.findall(pattern, line))

            # 共に一件見つかったら終了
            if (len(self.iteration) > 0 and len(self.energy) > 0):
                break;

        # energyは2回取得されるので重複を除く
        self.iteration = self.iteration[0]
        self.energy = list(set(self.energy[0]))

    def getData(self):
        home = os.environ['HOME']
        tmp_path = self.path
        path = tmp_path.lstrip(home).rstrip('/OUTCAR')
        return [path] + self.iteration + self.energy


def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)

def main():
    parser = argparse.ArgumentParser(
        prog='enew.py',
        description='simple energy watcher tool',
    )
    parser.add_argument("-v", help="watch OUTCAR (For VASP)", action="store_true")
    parser.add_argument("-e", help="watch espresso.out (For Quantum Espresso)", action="store_true")
    parser.add_argument('-p','--path', type=str, help='path which you want to find', required=True)

    # variable
    args = parser.parse_args()

    if args.v:
        headers=["directory", "Iteration", "Energy (unit: eV)"]

        table = []
        for file in find_all_files(args.path):
            parttern = 'OUTCAR' + '$'
            m = re.search(parttern, file)
            if m:
                out_parcer = OutcarParcer(file)
                out_parcer.getEnergyAndIteration()
                table.append(out_parcer.getData())

        print tabulate(table, headers, tablefmt="rst", numalign='center', floatfmt=".8f")
        
    if args.e:
        headers=["directory", "Convegence", "SCF count","Energy (unit: Ry)"]

        table = []
        for file in find_all_files(args.path):
            # 変更した方が良いかも
            parttern = 'espresso.out|espresso.opt.out' + '$'
            m = re.search(parttern, file)
            if m:
                qe_parcer = EspressoParcer(file)
                qe_parcer.getEnergyAndIteration()
                table.append(qe_parcer.getData())

        print tabulate(table, headers, tablefmt="rst", numalign='center', floatfmt=".10f")

if __name__ == '__main__':
    main()