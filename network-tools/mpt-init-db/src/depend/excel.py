import openpyxl


def load_excel_dict(file_name, begin_row=0):
    info_list = []
    workbook = openpyxl.load_workbook(filename=file_name)
    config_sheet = workbook.worksheets[0]
    keys = [key for index, key in enumerate(config_sheet.values) if index == 0][0]
    values = [value for index, value in enumerate(config_sheet.values) if index > begin_row and value[0] is not None]
    for values1 in values:
        dic = {
            str(key).strip(): str(value).strip() if value is not None else value for key, value in zip(keys, values1)
            if key is not None
        }

        info_list.append(dic)
    print(f'从{file_name}表中共读取到{len(info_list)}条数据')
    return info_list
