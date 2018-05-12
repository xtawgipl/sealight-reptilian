import xlwt

import Constants
from logger.loggerFactory import logger
from service.LightInfosService import LightInfosService
from service.ManufacturerService import ManufacturerService
from service.TechnologyService import TechnologyService


class OutputExcel(object):

    def __init__(self, file_path):
        self.technologyService = TechnologyService()
        self.lightInfosService = LightInfosService()
        self.file_path = file_path
        self.workbook = xlwt.Workbook()
        self.title_list = ["系列", "类型"]
        self.default_style = xlwt.easyxf('align: wrap on, vert center;align: horiz center')

    def create_sheet(self, sheet_name):
        """创建表"""
        return self.workbook.add_sheet(sheet_name, cell_overwrite_ok=True)  # 创建sheet

    def set_common_style(self, name, bold, color_index, height, pattern_fore_colour):
        """单元格样式"""
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name
        font.bold = bold
        font.color_index = color_index
        font.height = height
        style.font = font

        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        borders.bottom_colour = 0x3A
        style.borders = borders

        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER  # 垂直对齐
        alignment.vert = xlwt.Alignment.VERT_CENTER  # 水平对齐
        alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT  # 自动换行
        style.alignment = alignment

        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN

        """
            May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
        """
        pattern.pattern_fore_colour = pattern_fore_colour
        style.pattern = pattern
        return style

    def set_title_style(self, pattern_fore_colour=None):
        """单元格样式"""
        if pattern_fore_colour is None:
            pattern_fore_colour = 1
        return self.set_common_style('宋体', True, 2, 15 * 20, pattern_fore_colour)

    def set_content_style(self):
        """单元格样式"""
        return self.set_common_style('宋体', False, 1, 12 * 20, 1)

    def write_row(self, sheet, data, row_num, start_col_num=None, style=None):
        # if style is None:
        #     style = self.set_content_style()
        if start_col_num is None:
            start_col_num = 0
        """写一行数据"""
        if type(data) == list:
            for col in range(start_col_num, start_col_num + len(data)):
                if style is None:
                    sheet.write(row_num, col, data[col - start_col_num], self.default_style)
                else:
                    sheet.write(row_num, col, data[col - start_col_num], style)
        else:
            raise RuntimeError('格式不正确，必须为list类型数据')

    def save(self):
        """保存文件"""
        self.workbook.save(self.file_path)

    def get_manufacturer_data(self, manufacturerService, __manufacturer_id):
        return manufacturerService.find_by_key(__manufacturer_id)

    def get_light_titles(self, __manufacturer_data):
        """计算前、后、内 灯的表头"""
        # 前灯集合
        front_title_set = set()

        # 后灯集合
        rear_title_set = set()

        # 内类集合
        internal_title_set = set()
        model_list = __manufacturer_data.modelList
        for mode in model_list:
            type_list = mode.typeList
            for type in type_list:
                light_list = type.lightList
                for light in light_list:
                    if light.pos_id in Constants.FRONT_POS_ID_LIST:
                        front_title_set.add(light.use_name)
                    elif light.pos_id in Constants.REAR_POS_ID_LIST:
                        rear_title_set.add(light.use_name)
                    elif light.pos_id in Constants.INTERNAL_POS_ID_LIST:
                        internal_title_set.add(light.use_name)

        front_title_list = list(front_title_set)
        rear_title_list = list(rear_title_set)
        internal_title_list = list(internal_title_set)
        front_title_list.sort()
        rear_title_list.sort()
        internal_title_list.sort()
        logger.info("front_title_list = {}".format(front_title_list))
        logger.info("rear_title_list = {}".format(rear_title_list))
        logger.info("internal_title_list = {}".format(internal_title_list))
        return front_title_list, rear_title_list, internal_title_list

    def get_light_dataset(self, __manufacturer_data, front_title_list, rear_title_list, internal_title_list):
        """生成灯数据列表"""
        light_list_data = list()
        model_list = __manufacturer_data.modelList
        for mode in model_list:
            type_list = mode.typeList
            for type in type_list:
                light_list = type.lightList
                light_dict = self._init_light_dict(mode.model_name, type, front_title_list, rear_title_list, internal_title_list)
                for light in light_list:
                    technology_list = self.technologyService.find_by_type_use(type.type_id, light.use_id)
                    light_info_str = ""
                    counter = 0
                    for technology in technology_list:
                        counter += 1
                        light_info_str += "["
                        light_info_str += technology.technology_name
                        light_info_str += "] "
                        lightInfos = self.lightInfosService.find_by_keys(type.type_id, light.use_id, technology.technology_id)
                        light_info_str += lightInfos.osram_ece
                        if counter != len(technology_list):
                            light_info_str += "\r\n"
                    light_dict[light.use_name] = light_info_str
                light_list_data.append(light_dict)
        return light_list_data

    def _init_light_dict(self, model_name, type, front_title_list, rear_title_list, internal_title_list):
        light_dict = dict()
        light_dict["model_name"] = model_name
        light_dict["type_name"] = "{} {}kW built {}.{}-{}.{}".format(type.type_name, type.type_kw,
                                                                     type.type_from_month, type.type_from_year,
                                                                     type.type_to_month, type.type_to_year)
        for light_name in front_title_list:
            light_dict[light_name] = ""
        for light_name in rear_title_list:
            light_dict[light_name] = ""
        for light_name in internal_title_list:
            light_dict[light_name] = ""
        return light_dict

    def create_title(self, front_title_list, rear_title_list, internal_title_list):
        """生成excel表头"""
        pass


