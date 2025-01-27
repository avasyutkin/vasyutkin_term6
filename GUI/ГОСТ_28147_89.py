from textwrap import wrap

K = [{'0': 'c', '1': '4', '2': '6', '3': '2', '4': 'a', '5': '5', '6': 'b', '7': '9', '8': 'e', '9': '8', 'a': 'd', 'b': '7', 'c': '0', 'd': '3', 'e': 'f', 'f': '1'},
     {'0': '6', '1': '8', '2': '2', '3': '3', '4': '9', '5': 'a', '6': '5', '7': 'c', '8': '1', '9': 'e', 'a': '4', 'b': '7', 'c': 'b', 'd': 'd', 'e': '0', 'f': 'f'},
     {'0': 'b', '1': '3', '2': '5', '3': '8', '4': '2', '5': 'f', '6': 'a', '7': 'd', '8': 'e', '9': '1', 'a': '7', 'b': '4', 'c': 'c', 'd': '9', 'e': '6', 'f': '0'},
     {'0': 'c', '1': '8', '2': '2', '3': '1', '4': 'd', '5': '4', '6': 'f', '7': '6', '8': '7', '9': '0', 'a': 'a', 'b': '5', 'c': '3', 'd': 'e', 'e': '9', 'f': 'b'},
     {'0': '7', '1': 'f', '2': '5', '3': 'a', '4': '8', '5': '1', '6': '6', '7': 'd', '8': '0', '9': '9', 'a': '3', 'b': 'e', 'c': 'b', 'd': '4', 'e': '2', 'f': 'c'},
     {'0': '5', '1': 'd', '2': 'f', '3': '6', '4': '9', '5': '2', '6': 'c', '7': 'a', '8': 'b', '9': '7', 'a': '8', 'b': '1', 'c': '4', 'd': '3', 'e': 'e', 'f': '0'},
     {'0': '8', '1': 'e', '2': '2', '3': '5', '4': '6', '5': '9', '6': '1', '7': 'c', '8': 'f', '9': '4', 'a': 'b', 'b': '0', 'c': 'd', 'd': 'a', 'e': '3', 'f': '7'},
     {'0': '1', '1': '7', '2': 'e', '3': 'd', '4': '0', '5': '5', '6': '8', '7': '3', '8': '4', '9': 'f', 'a': 'a', 'b': '6', 'c': '9', 'd': 'c', 'e': 'b', 'f': '2'}]


def simple_swap_mode_gamma_generation(X, N1, N2):
    for count_X in range(4):
        if count_X == 3:  # в последних восьми циклах порядок считывания заполнений ключа обратный
            X = X[::-1]

        for i in range(len(X)):  # заполнение накопителя N1 суммируется по модулю 2^32 с заполнением накопителя X
            CM1 = '0' * (32 - len(bin((int(N1, 2) + int(X[i], 2)) % 2 ** 32)[2:])) + bin((int(N1, 2) + int(X[i], 2)) % 2 ** 32)[2:]

            CM1_ = wrap(CM1, 4)
            CM1 = ''
            for j in range(len(CM1_)):  # осуществляется подстановка в узлах замены по 4 бита на каждый узел
                CM1 += '0' * (4 - len(bin(int(K[j][hex(int(CM1_[j], 2))[2:]], 16))[2:])) + bin(int(K[j][hex(int(CM1_[j], 2))[2:]], 16))[2:]

            CM1 = CM1[11:] + CM1[:11]  # циклический сдвиг на одиннадцать шагов в сторону старших разрядов

            CM2 = '0' * (32 - len(bin(int(CM1, 2) ^ int(N2, 2))[2:])) + bin(int(CM1, 2) ^ int(N2, 2))[2:]  # результат сдвига суммируется поразрядно по модулю 2 с 32-разрядным заполнением накопителя N2

            N2 = N1  # содержимое N1 записывается в N2
            N1 = CM2  # полученный в СМ2 результат записывается в N1

    return N1, N2

def message_to_bin(message):
    message_arr = []
    for i in message:  # переводим в двоичный вид
        message_arr.append('0' * (16 - len(bin(ord(i))[2:])) + bin(ord(i))[2:])

    return message_arr


def key_to_bin(key):
    key_bin = ''
    for i in key:  # переводим в двоичный вид
        key_bin += '0' * (16 - len(bin(ord(i))[2:])) + bin(ord(i))[2:]

    return key_bin


def bin_to_message(bin_message):
    bin_message = wrap(bin_message, 16)
    Tш = ''
    for i in bin_message:  # переводим биты сообщения в текст
        Tш += chr(int(i, 2))

    return Tш


def encryption_decryption(message, K_S_, option):
    if len(K_S_) < 20:
        return 'Длина ключа должна быть равна двадцати символам.', K_S_
    if len(K_S_) > 20:
        K_S_ = K_S_[0:20]

    K_S[0], K_S[1] = key_to_bin(K_S_[0:16]), key_to_bin(K_S_[16:20])
    Tш = ''
    if option == True:  # если зашифровываем
        message = message_to_bin(message)

    Tо = wrap(''.join(message), 64)  # разбиваем исходное сообщение на блоки по 64 бит

    N1 = K_S[1][0: 32][::-1]  # первые 32 бита синхропосылки записываются в N1 (начинаем с первого разряда)
    N2 = K_S[1][32: 64][::-1]  # последние 32 бита - в N2 (начинаем с первого разряда)
    X = wrap(K_S[0], 32)  # заполняем ключ, разделяя его на блоки по 32 бита
    for i in range(len(X)):
        X[i] = X[i][::-1]  # начинаем с первого разряда

    N1_2 = simple_swap_mode_gamma_generation(X, N1, N2)  # генерируем гамму
    N1 = N1_2[0]
    N2 = N1_2[1]

    for i in range(len(Tо)):
        N4 = '0' * (32 - len(bin(int(N2, 2) + int(N6, 2) % 2 ** 32 - 1)[2:])) + bin(int(N2, 2) + int(N6, 2) % 2 ** 32 - 1)[2:]  # N2 суммируется по модулю (2^32—1) с 32-разрядной константой C1 из накопителя N6
        N3 = '0' * (32 - len(bin(int(N1, 2) + int(N5, 2) % 2 ** 32)[2:])) + bin(int(N1, 2) + int(N5, 2) % 2 ** 32)[2:]  # N1 суммируется по модулю 2^32 с 32-разрядной константой C2 из накопителя N5

        N1_2 = simple_swap_mode_gamma_generation(X, N3, N4)  # генерируем гамму
        N1 = N1_2[0][::-1]  # начинаем заполнение с первого разряда
        N2 = N1_2[1][::-1]  # начинаем заполнение с первого разряда
        N1_2 = N1 + N2

        for j in range(len(Tо[i])):
            if Tо[i][j] != '0' and Tо[i][j] != '1' and option == False:
                return 'Введенное сообщение не является шифртекстом.', K_S_
            Tш += str((int(Tо[i][j], 2) ^ int(N1_2[j], 2)))  # 64-разрядный блок гаммы шифра суммируется поразрядно по модулю 2 с первым 64-разрядным блоком открытых данных

    if option == False:  #если расшифровываем
        Tш = bin_to_message(Tш)

    return Tш, K_S_


K_S = ['', '']
N5 = '00000001000000010000000100000001'
N6 = '00000001000000010000000100000100'
