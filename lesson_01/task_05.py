import locale
import platform
import subprocess
import chardet

default_encoding = locale.getpreferredencoding()
print(default_encoding)

param = '-n' if platform.system().lower() == 'windows' else '-c'
args = ['ping', param, '1', 'yandex.ru']
args2 = ['ping', param, '1', 'youtube.com']

with subprocess.Popen(args, stdout=subprocess.PIPE) as process:
    for line in process.stdout:
        chardet_result = chardet.detect(line)
        print(line.decode(chardet_result['encoding']))

with subprocess.Popen(args2, stdout=subprocess.PIPE) as process:
    for line in process.stdout:
        chardet_result = chardet.detect(line)
        print(line.decode(chardet_result['encoding']))
