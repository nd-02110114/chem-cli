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
        self.result = []

    def getEnergyAndIterationNumber(self):
        tmp_content = self.content
        for line in tmp_content:
            if line.find("Iteration") != -1:
                self.result.append(line.replace("-", ""))

            if line.find("TOTEN") != -1:
                self.result.append(line)

    def show(self):
        output = ""
        tmp_result = self.result
        for line in tmp_result:
            output += line

        print(output)



if __name__ == '__main__':
    with open(args[1], 'r') as f:
        lines = f.readlines()

    energy = Energy(lines)
    energy.getEnergyAndIterationNumber()
    energy.show()
