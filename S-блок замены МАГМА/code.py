from textwrap import wrap

S_blocks = [{'0': 'C', '1': '4', '2': '6', '3': '2', '4': 'A', '5': '5', '6': 'B', '7': '9', '8': 'E', '9': '8', 'A': 'D', 'B': '7', 'C': '0', 'D': '3', 'E': 'F', 'F': '1'},
            {'0': '6', '1': '8', '2': '2', '3': '3', '4': '9', '5': 'A', '6': '5', '7': 'C', '8': '1', '9': 'E', 'A': '4', 'B': '7', 'C': 'B', 'D': 'D', 'E': '0', 'F': 'F'},
            {'0': 'B', '1': '3', '2': '5', '3': '8', '4': '2', '5': 'F', '6': 'A', '7': 'D', '8': 'E', '9': '1', 'A': '7', 'B': '4', 'C': 'C', 'D': '9', 'E': '6', 'F': '0'},
            {'0': 'C', '1': '8', '2': '2', '3': '1', '4': 'D', '5': '4', '6': 'F', '7': '6', '8': '7', '9': '0', 'A': 'A', 'B': '5', 'C': '3', 'D': 'E', 'E': '9', 'F': 'B'},
            {'0': '7', '1': 'F', '2': '5', '3': 'A', '4': '8', '5': '1', '6': '6', '7': 'D', '8': '0', '9': '9', 'A': '3', 'B': 'E', 'C': 'B', 'D': '4', 'E': '2', 'F': 'C'},
            {'0': '5', '1': 'D', '2': 'F', '3': '6', '4': '9', '5': '2', '6': 'C', '7': 'A', '8': 'B', '9': '7', 'A': '8', 'B': '1', 'C': '4', 'D': '3', 'E': 'E', 'F': '0'},
            {'0': '8', '1': 'E', '2': '2', '3': '5', '4': '6', '5': '9', '6': '1', '7': 'C', '8': 'F', '9': '4', 'A': 'B', 'B': '0', 'C': 'D', 'D': 'A', 'E': '3', 'F': '7'},
            {'0': '1', '1': '7', '2': 'E', '3': 'D', '4': '0', '5': '5', '6': '8', '7': '3', '8': '4', '9': 'F', 'A': 'A', 'B': '6', 'C': '9', 'D': 'C', 'E': 'B', 'F': '2'}]

alphabet = {'А': '00', 'Б': '01', 'В': '02', 'Г': '03', 'Д': '04', 'Е': '05', 'Ё': '06', 'Ж': '07', 'З': '08', 'И': '09', 'Й': '0A', 'К': '0B', 'Л': '0C', 'М': '0D', 'Н': '0E', 'О': '0F', 'П': '10', 'Р': '11', 'С': '12', 'Т': '13', 'У': '14', 'Ф': '15', 'Х': '16', 'Ц': '17', 'Ч': '18', 'Ш': '19', 'Щ': '1A', 'Ъ': '1B', 'Ы': '1C', 'Ь': '1D', 'Э': '1E', 'Ю': '1F', 'Я': '20'}
shift_alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

def encryption(message):
    message_index = ''
    for i in message:  # записываем в строку индексы всех букв (alphabet)
        message_index += alphabet[i]

    message = wrap(message_index, 4)  # делим эту строку по 4 символа
    k = 0  # счетчик S-блоков
    encrypted_message = ''
    for i in message:
        for j in i:
            encrypted_message += S_blocks[k][j]  # записываем в строку на что заменили каждый символ
        k += 1
        if k == 7:
            k = 0
    print(encrypted_message)
    message = ''
    for i in encrypted_message:  # циклический сдвиг на 11 влево
        message += shift_alphabet[(shift_alphabet.index(i) - 11) % 16]

    return message

def decryption(encrypted_message):
    message = ''

    for i in encrypted_message:  # циклический сдвиг на 11 вправо
        message += shift_alphabet[(shift_alphabet.index(i) + 11) % 16]

    message = wrap(message, 4)  # делим зашифрованную строку по 4 символа
    decrypted_message = ''
    k = 0  # счетчик S-блоков
    for i in message:
        for j in i:
            for p in S_blocks[k]:
                if j == S_blocks[k][p]:
                    decrypted_message += p  # заменяем обратно
        k += 1
        if k == 7:
            k = 0


    decrypted_message = wrap(decrypted_message, 2)   # делим строку по 2 символа
    message = ''
    for i in decrypted_message:
        for j in alphabet:
            if i == alphabet[j]:
                message += j  # находим по полученным значениям исходные буквы (alphabet)

    return message


message = input("Введите фразу: ")

encrypted_message = encryption(message)
print('Зашифрованное сообщение: ', encrypted_message)

decrypted_message = decryption(encrypted_message)
print('Расшифрованное сообщение: ', decrypted_message)