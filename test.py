import unittest
from encoding_functions import make_encoded_string, get_parameters, create_encoded_words
from decoding_functions import make_decoded_string


class Testencoding(unittest.TestCase):
    def setUp(self) -> None:
        self.encoded_words = {"A": "", "B": "", "C": "", "D": "", "E": "", "F": "", "1": "", "2": "", }

    def test_first(self) -> None:
        create_encoded_words(self.encoded_words, "", [
            0.9, 0.01, 0.01, 0.02, 0.05, 0.01, 0, 0,
        ])
        self.assertDictEqual(self.encoded_words, {'A': '0', 'B': '1101', 'C': '11000', 'D': '111', 'E': '10',
                                                  'F': '110010', '1': '1100110', '2': '1100111'})
        self.assertEqual(make_encoded_string(self.encoded_words, "", "AAAAA"), "00000")
        self.assertEqual(make_encoded_string(self.encoded_words, "",
                                             "BBA11122"),
                         "11011101011001101100110110011011001111100111")
        self.assertEqual(make_encoded_string(self.encoded_words, "",
                                             "ADEF121"),
                         "011110110010110011011001111100110")
        self.assertEqual(make_encoded_string(self.encoded_words, "",
                                             "CCCAAA"),
                         "110001100011000000")
        self.assertEqual(make_decoded_string(self.encoded_words, "",
                                             "11011101011001101100110110011011001111100111"),
                         "BBA11122")
        self.assertEqual(make_decoded_string(self.encoded_words, "",
                                             "110111000111"),
                         "BCD")
        self.assertEqual(make_decoded_string(self.encoded_words, "",
                                             "011110110010110011011001111100110"),
                         "ADEF121")
        self.assertEqual(make_decoded_string(self.encoded_words, "",
                                             "000110011111001111100110110011011110"),
                         "AAA2211DE")

    def test_second(self):
        self.encoded_words = {"A": "", "B": "", "C": "", "D": "", "E": "", "F": "", "1": "", "2": "", }
        create_encoded_words(self.encoded_words, "", [
            0.03125, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0, 0,
        ])
        self.assertDictEqual(self.encoded_words, {'A': '0', 'B': '1101', 'C': '11000', 'D': '111', 'E': '10',
                                                  'F': '110010', '1': '1100110', '2': '1100111'})
