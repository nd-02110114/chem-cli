#!/usr/bin/python
# coding: UTF-8

# 使い方
# $ cryw.py -p ouput_file

import sys
import re
import argparse

# 数字取得の正規表現
NUMBER_PATTERN = r'([+-]?[0-9]+\.?[0-9]*)'
# アルファベット取得の正規表現
ALPHABET_PATTERN = r'([a-zA-Z])'
# 小文字の正規表現
SMALL_ALPHABET_PATTERN = r'([a-z])'
# 原子数の取得のための正規表現
ATOM_PATTERN = r'number of atoms/cell'
# 原子座標取得のための正規表現
COORDINATE_PATTERN = r'ATOMIC_POSITIONS'
# 並進ベクトルのための正規表現
ALAT_TV_PATTERN = r'lattice parameter'
TV_COORDINATE_PATTERN = r'crystal axes'

# bohr to angの変換用の定数
BOHR_TO_ANG = 0.529177

# gjf template
GJF_TEMPLATE = """
%nproc=
%mem=4000MB
#p 

this line for comments

0 1
"""
#outout用の定数
NEXTLINE_PREFIX = '\n'
TWO_SPACE = '  '
THREE_SPACE = '   '

class Parcer(object):
    def __init__(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()

        self.path = path
        self.content = lines

class EspressoParcer(Parcer):
    def __init__(self, path):
        super(EspressoParcer, self).__init__(path)
        self.atom_number = 0
        self.alat = 0
        self.structure_info = []
        self.tv_vector = []
        self.coordinate_type = ''

    def get_atom_number(self):
        tmp_content = self.content
        for line in tmp_content:
            # 行の前後のspaceの削除
            line = line.strip()
            if re.match(ATOM_PATTERN, line):
                if re.findall(NUMBER_PATTERN, line):
                    self.atom_number = int(re.findall(NUMBER_PATTERN, line)[0])
                    break
                else:
                    print >> sys.stderr.write('atom number cannot be found...')
                    return

        if self.atom_number != 0:
            return self
        else:
            print >> sys.stderr.write('atom number cannot be found...')
            return


    def get_alat(self):
        tmp_content = self.content
        for line in tmp_content:
            line = line.strip()
            # alatの取得
            if re.match(ALAT_TV_PATTERN, line):
                if re.findall(NUMBER_PATTERN, line):
                    self.alat = float(re.findall(NUMBER_PATTERN, line)[0]) * BOHR_TO_ANG
                    break
                else:
                    print >> sys.stderr.write('Tv vector info cannot be found...')
                    return

        if self.alat != 0:
            return self
        else:
            print >> sys.stderr.write('Tv vector info cannot be found...')
            return


    def get_tv_coordinate(self):
        tmp_content = self.content
        count = 0
        text_data = []
        for line in tmp_content:
            line = line.strip()
            if re.match(TV_COORDINATE_PATTERN, line):
                text_data = tmp_content[(count+1):(count+4)]

            count += 1

        num_data = []
        for data in text_data:
            num = re.findall(NUMBER_PATTERN, data)
            num_data.append([float(i) * self.alat for i in num[1:]])

        self.tv_vector = num_data
        return self

    def __get_structure_text_info(self):
        tmp_content = self.content

        count = 0
        text_data = []
        for line in tmp_content:
            line = line.strip()
            if re.match(COORDINATE_PATTERN, line):
                length = len(tmp_content)
                self.coordinate_type = ''.join(re.findall(SMALL_ALPHABET_PATTERN, line))
                if (length > (count+self.atom_number+1)):
                    text_data.append(tmp_content[(count + 1):(count + self.atom_number + 1)])

            count += 1

        return text_data

    def __get_structure_numerical_info(self, text_data):
        numerical_data = []
        for line in text_data:
            atom = ''.join(re.findall(ALPHABET_PATTERN, line))
            coordinate = re.findall(NUMBER_PATTERN, line)
            if (len(coordinate) > 3):
                # fix or relaxの情報を省く
                coordinate = coordinate[:3]

            num_coordinate = [float(str_num) if self.coordinate_type == 'angstrom' else float(str_num) * BOHR_TO_ANG for str_num in coordinate]
            numerical_data.append([atom] + num_coordinate)

        return numerical_data

    def get_structure_info(self):
        text_data = self.__get_structure_text_info()

        # 例外処理
        if (len(text_data) == 0):
            print >> sys.stderr.write('structure data cannot be found...')

        num_data = []
        for data in text_data:
            num_data.append(self.__get_structure_numerical_info(data))

        self.structure_info = num_data
        return self

    def __add_space(self, data):
        if type(data) == str:
            if (len(data) == 2):
                return data + TWO_SPACE
            else:
                return data + THREE_SPACE

        if type(data) == float:
            text = "{0:.9f}".format(data)
            if (len(text) == 11):
                return THREE_SPACE + text
            elif(len(text) == 12):
                return TWO_SPACE + text
        
        print >> sys.stderr.write('Invalid coordinate data...')

    def latestStructureGjf(self, output_path):
        tmp_data = self.structure_info
        output_text = GJF_TEMPLATE
        for data in tmp_data[-1]:
            line_text = ''
            for i in data:
                line_text += self.__add_space(i)

            line_text += NEXTLINE_PREFIX
            output_text += line_text

        tmp_tv_data = self.tv_vector
        for tv_data in tmp_tv_data:
            line_text = self.__add_space('Tv')
            for i in tv_data:
                line_text += self.__add_space(i)

            line_text += NEXTLINE_PREFIX
            output_text += line_text

        #最後の改行
        output_text += NEXTLINE_PREFIX

        with open(output_path, 'w') as f:
            f.write(output_text)

        return output_text
  

def main():
    parser = argparse.ArgumentParser(
        prog='cryw.py',
        description='structure watcher for scf calculation by quantum espresso',
    )
    parser.add_argument('-p','--inpath', type=str, help='espresso output file', required=True)
    parser.add_argument("-o", '--outpath', type=str, help="output path (optional, default: current directory)", default="")
    parser.add_argument('-n','--name', type=str, help='gjf file name', required=True)

    # variable
    args = parser.parse_args()
    path = args.inpath
    name = args.name + ".gjf"
    outpath = args.outpath
    output_path = name if outpath == "" else outpath.rstrip("/") + '/' + name

    parcer = EspressoParcer(path)
    parcer.get_alat()
    parcer.get_atom_number()
    parcer.get_tv_coordinate()
    parcer.get_structure_info()
    parcer.latestStructureGjf(output_path)

if __name__ == '__main__':
    main()