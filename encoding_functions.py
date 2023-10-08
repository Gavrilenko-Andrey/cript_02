import decimal
from math import log2


def create_encoded_words(encoded_words: dict, filename: str, raw_probabilities=None) -> None:
    """
    Функция создания кодовых слов для символов заданного алфавита по вероятностям встречи этих символов в алфавите
    encoded words - словарь, ключами которого являются символы алфавита, а значениями до передачи в функцию -
    пустые строки, а после выполнения функции - кодовые слова. Filename - имя файла, из которого производится
    считывание вероятностей символов. Raw_probabilities - необязательный аргумент, список, при передаче значения
    вероятностей берутся из переданного списка
    """
    eps = 1e-10
    decimal.getcontext().prec = 10
    if not raw_probabilities:
        with open(f'./static/{filename}') as input_probability_file:
            line = input_probability_file.readline()
        probability = line.split()
    else:
        probability = raw_probabilities
    if len(probability) != len(encoded_words):
        raise ValueError("Вы установили неверное количество вероятностей. Пожалуйста, проверьте это")
    for i in range(len(probability)):
        try:
            probability[i] = decimal.Decimal(float(probability[i]))
        except ValueError:
            raise ValueError(f"Как минимум одна из вероятностей ({i+1}я) является не дробным числом, а символом. \
Пожалуйста, проверьте это.")
        # print(probability[i])
        if probability[i] < 0:
            raise ValueError("Одна из вероятностей оказалась меньше 0. Пожалуйста, проверьте это.")
    if sum(probability) <= 1 - eps or sum(probability) >= 1 + eps:
        raise ValueError("Сумма вероятностей не равна 1. Пожалуйста, проверьте это")

    possible_letters = list(encoded_words)

    haffman_algorithm_array = [0] * len(probability)
    for i in range(len(probability)):
        haffman_algorithm_array[i] = [probability[i], [possible_letters[i]]]
    # print(haffman_algorithm_array)
    # Свм алгоритм Хаффмана:
    while len(haffman_algorithm_array) > 1:
        haffman_algorithm_array.sort(key=lambda elem: elem[0], reverse=True)

        for letter in haffman_algorithm_array[-1][1]:
            encoded_words[letter] = "1" + encoded_words[letter]
        for letter in haffman_algorithm_array[-2][1]:
            encoded_words[letter] = "0" + encoded_words[letter]

        haffman_algorithm_array[-2][0] += haffman_algorithm_array[-1][0]
        haffman_algorithm_array[-2][1].extend(haffman_algorithm_array[-1][1])
        haffman_algorithm_array.pop()
    #     print(haffman_algorithm_array)
    # print(encoded_words)


def make_encoded_string(encoded_words: dict, filename: str, raw_sequence=None) -> str:
    """
    Функция кодирования заданной строки из символов алфавита в строку из кодовых слов. Encoded_words - словарь
    соответствия символов алфавита и кодовых слов. Filename - имя файла, из которого производится чтение заданной
    последовательности. Raw_sequence - необязательный аргумент, строка, при передаче в функцию кодируется она,
    а не строка из файла
    """
    if raw_sequence == "":
        return ""
    if not raw_sequence:
        with open(f'./static/{filename}') as input_string_file:
            sequence = input_string_file.read()
            # print(sequence)
    else:
        sequence = raw_sequence
    for elem in sequence:
        if elem not in encoded_words:
            raise ValueError("Ваша последовательность состоит из символов не представленных в алфавите. Пожалуйста, \
проверьте это.")
    return sequence.translate(sequence.maketrans(encoded_words))


def write_encoded_string_in_file(encoded_string: str, filename: str) -> None:
    """
    Функция записи закодированной строки в файл
    """
    with open(f'./static/{filename}', "w") as output_string_file:
        output_string_file.write(encoded_string)


def get_parameters(encoded_words: dict, filename: str, raw_probabilities=None) -> list:
    """
    Функция получения параметров кодируемого алфавита. Возвращает список из трех элементов. Первый - средняя длина
    кодового слова, второй - избыточность алфавита, третий - список из двух элементов: булевское значение - выполнение
    неравенства Крафта и дробное число - левая часть этого неравенства. Encoded_words - словарь
    соответствия символов алфавита и кодовых слов. Filename - имя файла, из которого производится чтение заданной
    последовательности. Raw_probabilities - необязательный аргумент, список, при передаче значения
    вероятностей берутся из переданного списка
    """
    return [get_average_length_of_words(encoded_words, filename, raw_probabilities),
            get_redundancy(filename, raw_probabilities),  # filename is used in get_redundancy
            check_kraft_inequality(encoded_words)]


def get_average_length_of_words(encoded_words: dict, filename: str, raw_probabilities=None) -> float:  # Подразумевается
    """
    Функция получения средней длины кодового слова алфавита
    """
    if not raw_probabilities:
        with open(f'./static/{filename}') as input_probability_file:  # что filename имеет то же значение,
            line = input_probability_file.readline()  # что и filename в функции create_encoded_words.
        probability = line.split()  # Также подразумевается, что эта функция вызывается после create_encoded_words.
    else:
        probability = raw_probabilities
    average_length = 0
    encoded_words_values = list(encoded_words.values())
    for i in range(len(probability)):
        probability[i] = float(probability[i])
        average_length += len(encoded_words_values[i]) * probability[i]
    return average_length


def get_redundancy(filename: str, raw_probabilities=None) -> float:  # Подразумевается, что filename имеет то же
    """
    Функция получения избыточности алфавита
    """
    if not raw_probabilities:
        with open(f'./static/{filename}') as input_probability_file:  # значение что и filename в функции
            line = input_probability_file.readline()  # create_encoded_words. Также подразумевается, что
        probability = line.split()  # эта функция вызывается после create_encoded_words.
    else:
        probability = raw_probabilities
    for i in range(len(probability)):
        probability[i] = float(probability[i])

    now_entropy = 0
    max_entropy = 0
    probability_of_word_in_uniform_distribution = 1 / len(probability)
    for i in range(len(probability)):
        # print(probability[i])
        now_entropy += probability[i] * log2(probability[i]) if probability[i] != 0 else 0
        max_entropy += probability_of_word_in_uniform_distribution * log2(probability_of_word_in_uniform_distribution)
    # print(f"now entropy: {now_entropy}, max entropy: {max_entropy}, average probability: \
# {probability_of_word_in_uniform_distribution}")
    return 1 - now_entropy / max_entropy


def check_kraft_inequality(encoded_words: dict) -> list:
    """
    Функция проверки неравенства Крафта и нахождения его левой части
    """
    decimal.getcontext().prec = 6
    left_part_of_kraft_inequality = 0
    left_part_of_kraft_inequality = decimal.Decimal(left_part_of_kraft_inequality)
    for elem in list(encoded_words.values()):
        left_part_of_kraft_inequality += decimal.Decimal(2**(-len(elem)))
    return [left_part_of_kraft_inequality <= 1, left_part_of_kraft_inequality]
