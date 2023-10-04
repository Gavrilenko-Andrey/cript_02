import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (QWidget,
                             QApplication,
                             QPushButton,
                             QMainWindow,
                             QLabel,
                             QGridLayout,
                             QVBoxLayout,
                             QStackedWidget,
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

        error = 1
        try:
            create_encoded_words(encoded_words, file_input_encode_probabilities)
        except FileNotFoundError:
            label = QLabel(f"There is no file named {file_input_encode_probabilities} in the static directory, \
please make sure you have created the file and set the right name.")
            #sys.exit()
        except ValueError as content:
            label = QLabel(content.args[0])
            #sys.exit()
        else:
            error = 0

        button_work_with_files = QPushButton(text="Работа с файлами")
        font = button_work_with_files.font()
        font.setPixelSize(24)
        button_work_with_files.setFont(font)
        button_work_with_files.setFixedSize(QSize(450, 300))
        button_work_with_files.clicked.connect(self.change_widget_to_files)

        button_work_with_writing = QPushButton(text="Работа вручную")
        font = button_work_with_writing.font()
        font.setPixelSize(24)
        button_work_with_writing.setFont(font)
        button_work_with_writing.setFixedSize(QSize(450, 300))
        button_work_with_writing.clicked.connect(self.change_widget_to_writing)

        button_get_parameters = QPushButton(text="Параметры")
        font = button_get_parameters.font()
        font.setPixelSize(24)
        button_get_parameters.setFont(font)
        button_get_parameters.setFixedSize(300, 150)

        button_return_main_from_files = QPushButton(text="Назад")
        font = button_return_main_from_files.font()
        font.setPixelSize(24)
        button_return_main_from_files.setFont(font)
        button_return_main_from_files.setFixedSize(100, 50)
        button_return_main_from_files.clicked.connect(self.change_widget_to_main)

        button_return_main_from_writing = QPushButton(text="Назад")
        font = button_return_main_from_writing.font()
        font.setPixelSize(24)
        button_return_main_from_writing.setFont(font)
        button_return_main_from_writing.setFixedSize(100, 50)
        button_return_main_from_writing.clicked.connect(self.change_widget_to_main)

        button_return_main_from_parameters = QPushButton(text="Назад")
        font = button_return_main_from_parameters.font()
        font.setPixelSize(24)
        button_return_main_from_parameters.setFont(font)
        button_return_main_from_parameters.setFixedSize(100, 50)
        button_return_main_from_parameters.clicked.connect(self.change_widget_to_main)

        button_files_encode = QPushButton(text="Кодировать")
        font = button_files_encode.font()
        font.setPixelSize(24)
        button_files_encode.setFont(font)
        button_files_encode.setFixedSize(450, 300)

        button_files_decode = QPushButton(text="Декодировать")
        font = button_files_decode.font()
        font.setPixelSize(24)
        button_files_decode.setFont(font)
        button_files_decode.setFixedSize(450, 300)

        button_files_encode_activate = QPushButton(text="Кодировать")
        font = button_files_encode_activate.font()
        font.setPixelSize(24)
        button_files_encode_activate.setFont(font)
        button_files_encode_activate.setFixedSize(300, 150)

        button_files_decode_activate = QPushButton(text="Декодировать")
        font = button_files_decode_activate.font()
        font.setPixelSize(24)
        button_files_decode_activate.setFont(font)
        button_files_decode_activate.setFixedSize(300, 150)

        button_files_return_from_encode = QPushButton(text="Назад")
        font = button_files_return_from_encode.font()
        font.setPixelSize(24)
        button_files_return_from_encode.setFont(font)
        button_files_return_from_encode.setFixedSize(100, 50)

        button_files_return_from_decode = QPushButton(text="Назад")
        font = button_files_return_from_decode.font()
        font.setPixelSize(24)
        button_files_return_from_decode.setFont(font)
        button_files_return_from_decode.setFixedSize(100, 50)

        button_writing_encode = QPushButton(text="Кодировать")
        font = button_writing_encode.font()
        font.setPixelSize(24)
        button_writing_encode.setFont(font)
        button_writing_encode.setFixedSize(450, 300)

        button_writing_decode = QPushButton(text="Декодировать")
        font = button_writing_decode.font()
        font.setPixelSize(24)
        button_writing_decode.setFont(font)
        button_writing_decode.setFixedSize(450, 300)

        button_writing_encode_activate = QPushButton(text="Кодировать")
        font = button_writing_encode_activate.font()
        font.setPixelSize(24)
        button_writing_encode_activate.setFont(font)
        button_writing_encode_activate.setFixedSize(300, 150)

        button_writing_decode_activate = QPushButton(text="Декодировать")
        font = button_writing_decode_activate.font()
        font.setPixelSize(24)
        button_writing_decode_activate.setFont(font)
        button_writing_decode_activate.setFixedSize(300, 150)

        button_writing_return_from_encode = QPushButton(text="Назад")
        font = button_writing_return_from_encode.font()
        font.setPixelSize(24)
        button_writing_return_from_encode.setFont(font)
        button_writing_return_from_encode.setFixedSize(100, 50)

        button_writing_return_from_decode = QPushButton(text="Назад")
        font = button_writing_return_from_decode.font()
        font.setPixelSize(24)
        button_writing_return_from_decode.setFont(font)
        button_writing_return_from_decode.setFixedSize(100, 50)

        self.begin_layout = QGridLayout()
        self.begin_layout.addWidget(button_work_with_files, 1, 0)
        self.begin_layout.addWidget(button_work_with_writing, 1, 2)
        self.begin_layout.addWidget(button_get_parameters, 2, 1)

        self.files_layout = QGridLayout()
        self.files_layout.addWidget(button_return_main_from_files, 0, 0)
        self.files_layout.addWidget(button_files_encode, 1, 0)
        self.files_layout.addWidget(button_files_decode, 1, 1)

        self.files_widget = QWidget()
        self.files_widget.setLayout(self.files_layout)

        self.writing_layout = QGridLayout()
        self.writing_layout.addWidget(button_return_main_from_writing, 0, 0,
                                      alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.writing_layout.addWidget(button_writing_encode, 1, 20, 1, 30)
        self.writing_layout.addWidget(button_writing_decode, 1, 60, 1, 23)

        self.writing_widget = QWidget()
        self.writing_widget.setLayout(self.writing_layout)

        params_layout = QGridLayout()

        self.main_widget = QWidget()

        if error:
            pass
            layout = QVBoxLayout()
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setWordWrap(True)
            font = label.font()
            font.setPixelSize(28)
            font.setBold(True)
            label.setFont(font)
            layout.addWidget(label)
            self.main_widget.setLayout(layout)
        else:
            self.main_widget.setLayout(self.begin_layout)

        self.setMinimumSize(self.sizeHint())

        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        self.stacked.addWidget(self.main_widget)
        self.stacked.addWidget(self.writing_widget)
        self.stacked.addWidget(self.files_widget)
        self.stacked.setCurrentWidget(self.main_widget)
        # self.setCentralWidget(self.main_widget)
        # self.stacked.setCurrentWidget(self.main_widget)

    def change_widget_to_files(self):
        self.stacked.setCurrentWidget(self.files_widget)
        # self.main_widget.
        # self.main_widget.setLayout(self.files_layout)

    def change_widget_to_writing(self):
        #pass
        self.stacked.setCurrentWidget(self.writing_widget)

    def change_widget_to_main(self):
        #pass
        self.stacked.setCurrentWidget(self.main_widget)


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
