
import xlwt

from logger.loggerFactory import logger


class ExcelUtil(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.workbook = xlwt.Workbook()

    def create_sheet(self, sheet_name):
        return self.workbook.add_sheet(sheet_name, cell_overwrite_ok=True)  # 创建sheet

    def set_style(__name, height, bold=False):
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = __name  # 'Times New Roman'
        font.bold = bold
        font.color_index = 2
        font.height = height
        style.font = font
        return style

    def write_row(self, sheet, row_num, data):
        if type(data) == list:
            for col in range(0, len(data)):
                sheet.write(row_num, col, data[col])
        else:
            raise RuntimeError('格式不正确，必须为list类型数据')

    def save(self):
        self.workbook.save(self.file_path)  # 保存文件


if __name__ == '__main__':
    excelUtil = ExcelUtil("D:/test.xls")
    excelUtil.write_row(excelUtil.create_sheet("test"), 1, [1, 2, 3, 4, 5])
    excelUtil.save()