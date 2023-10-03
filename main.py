import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (QWidget,
                             QApplication,
                             QPushButton,
                             QMainWindow,
                             QLabel,
                             QGridLayout,
                             QVBoxLayout,
                             )

from encoding_functions import create_encoded_words, make_encoded_string, write_encoded_string_in_file, get_parameters
from decoding_functions import make_decoded_string, write_decoded_string_in_file


encoded_words = {"A": "", "B": "", "C": "", "D": "", "E": "", "F": "", "1": "", "2": "", }

file_input_encode_probabilities = "encode_input.txt"
file_input_encode_sequence = "encode_sequence_input.txt"
file_output_encode_sequence = "encode_sequence_output.txt"
file_input_decode_sequence = "decode_sequence_input.txt"
file_output_decode_sequence = "decode_sequence_output.txt"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background-color: #FFFAAA')
        self.setWindowTitle("Код Хаффмана")
        self.setFixedSize(QSize(1360, 766))
        widget = QWidget()
        self.setCentralWidget(widget)
        error = 1
        try:
            create_encoded_words(encoded_words, file_input_encode_probabilities)
        except FileNotFoundError:
            layout = QVBoxLayout()
            label = QLabel(f"There is no file named {file_input_encode_probabilities} in the static directory, \
please make sure you have created the file and set the right name.")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setWordWrap(True)
            font = label.font()
            font.setPixelSize(28)
            font.setBold(True)
            label.setFont(font)
            layout.addWidget(label)
            widget.setLayout(layout)
            #sys.exit()
        except ValueError as content:
            layout = QVBoxLayout()
            label = QLabel(content.args[0])
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setWordWrap(True)
            font = label.font()
            font.setPixelSize(28)
            font.setBold(True)
            label.setFont(font)
            layout.addWidget(label)
            widget.setLayout(layout)
            #sys.exit()
        else:
            error = 0

        button_work_with_files = QPushButton(text="Работа с файлами")
        font = button_work_with_files.font()
        font.setPixelSize(24)
        button_work_with_files.setFont(font)
        button_work_with_files.setFixedSize(QSize(450, 300))
        button_work_with_writing = QPushButton(text="Работа вручную")
        font = button_work_with_writing.font()
        font.setPixelSize(24)
        button_work_with_writing.setFont(font)
        button_work_with_writing.setFixedSize(QSize(450, 300))
        button_return = QPushButton(text="Назад")
        button_files_encode = QPushButton(text="Кодировать")
        button_files_decode = QPushButton(text="Декодировать")
        button_files_encode_activate = QPushButton(text="Кодировать")
        button_files_decode_activate = QPushButton(text="Декодировать")
        button_files_return = QPushButton(text="Назад")
        button_writing_encode = QPushButton(text="Кодировать")
        button_writing_decode = QPushButton(text="Декодировать")
        button_writing_encode_activate = QPushButton(text="Кодировать")
        button_writing_decode_activate = QPushButton(text="Декодировать")
        button_writing_return = QPushButton(text="Назад")

        begin_layout = QGridLayout()
        begin_layout.addWidget(button_work_with_files, 1, 0)
        begin_layout.addWidget(button_work_with_writing, 1, 1)
        if not error:
            widget.setLayout(begin_layout)
        self.setMinimumSize(self.sizeHint())


if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
    loh = 1
    if not loh:

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
