#!/usr/bin/python
# coding: UTF-8

# VASP POSCAR作成スクリプト
# 使い方
# python potcar.py　hogehoge.gjf
# 引数に渡したgjfのパスを元にposcarを生成

import sys

args = sys.argv

# gjfをインポートする
gjf_path = args[1]
gjf_file = open(gjf_path, 'r')
lines = gjf_file.readlines()
gjf_file.close()

# 必要な情報を抜き出す
element_nums = []
element_cartesian_data = []
translation_vector_cartesian_data = []

# gjfファイルは, ６行目からcartesianの座標が入る
start_num = 6
count = 0
element = ''
element_num = 0

for line in lines:
    line_data = line.split()

    # ７行目以降かつ配列データが4つのものを取り出す
    if (count >= start_num and len(line_data) == 4):
         # 原子カウントロジック
        if (line_data[0] != element):
            if (element_num != 0): 
                element_nums.append(element_num)
            
            element_num = 0
            element = line_data[0]

        element_num += 1

        if (line_data[0] == 'Tv'):
            del line_data[0]
            translation_vector_cartesian_data.append(line_data)
        else:
            del line_data[0]
            element_cartesian_data.append(line_data)

       
    count+=1

# デバック用
# print(len(element_cartesian_data))
# print(element_nums)
# print(translation_vector_cartesian_data)

# 以下、POSCAR作成スクリプト
space_prefix = '  '
relax = '  T T T'
new_line_prefix = '\n'

# 最初の１行めは空白+格子定数の倍率は1.0000
output = '\n1.0000'

# まず並進ベクトルの設定を加える
for datas in translation_vector_cartesian_data:
    output += new_line_prefix
    for data in datas:
        if (len(data) == 11):
            output += '  ' + str(data)
        if (len(data) == 10):
            output += '   ' + str(data)

# 次に原子数を追加
output += new_line_prefix + space_prefix
for data in element_nums:
    output += str(data) + ' '

# cartesian座標を使うことを宣言
content = '\nSelective dynamics\ncartesian'
output += content

# まず次に原子のcartesianの設定を加える
for datas in element_cartesian_data:
    output += new_line_prefix
    for data in datas:
        # 綺麗に並べるために文字数で分岐
        if (len(data) == 12):
            output += '  ' + str(data)
        if (len(data) == 11):
            output += '   ' + str(data)
        if (len(data) == 10):
            output += '     ' + str(data)

    output += relax

# 最後に書き込み
output_name = 'POSCAR'
with open(output_name, 'w') as f:
    f.write(output)