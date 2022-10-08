import csv
import re
import chardet

os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
FILENAMES = ['info_1.txt', 'info_2.txt', 'info_3.txt', ]
PATTERNS = ['Изготовитель ОС', 'Название ОС', 'Код продукта', 'Тип системы']
main_data = [PATTERNS, ]


def get_data():
    for filename in FILENAMES:
        with open(filename, 'rb') as file:
            content = file.read()
        encoding = chardet.detect(content)['encoding']

        with open(filename, encoding=encoding) as encoding_file:
            data = encoding_file.readlines()
            for idx, pattern in enumerate(PATTERNS):
                for line in data:
                    result = re.findall(f'{pattern}.*', line)
                    if result:
                        result = result[0].split(':')[1].strip()
                        if idx == 0:
                            os_prod_list.append(result)
                        if idx == 1:
                            os_name_list.append(result)
                        if idx == 2:
                            os_code_list.append(result)
                        if idx == 3:
                            os_type_list.append(result)
    for idx in range(0, len(PATTERNS) - 1):
        list_to_main_data = [os_prod_list[idx], os_name_list[idx], os_code_list[idx], os_type_list[idx]]
        main_data.append(list_to_main_data)
    return main_data


def write_to_csv(to_filename):
    data = get_data()
    with open(to_filename, 'w', encoding='utf-8') as file:
        f_n_writer = csv.writer(file)
        for row in data:
            f_n_writer.writerow(row)


write_to_csv('to_filename.csv')