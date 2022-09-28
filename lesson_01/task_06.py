import chardet

with open('test_file.txt', 'rb') as file:
    content = file.read()
encoding = chardet.detect(content)['encoding']
print(encoding)

with open('test_file.txt', encoding=encoding) as encoding_file:
    for line in encoding_file:
        print(line)