if __name__ == '__main__':

    # 表头占2行
    title_low_num = 2

    # 系列 列开始合并的列
    model_merge_start = title_low_num

    # type 类型 列开始合并的列
    type_merge_start = title_low_num

    manufacturerService = ManufacturerService()
    manufacturer_data = manufacturerService.find_by_key(1)

    outputExcel = OutputExcel(Constants.EXCEL_PATH + "{}.xls".format(manufacturer_data.manufacturer_name))
    sheet = outputExcel.create_sheet(manufacturer_data.manufacturer_name)

    front_title_list, rear_title_list, internal_title_list = outputExcel.get_light_titles(manufacturer_data)
    light_list = list()
    light_list.extend(front_title_list)
    light_list.extend(rear_title_list)
    light_list.extend(internal_title_list)

    title_len = len(outputExcel.title_list)
    front_len = len(front_title_list)
    rear_len = len(rear_title_list)
    internal_len = len(internal_title_list)
    sheet.write_merge(0, 0,
                      title_len,
                      title_len + front_len - 1,
                      "前灯", outputExcel.set_title_style(2))
    sheet.write_merge(0, 0,
                      title_len + front_len,
                      title_len + front_len + rear_len - 1,
                      "后灯", outputExcel.set_title_style(3))
    sheet.write_merge(0, 0,
                      title_len + front_len + rear_len,
                      title_len + front_len + rear_len + internal_len - 1,
                      "内灯", outputExcel.set_title_style(5))

    for col_num in range(0, len(outputExcel.title_list)):
        sheet.write_merge(0, 1, col_num, col_num, outputExcel.title_list[col_num], outputExcel.set_title_style())

    outputExcel.write_row(sheet, light_list, 1, title_len, outputExcel.set_title_style())

    for col_num in range(0, len(light_list) + len(outputExcel.title_list)):
        sheet.col(col_num).width = 256 * 20

    dataset = outputExcel.get_light_dataset(manufacturer_data, front_title_list, rear_title_list, internal_title_list)

    for i in range(0, len(dataset)):
        outputExcel.write_row(sheet, list(dataset[i].values()), i + 2, 0)
        if i != 0:
            if dataset[i]["model_name"] != dataset[i - 1]["model_name"]:
                if i - 1 + title_low_num - model_merge_start > 1:
                    sheet.write_merge(model_merge_start, i - 1 + title_low_num, 0, 0,
                                      dataset[i - 1]["model_name"], outputExcel.default_style)
                    model_merge_start = i + title_low_num
            # if dataset[i]["type_name"] != dataset[i - 1]["type_name"]:
            #     if i - 1 + title_low_num - type_merge_start > 1:
            #         sheet.write_merge(type_merge_start, i - 1 + title_low_num, 1, 1,
            #                           dataset[i - 1]["type_name"], outputExcel.default_style)
            #         type_merge_start = i + title_low_num

    sheet.write_merge(model_merge_start, len(dataset) - 1 + title_low_num, 0, 0,
                      dataset[len(dataset) - 1]["model_name"], outputExcel.default_style)
    # sheet.write_merge(type_merge_start, len(dataset) - 1 + title_low_num, 1, 1,
    #                   dataset[len(dataset) - 1]["type_name"], outputExcel.default_style)
    outputExcel.save()
