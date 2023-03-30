"""
    -- coding: utf-8 --
    @Author: codeking
    @Data : 2022/5/1 17:49
    @File : main.py.py
"""

# 继承这个类  py可以多继承
import sys

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFileDialog, QMessageBox, QHBoxLayout

from Utils.ConvertCsvToExcel import ConvertToExcel, AddCasToExcel, GetCaslist
from Utils.ConvertSdfToMol import ConvertSdfToMol
from Utils.DealPicture import rename_pic
from Utils.GenerateNums import GenNums
from Utils.GetCidDic import get_cid_dic, Read_SDF
from pubchemui import Ui_Pubchem_Tools


class View(QtWidgets.QWidget, Ui_Pubchem_Tools):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 设置标题
        # self.setWindowTitle("pubchem转化数据工具")
        self.csv_path=''
        self.sdf_path=''
        self.excel_path=''
        # 转化excel的状态
        self.ConvertToExcelFlag=False
        #选择存储mol的路径
        self.Save2DMolPath=''
        self.Save3DMolPath=''
        # 选择图片文件地址
        self.SelectPicPath=''
        self.SavePicPath=''

    # 生成数字的编辑栏
    @Slot()
    def on_NumsEdit_textChanged(self):
        self.GenNumsState.setText('还未生成')

    @Slot()
    def on_GenerateNumsButton_clicked(self):
        choice = QMessageBox.question(self, '确认', '您确认要执行该操作?')
        if choice == QMessageBox.Yes:
            print('确定')
            print(self.NumsEdit.text())
            self.GenNumsState.setText('正在生成！')
            GenNums(r'D:/DATA/',self.NumsEdit.text())
            print("生成结束！")
            self.GenNumsState.setText('生成成功！')
            QMessageBox.information(self, '提示', '生成成功！')
        elif choice == QMessageBox.No:
            print('取消')

    # 选择图片文件
    @Slot()
    def on_SelectPicButton_clicked(self):
        self.SelectPicPath=QFileDialog.getExistingDirectory(self,caption="选择你的图片文件",dir=r'D:\DATA\ALL_Pic')
        print(f"SelectPicPath: {self.SelectPicPath}")

    # 选择图片文件
    @Slot()
    def on_ConvertPicButton_clicked(self):
        if(self.SelectPicPath!='' and self.excel_path!=''):
            choice = QMessageBox.question(self, '确认', '您确认要执行该操作?')
            if choice == QMessageBox.Yes:
                print('确定')
                self.SavePicPath= self.SelectPicPath
                print(f"SelectPicPath: {self.SavePicPath}")
                # todo 转化图片
                # excel地址
                read_path=self.excel_path
                # 图片地址
                filePath=self.SavePicPath
                self.ConvertPicState.setText("正在转化，请稍后...")
                rename_pic(read_path,filePath)
                self.ConvertPicState.setText("转化成功!")
                QMessageBox.information(self, '提示', '转化成功！')
            elif choice == QMessageBox.No:
                print('取消')
        else:
            QMessageBox.warning(self, '警告', '请先选择图片文件夹和Excel文件！')

    @Slot()
    def on_Save2DMolButton_clicked(self):
        self.Save2DMolPath=QFileDialog.getExistingDirectory(self,caption="选择你的2Dmol存储文件",dir=r'D:\DATA\ALL_2DMol')
        print(f"Save2DMolPath: {self.Save2DMolPath}")

    @Slot()
    def on_Save3DMolButton_clicked(self):
        self.Save3DMolPath=QFileDialog.getExistingDirectory(self,caption="选择你的3Dmol存储文件",dir=r'D:\DATA\ALL_3DMol')
        print(f"Save3DMolPath: {self.Save3DMolPath}")


    @Slot()
    def on_SelectCsvButton_clicked(self):
        # 选择Csv文件
        # 返回值是元组， 不需要的参数用 _ 占位
        self.csv_path,_=QFileDialog.getOpenFileName(self,caption="选择你的csv文件",dir=r'D:\DATA\ALL_Excel',filter="选择csv文件(*.csv)")
        print(f"csv_path: {self.csv_path}")

    @Slot()
    def on_SelectSdfButton_clicked(self):
        self.sdf_path,_=QFileDialog.getOpenFileName(self,caption="选择你的sdf文件",dir=r'D:\DATA\ALL_SDF',filter="sdf(*.sdf)")
        print(f"sdf_path: {self.sdf_path}")

    @Slot()
    def on_SaveExcelButton_clicked(self):
        # print(mytime)
        if(self.csv_path!=''):
            choice = QMessageBox.question(self, '确认', '您确认要执行该操作?')
            if choice == QMessageBox.Yes:
                print('确定')
                ConvertToExcel(self.csv_path)
                self.ConvertState.setText('正在转化，请等待....')
                print("转化结束！")
                self.ConvertToExcelFlag=True
                self.ConvertState.setText('转化成功！')
                QMessageBox.information(self, '提示', '转化成功！')
            elif choice == QMessageBox.No:
                print('取消')
        else:
            QMessageBox.warning(self, '警告', '请先选择CSV文件！')

    # 将cas号添加到excel中
    @Slot()
    def on_AddCasToExcelButton_clicked(self):
        if(self.ConvertToExcelFlag==True):
            choice = QMessageBox.question(self, '确认', '您确认要执行该操作?')
            if choice == QMessageBox.Yes:
                print('确定')
                ExcelPath=self.csv_path.replace('csv','xlsx')
                AddCasToExcel(ExcelPath)
                self.AddCasState.setText('正在添加，请等待....')
                print("添加成功！")
                self.AddCasState.setText('添加成功！')
                QMessageBox.information(self, '提示', '添加成功！')
            elif choice == QMessageBox.No:
                print('取消')
        else:
            QMessageBox.warning(self, '警告', '请先转化Excel文件！')

    # 选择excel的按钮
    @Slot()
    def on_SelectExcelButton_clicked(self):
        # 选择excel文件
        self.excel_path,_=QFileDialog.getOpenFileName(self,caption="选择你的excel文件",dir=r'D:\DATA\ALL_Excel',filter="选择python文件(*.xlsx)")
        print(f"sdf_path: {self.excel_path}")


    @Slot()
    def on_SaveMol2DButton_clicked(self):
        if(self.sdf_path!='' and self.excel_path!='' and self.Save2DMolPath!=''):
            choice = QMessageBox.question(self, '确认', '您确认要执行该操作?')
            if choice == QMessageBox.Yes:
                print('确定')
                temp_data = GetCaslist(excel_path=r'{excel_path_f}'.format(excel_path_f=self.excel_path))
                cas_list = temp_data[0]
                cid_list = temp_data[1]
                #  将数据存储到cid_dic字典里面
                cid_dic = get_cid_dic(cid_list, cas_list)
                # 读取sdf的数据全部存储为列表了 写入sdf的路径
                sdf_file = Read_SDF(read_path=str(self.sdf_path))
                # todo 转化sdf到2Dmol文件
                Save_Mol_Path=self.Save2DMolPath
                self.Convert2DState.setText("正在转化，请等待....")
                ConvertSdfToMol(cas_list,cid_dic,sdf_file,Save_Mol_Path)
                QMessageBox.information(self, '提示', '转化成功！')
                self.Convert2DState.setText("2D转化成功！")
            elif choice == QMessageBox.No:
                print('取消')
        else:
            QMessageBox.warning(self, '警告', '请先选择SDF或者Excel文件！也或许没有选择存储路径！')

    @Slot()
    def on_SaveMol3DButton_clicked(self):
        if(self.sdf_path!='' and self.excel_path!=''and self.Save3DMolPath!=''):
            choice = QMessageBox.question(self, '确认', '您确认要执行该操作?')
            if choice == QMessageBox.Yes:
                print('确定')
                # todo 转化sdf为3Dmol文件
                temp_data = GetCaslist(excel_path=r'{excel_path_f}'.format(excel_path_f=self.excel_path))
                cas_list = temp_data[0]
                cid_list = temp_data[1]
                #  将数据存储到cid_dic字典里面
                cid_dic = get_cid_dic(cid_list, cas_list)
                # 读取sdf的数据全部存储为列表了 写入sdf的路径
                sdf_file = Read_SDF(read_path=str(self.sdf_path))
                # todo 转化sdf到3Dmol文件
                Save_Mol_Path=self.Save3DMolPath
                self.Convert3DState.setText("正在转化，请等待....")
                ConvertSdfToMol(cas_list,cid_dic,sdf_file,Save_Mol_Path)
                QMessageBox.information(self, '提示', '转化成功！')
                self.Convert3DState.setText("3D转化成功！")
                print("转化结束！")
                QMessageBox.information(self, '提示', '转化成功！')
            elif choice == QMessageBox.No:
                print('取消')
        else:
            QMessageBox.warning(self, '警告', '请先选择SDF或者Excel文件！也或许没有选择存储路径！')


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    # 设置风格样式 Fusion,windows,windowsvista
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    # window = QMainWindow() # 看自己的选择
    # window = QtWidgets.QWidget()  # 看自己的选择
    view = View()
    # view.setupUi(window)
    # view.setupUi(view)  这个可以放在构造函数中
    # window.show()
    view.show()
    sys.exit(app.exec())
