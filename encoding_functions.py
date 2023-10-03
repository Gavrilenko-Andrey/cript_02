import decimal
from math import log2


def create_encoded_words(encoded_words: dict, filename: str, raw_probabilities=None) -> None:
    eps = 1e-10
    decimal.getcontext().prec = 10
    if not raw_probabilities:
        with open(f'./static/{filename}') as input_probability_file:
            line = input_probability_file.readline()
        probability = line.split()
    else:
        probability = raw_probabilities
    if len(probability) != len(encoded_words):
        raise ValueError("You set the wrong amount of probabilities in your file. Please, check it.")
    for i in range(len(probability)):
        probability[i] = decimal.Decimal(float(probability[i]))
        # print(probability[i])
        if probability[i] < 0:
            raise ValueError("One of the probabilities was less than 0. Please, check it.")
    if sum(probability) <= 1 - eps or sum(probability) >= 1 + eps:
        raise ValueError("Sum of your probabilities is not equal to 1. Please, check it.")

    possible_letters = list(encoded_words)

    haffman_algorithm_array = [0] * len(probability)
    for i in range(len(probability)):
        haffman_algorithm_array[i] = [probability[i], [possible_letters[i]]]
    # print(haffman_algorithm_array)

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


def make_encoded_string(encoded_words: dict, filename: str, raw_sequence="") -> str:
    if not raw_sequence:
        with open(f'./static/{filename}') as input_string_file:
            sequence = input_string_file.read()
            # print(sequence)
    else:
        sequence = raw_sequence
    for elem in sequence:
        if elem not in encoded_words:
            raise ValueError("""Your sequence consists of symbols that are not present in the alphabet. 
Please, check it.""")
    return sequence.translate(sequence.maketrans(encoded_words))


def write_encoded_string_in_file(encoded_string: str, filename: str) -> None:
    with open(f'./static/{filename}', "w") as output_string_file:
        output_string_file.write(encoded_string)


def get_parameters(encoded_words: dict, filename: str, raw_probabilities=None) -> list:
    return [get_average_length_of_words(encoded_words, filename, raw_probabilities),
            get_redundancy(filename, raw_probabilities),  # filename is used in get_redundancy
            check_kraft_inequality(encoded_words)]


def get_average_length_of_words(encoded_words: dict, filename: str, raw_probabilities=None) -> float:  # Подразумевается
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
    print(f"now entropy: {now_entropy}, max entropy: {max_entropy}, average probability: \
{probability_of_word_in_uniform_distribution}")
    return 1 - now_entropy / max_entropy


def check_kraft_inequality(encoded_words: dict) -> list:
    left_part_of_kraft_inequality = 0
    left_part_of_kraft_inequality = decimal.Decimal(left_part_of_kraft_inequality)
    for elem in list(encoded_words.values()):
        left_part_of_kraft_inequality += decimal.Decimal(2**(-len(elem)))
    return [left_part_of_kraft_inequality <= 1, left_part_of_kraft_inequality]
