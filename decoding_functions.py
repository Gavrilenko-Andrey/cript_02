import re


def make_decoded_string(encoded_words: dict, filename: str, raw_sequence="") -> str:
    decoded_words = {word: letter for letter, word in encoded_words.items()}
    if not raw_sequence:
        with open(f"./static/{filename}") as input_encoded_string_file:
            encoded_sequence = input_encoded_string_file.read()
    else:
        encoded_sequence = raw_sequence
    if re.search('[^01]', encoded_sequence):
        raise ValueError("There are unsupported symbols in your sequence, only supported symbols are 0 and 1. \
Please, check it.")
    decoded_sequence = ""
    pointer = 0
    while pointer < len(encoded_sequence):
        for word in decoded_words:
            if encoded_sequence.find(word, pointer, pointer + len(word)) != -1:
                pointer += len(word)
                decoded_sequence += decoded_words[word]
                break
        else:
            raise ValueError("There are unsupported sequences in your file. Message can't be decoded with the given\
alphabet. Please, check it.")

    # decoded_sequence = encoded_sequence.translate(encoded_sequence.maketrans(decoded_words))
    print(f'decoded sequence: {decoded_sequence}, decoded words:\n{decoded_words},\nencoded sequence:\
{encoded_sequence}')

#         if re.search('[01]', decoded_sequence):
#             raise ValueError("There are unsupported sequences in your file. Message can't be decoded with the given \
# alphabet. Please, check it.")
    return decoded_sequence


def write_decoded_string_in_file(decoded_string: str, filename: str) -> None:
    with open(f'./static/{filename}', "w") as output_string_file:
        output_string_file.write(decoded_string)
