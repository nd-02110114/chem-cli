# VASP POTCAR作成スクリプト
# 使い方
# python potcar.py H Cu S N
# 引数に渡した原子の順番にpotcarが生成

import sys

args = sys.argv
# args[1]:  第一引数

# potcarファイルがあるVASPディレクトリをさす
# 環境によってかえる必要あり
potential_path = '/users/nd0211/utils/VASP/potPAW.54_PBE'

output = ''
output_name = 'POTCAR'
length = len(args)
for i in range(length):
    if (length == 1):
        print('引数が足りません')
        break

    if (i == 0):
        # 第一引数は関係ないので, スキップする
        continue
    
    # Pathの作成
    potcar_path = potential_path + '/{0}/POTCAR'.format(args[i])

    # ファイルの中身の読み込み
    potcar_file = open(potcar_path, "r")
    output += potcar_file.read()
    potcar_file.close()

    if (i == (length-1)):
        # POTCARの作成
        with open(output_name, 'w') as f:
            f.write(output)

