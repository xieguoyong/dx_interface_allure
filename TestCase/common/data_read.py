import os
from xlrd import open_workbook
import datetime
import yaml
from xlutils.copy import copy

upPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
yamlpath = os.path.join(upPath, "TestData", "g_data.yaml")


# 从excel文件中读取测试用例
def get_xls(type, excel_name, sheet_name):
    # excel文件路径
    excel_path = os.path.join(upPath, "TestData", excel_name)
    file = open_workbook(excel_path)
    sheet = file.sheet_by_name(sheet_name)
    # 总行数
    rows = sheet.nrows
    # 判断需要list还是dict的数据返回
    if type == "list":
        cls = []
        for i in range(rows):
            if i != 0:
                cls.append(sheet.row_values(i))

    elif type == "dict":
        cls = {}
        for i in range(rows):
            if i != 0:
                cls.setdefault(sheet.row_values(i)[0], sheet.row_values(i)[1])

    if sheet_name == "setup":
        num = cls['num']
        new_file = copy(file)
        new_sheet = new_file.get_sheet(0)
        new_sheet.write(1, 1, int(int(num) + 1))
        # new_sheet.write(3, 1, int(int(cls['user_phone']) + 1))

        new_file.save(excel_path)
        cls = handle_setup_data(cls)

    return cls


def handle_setup_data(cls):
    num = int(cls['num'])
    patient_code = int(cls['patient_code'])
    start_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # user_name = "%s%s" % (cls['user_name'], num)
    start_datetime = "%s %s" % (start_date, cls['StartDateTime'])
    end_datetime = "%s %s" % (start_date, cls['EndDateTime'])
    cls['num'] = str(num)
    # cls['user_name'] = str(user_name)
    # 开始日期结束日期均设置成当天
    cls[u'startDate'] = str(start_date)
    cls[u'endDate'] = str(start_date)
    cls['StartDateTime'] = str(start_datetime)
    cls['EndDateTime'] = str(end_datetime)
    cls['patient_code'] = str(patient_code)

    return cls


# 从yaml文件中读取数据
def get_yaml():
    f = open(yamlpath, 'r')
    # 读取，结果为dict类型
    x = yaml.load(f, Loader=yaml.FullLoader)
    f.close()
    return x


# 数据写入yaml文件
def set_yaml(data):
    f = open(yamlpath, 'w')
    # 将data追加写入到yaml文件中
    yaml.dump(data, f)
    f.close()


# 清除yaml中的数据
def del_yaml():
    f = open(yamlpath, 'w')
    f.truncate()

