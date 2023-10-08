import re


def make_decoded_string(encoded_words: dict, filename: str, raw_sequence=None) -> str:
    """
        Функция декодирования заданной строки из кодовых слов в строку из символов алфавита. Encoded_words - словарь
        соответствия символов алфавита и кодовых слов. Filename - имя файла, из которого производится чтение заданной
        последовательности. Raw_sequence - необязательный аргумент, строка, при передаче в функцию декодируется она,
        а не строка из файла
        """
    if raw_sequence == "":
        return ""
    decoded_words = {word: letter for letter, word in encoded_words.items()}
    if not raw_sequence:
        with open(f"./static/{filename}") as input_encoded_string_file:
            encoded_sequence = input_encoded_string_file.read()
    else:
        encoded_sequence = raw_sequence
    if re.search('[^01]', encoded_sequence):
        raise ValueError("В вашей последовательности есть неподдерживаемые символы. Поддерживаемыми символами являются \
0 и 1. Пожалуйста, проверьте это.")
    decoded_sequence = ""
    pointer = 0
    while pointer < len(encoded_sequence):
        for word in decoded_words:
            if encoded_sequence.find(word, pointer, pointer + len(word)) != -1:
                pointer += len(word)
                decoded_sequence += decoded_words[word]
                break
        else:
            raise ValueError("В вашей последовательности есть неподдерживаемые подпоследовательности, которые не могут \
быть декодированы с помощью текущего алфавита. Пожалуйста, проверьте это.")

    # decoded_sequence = encoded_sequence.translate(encoded_sequence.maketrans(decoded_words))
    # print(f'decoded sequence: {decoded_sequence}, decoded words:\n{decoded_words},\nencoded sequence:\
# {encoded_sequence}')
#         if re.search('[01]', decoded_sequence):
#             raise ValueError("There are unsupported sequences in your file. Message can't be decoded with the given \
# alphabet. Please, check it.")
    return decoded_sequence


def write_decoded_string_in_file(decoded_string: str, filename: str) -> None:
    """
        Функция записи декодированной строки в файл
        """
    with open(f'./static/{filename}', "w") as output_string_file:
        output_string_file.write(decoded_string)
