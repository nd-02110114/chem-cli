#!/usr/bin/python
# coding: UTF-8

# 使い方
# python potcar.py　hogehoge.gjf
# 引数に渡したgjfのパスを元にposcarを生成

import sys
import argparse

class GaussianParcer():
    def __init__(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()

        self.path = path
        self.content = lines
        self.element_nums = []
        self.element_cartesian_data = []
        self.translation_vector_cartesian_data = []

    def getData(self):
        # gjfファイルは, ６行目からcartesianの座標が入る(重要)
        start_num = 6
        count = 0
        element = None
        element_num = 0

        for line in self.content:
            line_data = line.split()
        
            # ７行目以降かつ配列データが4つのものを取り出す
            if (count >= start_num and len(line_data) == 4):
                 # 原子カウントロジック
                if (line_data[0] != element):
                    if (element_num != 0):
                        self.element_nums.append(element_num)
        
                    element_num = 0
                    element = line_data[0]
        
                element_num += 1
        
                if (line_data[0] == 'Tv'):
                    del line_data[0]
                    self.translation_vector_cartesian_data.append(line_data)
                else:
                    del line_data[0]
                    self.element_cartesian_data.append(line_data)
        
        
            count+= 1

class PoscarCreator():
    def __init__(self, element_nums, translation_vector_cartesian, element_cartesian, fix_number):
        self.element_nums = element_nums
        self.translation_vector_cartesian = translation_vector_cartesian
        self.element_cartesian = element_cartesian
        self.fix_number = fix_number
        self.output = None

    def createPoscar(self):
        space_prefix = '  '
        relax = '  T T T'
        fix = '  F F F'
        new_line_prefix = '\n'
        
        # 最初の１行めは空白+格子定数の倍率は1.0000
        output = '\n1.0000'
        
        # まず並進ベクトルの設定を加える
        for datas in self.translation_vector_cartesian:
            output += new_line_prefix
            for data in datas:
                if (len(data) == 11):
                    output += '  ' + str(data)
                if (len(data) == 10):
                    output += '   ' + str(data)
        
        # 次に原子数を追加
        output += new_line_prefix + space_prefix
        for data in self.element_nums:
            output += str(data) + ' '
        
        # cartesian座標を使うことを宣言
        content = '\nSelective dynamics\ncartesian'
        output += content
        
        # まず次に原子のcartesianの設定を加える
        coordinate_line_count = 1
        for datas in self.element_cartesian:
            output += new_line_prefix
            for data in datas:
                # 綺麗に並べるために文字数で分岐
                if (len(data) == 12):
                    output += '  ' + str(data)
                if (len(data) == 11):
                    output += '   ' + str(data)
                if (len(data) == 10):
                    output += '     ' + str(data)

            output += fix if coordinate_line_count <= self.fix_number else relax
            coordinate_line_count += 1

        return output 

def main():
    parser = argparse.ArgumentParser(
        prog='poscar.py',
        description='convert tool from .gjf to POSCAR',
    )
    parser.add_argument("-f", type=int, help="fix number (optional, you can fix the atom)",  default=0)
    parser.add_argument("-o", type=str, help="output path (optional, default: current directory)", default="")
    parser.add_argument("-p", type=str, help="path for .gjf file", required=True)

    # 引数のimport
    args = parser.parse_args()
    fix_number = args.f
    output_path = args.o
    output_name = "POSCAR" if output_path == "" else output_path.rstrip("/") + "/POSCAR"
    gjf_path = args.p

    gus_parcer = GaussianParcer(gjf_path)
    gus_parcer.getData()

    pos_create = PoscarCreator(
        gus_parcer.element_nums,
        gus_parcer.translation_vector_cartesian_data,
        gus_parcer.element_cartesian_data,
        fix_number
    )
    output = pos_create.createPoscar()
    with open(output_name, 'w') as f:
        f.write(output)

if __name__ == '__main__':
    main()
