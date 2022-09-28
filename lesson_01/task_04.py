word_01 = 'разработка'
word_02 = 'администрирование'
word_03 = 'protocol'
word_04 = 'standard'

words_list = [word_01, word_02, word_03, word_04]
words_list_utf = []
word_list_decode = []

for word in words_list:
    words_list_utf.append(word.encode('utf-8'))

for word in words_list_utf:
    print(type(word))
    word_list_decode.append(word.decode('utf-8'))

print(words_list)
print(words_list_utf)
print(word_list_decode)
print( words_list == word_list_decode)



