# -*- coding: utf-8 -*-
import xlrd
class getExcelData:
    def openFiles(self,files):
        try:
            data = xlrd.open_workbook(filename=files)
            return data
        except:
            print u"当前文件无法打开"
    def getRows(self,files,sheet):
        data = self.openFiles(files)
        table = data.sheet_by_name(sheet)
        nrows = table.nrows
        return nrows
    def getCols(self,files,sheet):
        data = self.openFiles(files)
        table = data.sheet_by_name(sheet)
        ncols = table.ncols
        return ncols
    def getallSheet(self,files):
        data = self.openFiles(files)
        sheets = data.sheet_names()
        return sheets
    def getSheet(self,files,sheet):
        data = self.openFiles(files)
        table = data.sheet_by_name(sheet)
        return table
    def getData(self,files,sheet):
        nrows = self.getRows(files,sheet)
        nclos = self.getCols(files,sheet)
        datas = []
        col_name=['xuqiu','case_router','case_title','case_pre','case_step','case_action','case_actionPre','case_prior','case_result','case_insru']
        sheet=self.getSheet(files,sheet)
        for i in range(2,nrows):
            data = {}
            rows = sheet.row_values(i)
            for j  in range(0,len(col_name)):
                data[col_name[j]]=rows[j]
                data["case_id"] = i-1
            datas.append(data)
        return datas
    def mulData(self,filepath):
        sheets = self.getallSheet(filepath)
        mulData = []
        for sheet in sheets:
            datas = self.getData(filepath,sheet)
            for data in datas:
                data['case_model'] = sheet
            mulData = mulData+datas
        return mulData
if __name__=="__main__":
    filepath = r'C:\Users\nan.wei\Desktop\海底捞测试用例.xlsx'.decode('utf-8')
    data = getExcelData()
    datas = data.mulData(filepath)
    print datas










