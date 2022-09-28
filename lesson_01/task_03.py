# Определить, какие из слов «attribute», «класс», «функция», «type»
# невозможно записать в байтовом типе. Важно: решение должно быть универсальным,
# т.е. не зависеть от того, какие конкретно слова мы исследуем.

word_01 = 'attribute'
word_02 = 'класс'
word_03 = 'функция'
word_04 = 'type'
words_list = [word_01, word_02, word_03, word_04]

for word in words_list:
    convertation = True
    for letter in word:
        if ord(letter) > 127:
            convertation = False
            break
    if convertation:
        print(f'Строка "{word}" конвертируется в байтовый тип ')
    else:
        print(f'Строка "{word}" не конвертируется в байтовый тип ')
