"""
    -- coding: utf-8 --
    @Author: codeking
    @Data : 2022/5/2 14:10
    @File : GetCidDic.py
"""
# 获取cid对应的cas，将其存储为字典
def get_cid_dic(cid_list, cas_list):
    # 将cid数据 和 cas号对应起来
    cid_dic = {}
    if (len(cid_list) == len(cas_list)):
        for index in range(0, len(cas_list)):
            key = cid_list[index]
            value = cas_list[index]
            cid_dic.update({str(key): value})
        return cid_dic
    else:
        print('数据获取有误')

def Read_SDF(read_path):
    try:
        # 读取存储的sdf文件
        with open('{read_path}'.format(read_path=read_path), 'r', encoding='utf-8') as sdf_file:
            sdf_file = sdf_file.readlines()
            print('sdf文件读取成功')
            return sdf_file
    except Exception as e:
        print('sdf文件有问题，请检查一下，失败原因：', e)