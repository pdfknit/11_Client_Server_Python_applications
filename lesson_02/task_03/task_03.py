import yaml


def open_yaml_file(filename):
    with open('src_file.yaml', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data


def write_to_yaml(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


data = open_yaml_file(filename='src_file.yaml')
filename = 'file.yaml'
write_to_yaml(filename, data)
data_02 = open_yaml_file(filename)
print(data == data_02)
