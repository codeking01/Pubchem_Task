"""
    -- coding: utf-8 --
    @Author: codeking
    @Data : 2022/5/3 12:20
    @File : GenerateNums.py
"""
# 这个用来生成序列数字，然后将其存入txt文件中
from tqdm import tqdm

def GenNums(txtpath,NumsList):
    # 把1到1000 写入txt文件
    # 根据传递的列表的值命名这个txt文件
    NumsList=NumsList.split(',')
    num_start=int(NumsList[0])
    num_end=int(NumsList[1])
    print('开始写入')
    # 先删除原来的文件再转化新的文件
    open(f'{txtpath}/nums.txt', 'w').close()
    for i in tqdm(range(num_start, num_end)):
        try:
            with open(f'{txtpath}/nums.txt', encoding='utf-8', mode='a') as file:
                file.write(str(i) + '\n')
            file.close()
        except Exception as e:
            print('文件生成失败，原因为：', e)
    print('结束写入')