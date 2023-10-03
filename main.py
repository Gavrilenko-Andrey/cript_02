import sys
from encoding_functions import create_encoded_words, make_encoded_string, write_encoded_string_in_file, get_parameters
from decoding_functions import make_decoded_string, write_decoded_string_in_file

if __name__ == '__main__':
    encoded_words = {"A": "", "B": "", "C": "", "D": "", "E": "", "F": "", "1": "", "2": "", }

    file_input_encode_probabilities = "encode_input.txt"
    file_input_encode_sequence = "encode_sequence_input.txt"
    file_output_encode_sequence = "encode_sequence_output.txt"
    file_input_decode_sequence = "decode_sequence_input.txt"
    file_output_decode_sequence = "decode_sequence_output.txt"

    try:
        create_encoded_words(encoded_words, file_input_encode_probabilities)
    except FileNotFoundError:
        content = """There is no such file(s) in the static directory, please make sure you have created the file
and set the right name."""
        print(content)
        sys.exit()
    except ValueError as content:
        print(content)
        sys.exit()

    try:
        encoded_sequence = make_encoded_string(encoded_words, file_input_encode_sequence)
    except FileNotFoundError:
        content = """There is no such file(s) in the static directory, please make sure you have created the file
and set the right name."""
        print(content)
        sys.exit()
    except ValueError as content:
        print(content)
        sys.exit()
    print(encoded_sequence)

    print(encoded_words)

    try:
        write_encoded_string_in_file(encoded_sequence, file_output_encode_sequence)
    except FileNotFoundError:
        content = """There is no such file(s) in the static directory, please make sure you have created the file
and set the right name."""
        print(content)
        sys.exit()

    parameters = get_parameters(encoded_words, file_input_encode_probabilities)
    print(parameters)

    # decoded_words = {word: letter for word, letter in encoded_words.items()}

    try:
        decoded_sequence = make_decoded_string(encoded_words, file_input_decode_sequence)
    except FileNotFoundError:
        content = "There is no such file(s) in the static directory, please make sure you have created the file \
and set the right name."
        print(content)
        sys.exit()
    except ValueError as content:
        print(content)
        sys.exit()

    try:
        write_decoded_string_in_file(encoded_sequence, file_output_decode_sequence)
    except FileNotFoundError:
        content = """There is no such file(s) in the static directory, please make sure you have created the file
    and set the right name."""
        print(content)
        sys.exit()
