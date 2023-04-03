"""
    -- coding: utf-8 --
    @Author: codeking
    @Data : 2022/5/2 14:21
    @File : ConvertSdfToMol.py
"""
import functools
import inspect
import time

from tqdm import tqdm

# 把数据写入为mol，并且以cas号命名
def save_mol(savefilepath, data, temp_list,saved_caslist,cas_list,current_index):
    try:
        # todo 判断一下存储的cas是否原来也存储过
        # 处理cas是列表的数据
        if (type(data) == list):
            for L_index in data:
                # 判断一下存储的cas是否原来也存储过
                if(L_index in saved_caslist):
                    same_index=0
                    # 判断出现过几次了
                    for L in  saved_caslist:
                        if(L_index == L):
                            same_index+=1
                    # 修改原来的名字为 100_10_1-1
                    cas_name=L_index+'-'+str(same_index)
                    file = open('{savefile}/{cas}.mol'.format(savefile=savefilepath, cas=cas_name), 'w', encoding='utf-8')
                    for i in temp_list:
                        file.write(i)
                    file.close()
                    saved_caslist.append(data)
                else:
                    file = open('{savefile}/{cas}.mol'.format(savefile=savefilepath, cas=L_index), 'w', encoding='utf-8')
                    for i in temp_list:
                        file.write(i)
                    file.close()
                    saved_caslist.append(L_index)
        # 单个数据
        else:
            # 判断一下存储的cas是否原来也存储过
            if(data in saved_caslist):
                same_index=0
                # 判断出现过几次了
                for L in  saved_caslist:
                    if(data == L):
                        same_index+=1
                # 修改原来的名字为 100_10_1-1
                cas_name=data+'-'+str(same_index)
                file = open('{savefile}/{cas}.mol'.format(savefile=savefilepath, cas=cas_name), 'w', encoding='utf-8')
                for i in temp_list:
                    file.write(i)
                file.close()
                saved_caslist.append(data)
            else:
                file = open('{savefile}/{cas}.mol'.format(savefile=savefilepath, cas=data), 'w', encoding='utf-8')
                for i in temp_list:
                    file.write(i)
                file.close()
                saved_caslist.append(data)
    except Exception as e:
        # 考虑将失败的数据存入日志文件中
        # with open('../log/{cas}.log'.format(cas='fail_sdf'), encoding='utf-8', mode='a') as file:
        #     # 将转化失败的存入日志中
        #     file.write(str(cas_list[current_index]))
        #     file.write('\n**失败原因：' + str(e) + '\n')
        #     file.close()
        print('\n****cas名称不合法，或者保存路径有误，请检查，失败原因{e}\n'.format(e=e))


# 判断cas是否为空
def IsNotEmpty(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        func_args = inspect.getcallargs(func,*args,**kwargs)
        sdf_cid=func_args.get('sdf_cid')
        cid_dic=func_args.get('cid_dic')
        current_index=func_args.get('current_index')
        if (str(sdf_cid) in cid_dic):
            # cas不为空的时候进行存储
            if (cid_dic[str(sdf_cid)] != ''):
                func(*args)
                print('第{num}数据转化成功'.format(num=current_index))
            # 处理cas为空的情况
            else:
                print('cas号不存在!')
        else:
            # with open('../log/{cas}.log'.format(cas='fail_sdf'), encoding='utf-8', mode='a') as file:
            #     # 将转化失败的存入日志中
            #     file.write(str(sdf_cid))
            #     file.write('\n**失败原因: cid不在excel表里面！' + '\n')
            #     file.close()
            print(f"cid号不在当前字典中!")
    return wrapper


# 将sdf内容转化为mol存储，需要判断cas是否存在，如不存在则跳过
@IsNotEmpty
def convert_mol(savepath, temp_list, current_index, sdf_cid,cid_dic,saved_caslist,cas_list):
    data = cid_dic[str(sdf_cid)]
    save_mol(savefilepath=savepath, data=data, temp_list=temp_list,saved_caslist=saved_caslist,cas_list=cas_list,current_index=current_index)

def ConvertSdfToMol(cas_list,cid_dic,sdf_file,Save_Mol_Path):
    t1=time.time()
    # 用来标记存储过的cas
    saved_caslist=[]

    current_index = 0
    temp_list = []
    # flag用来标记是否处在多余部分
    flag = False
    # 默认路径
    savepath = Save_Mol_Path
    for index in tqdm(range(0, len(sdf_file))):
        if (flag == False and sdf_file[index] != 'M  END\n'):
            temp_list.append(sdf_file[index])
        elif (sdf_file[index] == 'M  END\n'):
            # 一个sdf的内容全部拿到，临时存储至temp_list
            temp_list.append(sdf_file[index])
            # 判断sdf的cid 和存储的cid是否对的上 去除换行的
            sdf_cid = temp_list[0].strip()

            # 根据cas号开始命名存储文件
            convert_mol(savepath, temp_list, current_index, sdf_cid,cid_dic,saved_caslist,cas_list)
            # convert_mol(savepath=str(savepath),temp_list=temp_list, current_index=current_index)
            current_index += 1
            # 清空临时列表
            temp_list = []
            # 这个时候进入多余部分，修改flag
            flag = True
            # 当达到cas_list的长度的时候，程序结束
            if (current_index == len(cas_list)):
                print("*********数据转化结束。感谢您的使用！")
                t2 = time.time()
                t = round(t2 - t1, 2)
                print('消耗时间{t}(s)'.format(t=t))
                break
        elif (sdf_file[index] == '$$$$\n'):
            flag = False
