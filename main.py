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
                             QLineEdit,
                             )
from encoding_functions import create_encoded_words, make_encoded_string, write_encoded_string_in_file, get_parameters
from decoding_functions import make_decoded_string, write_decoded_string_in_file


class MainWindow(QMainWindow):
    """
    Единственное окно в графическом интерфейсе
    """
    def __init__(self):
        super().__init__()
        # Изначальный словарь соответствия символов алфавита и кодовых слов
        self.encoded_words = {"A": "", "B": "", "C": "", "D": "", "E": "", "F": "", "1": "", "2": "", }
        # файлы, используемые для записи и прочтения последовательностей
        self.file_input_encode_probabilities = "encode_input.txt"
        self.file_input_encode_sequence = "encode_sequence_input.txt"
        self.file_output_encode_sequence = "encode_sequence_output.txt"
        self.file_input_decode_sequence = "decode_sequence_input.txt"
        self.file_output_decode_sequence = "decode_sequence_output.txt"
        self.setStyleSheet('background-color: #FFFAAA')
        self.setWindowTitle("Код Хаффмана")
        self.setFixedSize(QSize(1360, 766))
        # При запуске программы функция пытается считать вероятности из файла, если файла не удается обнаружить -
        # приложение выдает сообщение об ошибке
        error = 1
        try:
            create_encoded_words(self.encoded_words, self.file_input_encode_probabilities)
            # print(self.encoded_words)
        except FileNotFoundError:
            label = QLabel(f"There is no file named {self.file_input_encode_probabilities} in the static directory, \
please make sure you have created the file and set the right name.")
            #sys.exit()
        except ValueError as content:
            label = QLabel(content.args[0])
            #sys.exit()
        else:
            error = 0

        # Кнопка на главном экране - переход на экран "Работы с фалами"
        button_work_with_files = QPushButton(text="Работа с файлами")
        font = button_work_with_files.font()
        font.setPixelSize(24)
        button_work_with_files.setFont(font)
        button_work_with_files.setFixedSize(QSize(450, 300))
        button_work_with_files.clicked.connect(self.change_widget_to_files)

        # Кнопка на главном экране - переход на экран "Работы вручную"
        button_work_with_writing = QPushButton(text="Работа вручную")
        font = button_work_with_writing.font()
        font.setPixelSize(24)
        button_work_with_writing.setFont(font)
        button_work_with_writing.setFixedSize(QSize(450, 300))
        button_work_with_writing.clicked.connect(self.change_widget_to_writing)

        """
        Кнопка на главном экране - переход на экран "Параметры", функция получения параметров вызывается при 
        первом запуске программы
        """
        button_get_parameters = QPushButton(text="Параметры")
        font = button_get_parameters.font()
        font.setPixelSize(24)
        button_get_parameters.setFont(font)
        button_get_parameters.setFixedSize(300, 150)
        button_get_parameters.clicked.connect(self.change_widget_to_params)

        # Кнопка на экране "Работа с файлами" - переход на главный экран"
        button_return_main_from_files = QPushButton(text="Назад")
        font = button_return_main_from_files.font()
        font.setPixelSize(24)
        button_return_main_from_files.setFont(font)
        button_return_main_from_files.setFixedSize(100, 50)
        button_return_main_from_files.clicked.connect(self.change_widget_to_main)

        # Кнопка на экране "Работа вручную" - переход на главный экран"
        button_return_main_from_writing = QPushButton(text="Назад")
        font = button_return_main_from_writing.font()
        font.setPixelSize(24)
        button_return_main_from_writing.setFont(font)
        button_return_main_from_writing.setFixedSize(100, 50)
        button_return_main_from_writing.clicked.connect(self.change_widget_to_main)

        # Кнопка на экране "Параметры" - переход на главный экран"
        button_return_main_from_parameters = QPushButton(text="Назад")
        font = button_return_main_from_parameters.font()
        font.setPixelSize(24)
        button_return_main_from_parameters.setFont(font)
        button_return_main_from_parameters.setFixedSize(100, 50)
        button_return_main_from_parameters.clicked.connect(self.change_widget_to_main)

        # Кнопка на экране "Работа с файлами" - переход на  экран кодирования последовательности из файла"
        button_files_encode = QPushButton(text="Кодировать")
        font = button_files_encode.font()
        font.setPixelSize(24)
        button_files_encode.setFont(font)
        button_files_encode.setFixedSize(450, 300)
        button_files_encode.clicked.connect(self.change_widget_to_files_encode)

        # Кнопка на экране "Работа с файлами" - переход на  экран декодирования последовательности из файла"
        button_files_decode = QPushButton(text="Декодировать")
        font = button_files_decode.font()
        font.setPixelSize(24)
        button_files_decode.setFont(font)
        button_files_decode.setFixedSize(450, 300)
        button_files_decode.clicked.connect(self.change_widget_to_files_decode)

        """
        Кнопка на экране кодирования последовательности из файла - запуск функции кодирования последовательности 
        из заданного файла, при успешном выполнении записывает закодированную последовательность в файл и отображает ее.
        Если последовательность состоит из неподдерживаемых символов или последовательностей - кнопка неактивна.
        """
        button_files_encode_activate = QPushButton(text="Кодировать и записать в файл")
        font = button_files_encode_activate.font()
        font.setPixelSize(24)
        button_files_encode_activate.setFont(font)
        button_files_encode_activate.setFixedSize(450, 300)
        button_files_encode_activate.clicked.connect(self.activate_files_encode)

        """
        Кнопка на экране декодирования последовательности из файла - запуск функции декодирования последовательности 
        из заданного файла, при успешном выполнении записывает декодированную последовательность в файл и отображает ее.
        Если последовательность состоит из неподдерживаемых символов или последовательностей - кнопка неактивна.
        """
        button_files_decode_activate = QPushButton(text="Декодировать и записать в файл")
        font = button_files_decode_activate.font()
        font.setPixelSize(24)
        button_files_decode_activate.setFont(font)
        button_files_decode_activate.setFixedSize(450, 300)
        button_files_decode_activate.clicked.connect(self.activate_files_decode)

        """
        Кнопка на экране кодирования последовательности из файла - переход на экран "Работа с файлами" 
        """
        button_files_return_from_encode = QPushButton(text="Назад")
        font = button_files_return_from_encode.font()
        font.setPixelSize(24)
        button_files_return_from_encode.setFont(font)
        button_files_return_from_encode.setFixedSize(100, 50)
        button_files_return_from_encode.clicked.connect(self.change_widget_to_files)

        """
        Кнопка на экране декодирования последовательности из файла - переход на экран "Работа с файлами" 
        """
        button_files_return_from_decode = QPushButton(text="Назад")
        font = button_files_return_from_decode.font()
        font.setPixelSize(24)
        button_files_return_from_decode.setFont(font)
        button_files_return_from_decode.setFixedSize(100, 50)
        button_files_return_from_decode.clicked.connect(self.change_widget_to_files)

        # Кнопка на экране "Работа вручную" - переход на  экран кодирования последовательности вручную"
        button_writing_encode = QPushButton(text="Кодировать")
        font = button_writing_encode.font()
        font.setPixelSize(24)
        button_writing_encode.setFont(font)
        button_writing_encode.setFixedSize(450, 300)
        button_writing_encode.clicked.connect(self.change_widget_to_writing_encode)

        # Кнопка на экране "Работа вручную" - переход на  экран декодирования последовательности вручную"
        button_writing_decode = QPushButton(text="Декодировать")
        font = button_writing_decode.font()
        font.setPixelSize(24)
        button_writing_decode.setFont(font)
        button_writing_decode.setFixedSize(450, 300)
        button_writing_decode.clicked.connect(self.change_widget_to_writing_decode)

        """
        Кнопка на экране кодирования последовательности вручную - запуск функции кодирования заданной пользователем 
        последовательности, при успешном выполнении отображает закодированную последовательность. 
        Если последовательность состоит из неподдерживаемых символов или последовательностей - кнопка неактивна.
        """
        button_writing_encode_activate = QPushButton(text="Кодировать")
        font = button_writing_encode_activate.font()
        font.setPixelSize(24)
        button_writing_encode_activate.setFont(font)
        button_writing_encode_activate.setFixedSize(450, 300)
        button_writing_encode_activate.clicked.connect(self.activate_writing_encode)

        """
        Кнопка на экране декодирования последовательности вручную - запуск функции декодирования заданной пользователем 
        последовательности, при успешном выполнении отображает декодированную последовательность.
        Если последовательность состоит из неподдерживаемых символов или последовательностей - кнопка неактивна.
        """
        button_writing_decode_activate = QPushButton(text="Декодировать")
        font = button_writing_decode_activate.font()
        font.setPixelSize(24)
        button_writing_decode_activate.setFont(font)
        button_writing_decode_activate.setFixedSize(450, 300)
        button_writing_decode_activate.clicked.connect(self.activate_writing_decode)

        """
        Кнопка на экране декодирования последовательности вручную - переход на экран "Работа вручную" 
        """
        button_writing_return_from_encode = QPushButton(text="Назад")
        font = button_writing_return_from_encode.font()
        font.setPixelSize(24)
        button_writing_return_from_encode.setFont(font)
        button_writing_return_from_encode.setFixedSize(100, 50)
        button_writing_return_from_encode.clicked.connect(self.change_widget_to_writing)

        """
        Кнопка на экране декодирования последовательности вручную - переход на экран "Работа вручную" 
        """
        button_writing_return_from_decode = QPushButton(text="Назад")
        font = button_writing_return_from_decode.font()
        font.setPixelSize(24)
        button_writing_return_from_decode.setFont(font)
        button_writing_return_from_decode.setFixedSize(100, 50)
        button_writing_return_from_decode.clicked.connect(self.change_widget_to_writing)

        """
        Главный экран - при ошибке чтения из файла вероятностей символов алфавита показывает сообщение об ошибке.
        При отсутствии ошибок отображает кнопки перехода на экраны "Работа с файлами", "Работа вручную", "Параметры".
        """
        self.begin_layout = QGridLayout()
        self.begin_layout.addWidget(button_work_with_files, 1, 0)
        self.begin_layout.addWidget(button_work_with_writing, 1, 2)
        self.begin_layout.addWidget(button_get_parameters, 2, 1)

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

        """
        Экран "Работа с файлами", имеет кнопки перехода на экраны кодирования и декодирования последовательностей из
        файлов, а также кнопку перехода на главный экран.
        """
        self.files_layout = QGridLayout()
        self.files_layout.addWidget(button_return_main_from_files, 0, 0,
                                    alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.files_layout.addWidget(button_files_encode, 1, 20, 1, 30)
        self.files_layout.addWidget(button_files_decode, 1, 60, 1, 23)

        self.files_widget = QWidget()
        self.files_widget.setLayout(self.files_layout)

        """
        Экран кодировки последовательности из файла, имеет кнопку кодирования последовательности из файла 
        и записи ее в кодовых словах одновременно в файл и на экран. В случае ошибки выводит на экран ее текст.
        Также имеет кнопку перехода на экран "Работы с файлами".
        """
        self.files_encode_layout = QGridLayout()
        label1 = QLabel("")
        font = label1.font()
        font.setPixelSize(24)
        label1.setFont(font)
        label1.setWordWrap(True)
        label2 = QLabel("")
        font = label2.font()
        font.setPixelSize(24)
        label2.setFont(font)
        label2.setWordWrap(True)
        self.files_encode_layout.addWidget(button_files_return_from_encode, 0, 0,
                                           alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.files_encode_layout.addWidget(label1, 1, 0, 1, 50)
        self.files_encode_layout.addWidget(label2, 1, 51, 1, 100)
        self.files_encode_layout.addWidget(button_files_encode_activate, 2, 49)

        self.files_encode_widget = QWidget()
        self.files_encode_widget.setLayout(self.files_encode_layout)

        """
        Экран декодировки последовательности из файла, имеет кнопку декодирования последовательности из файла 
        и записи ее в символах алфавита одновременно в файл и на экран. В случае ошибки выводит на экран ее текст.
        Также имеет кнопку перехода на главный экран "Работы с файлами".
        """
        self.files_decode_layout = QGridLayout()
        label1 = QLabel("")
        font = label1.font()
        font.setPixelSize(24)
        label1.setFont(font)
        label1.setWordWrap(True)
        label2 = QLabel("")
        font = label2.font()
        font.setPixelSize(24)
        label2.setFont(font)
        label2.setWordWrap(True)

        self.files_decode_layout.addWidget(button_files_return_from_decode, 0, 0,
                                           alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.files_decode_layout.addWidget(label1, 1, 0, 1, 50)
        self.files_decode_layout.addWidget(label2, 1, 51, 1, 100)
        self.files_decode_layout.addWidget(button_files_decode_activate, 2, 49)

        self.files_decode_widget = QWidget()
        self.files_decode_widget.setLayout(self.files_decode_layout)

        """
        Экран "Работа вручную", имеет кнопки перехода на экраны кодирования и декодирования последовательностей вручную,
        а также кнопку перехода на главный экран.
        """
        self.writing_layout = QGridLayout()
        self.writing_layout.addWidget(button_return_main_from_writing, 0, 0,
                                      alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.writing_layout.addWidget(button_writing_encode, 1, 20, 1, 30)
        self.writing_layout.addWidget(button_writing_decode, 1, 60, 1, 23)

        """
        Экран кодировки последовательности вручную, имеет кнопку кодирования введенной пользователем последовательности
        и выводу ее на экран. В случае ошибки кодировки выводит на экран ее текст. 
        Также имеет кнопку перехода на экран "Работы вручную".
        """
        self.writing_encode_layout = QGridLayout()
        label1 = QLabel("Исходная последовательность")
        font = label1.font()
        font.setPixelSize(24)
        label1.setFont(font)
        label1.setWordWrap(True)
        textarea1 = QLineEdit()
        font = textarea1.font()
        font.setPixelSize(24)
        textarea1.setFont(font)
        label2 = QLabel("Закодированная последовательность")
        font = label2.font()
        font.setPixelSize(24)
        label2.setFont(font)
        label2.setWordWrap(True)
        textarea2 = QLineEdit()
        font = textarea2.font()
        font.setPixelSize(24)
        textarea2.setFont(font)
        self.writing_encode_layout.addWidget(button_writing_return_from_encode, 0, 0,
                                             alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.writing_encode_layout.addWidget(label1, 1, 0, 1, 50)
        self.writing_encode_layout.addWidget(label2, 1, 51, 1, 100)
        self.writing_encode_layout.addWidget(textarea1, 2, 0, 5, 50)
        self.writing_encode_layout.addWidget(textarea2, 2, 51, 5, 100)
        self.writing_encode_layout.addWidget(button_writing_encode_activate, 6, 49, 8, 74)
        
        self.writing_encode_widget = QWidget()
        self.writing_encode_widget.setLayout(self.writing_encode_layout)

        """
        Экран декодировки последовательности вручную, имеет кнопку декодирования введенной пользователем 
        последовательности и выводу ее на экран. В случае ошибки кодировки выводит на экран ее текст. 
        Также имеет кнопку перехода на экран "Работы вручную".
        """
        self.writing_decode_layout = QGridLayout()
        label1 = QLabel("Исходная последовательность")
        font = label1.font()
        font.setPixelSize(24)
        label1.setFont(font)
        label1.setWordWrap(True)
        textarea1 = QLineEdit()
        font = textarea1.font()
        font.setPixelSize(24)
        textarea1.setFont(font)
        label2 = QLabel("Декодированная последовательность")
        font = label2.font()
        font.setPixelSize(24)
        label2.setFont(font)
        label2.setWordWrap(True)
        textarea2 = QLineEdit()
        font = textarea2.font()
        font.setPixelSize(24)
        textarea2.setFont(font)
        self.writing_decode_layout.addWidget(button_writing_return_from_decode, 0, 0,
                                             alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.writing_decode_layout.addWidget(label1, 1, 0, 1, 50)
        self.writing_decode_layout.addWidget(label2, 1, 51, 1, 100)
        self.writing_decode_layout.addWidget(textarea1, 2, 0, 5, 50)
        self.writing_decode_layout.addWidget(textarea2, 2, 51, 5, 100)
        self.writing_decode_layout.addWidget(button_writing_decode_activate, 6, 49, 8, 74)

        self.writing_decode_widget = QWidget()
        self.writing_decode_widget.setLayout(self.writing_decode_layout)

        self.writing_widget = QWidget()
        self.writing_widget.setLayout(self.writing_layout)

        """
        Экран "Параметры", отображает следующие параметры алфавита: средняя длина кодового слова, избыточность,
        выполнение/невыполнение неравенства Крафта и его левую часть
        """
        self.params_layout = QGridLayout()
        self.params_widget = QWidget()
        """
        В случае удачного прочтения вероятностей символов алфавита из файла при запуске программы выполняется функция
        вычисления параметров алфавита
        """
        if not error:
            self.parameters = get_parameters(self.encoded_words, self.file_input_encode_probabilities)
            label_params_average_length = QLineEdit(f"Средняя длина кодовых слов равна {self.parameters[0]:.6f}")
            font = label_params_average_length.font()
            font.setPixelSize(24)
            label_params_average_length.setFont(font)
            label_params_redundancy = QLineEdit(f"Избыточность равна {self.parameters[1]:.6f}")
            font = label_params_redundancy.font()
            font.setPixelSize(24)
            label_params_redundancy.setFont(font)
            if self.parameters[2][0]:
                check_kraft = "выполняется"
            else:
                check_kraft = "не выполняется"
            label_params_kraft_inequality = QLineEdit(f"Неравенство Крафта {check_kraft}. Левая часть равна \
{self.parameters[2][1]:.6f}")
            font = label_params_kraft_inequality.font()
            font.setPixelSize(24)
            label_params_kraft_inequality.setFont(font)
            label_params_encoded_words = QLineEdit(f"Кодовые слова: {self.encoded_words}")
            font = label_params_encoded_words.font()
            font.setPixelSize(24)
            label_params_encoded_words.setFont(font)
            self.params_layout.addWidget(button_return_main_from_parameters, 0, 0,
                                         alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            self.params_layout.addWidget(label_params_average_length, 1, 10, 1, 100)
            self.params_layout.addWidget(label_params_redundancy, 2, 10, 2, 100)
            self.params_layout.addWidget(label_params_kraft_inequality, 3, 10, 3, 100)
            self.params_layout.addWidget(label_params_encoded_words, 4, 10, 4, 100)
            # print(self.parameters)

        self.params_widget.setLayout(self.params_layout)

        self.setMinimumSize(self.sizeHint())

        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        self.stacked.addWidget(self.main_widget)
        self.stacked.addWidget(self.writing_widget)
        self.stacked.addWidget(self.files_widget)
        self.stacked.addWidget(self.params_widget)
        self.stacked.addWidget(self.files_encode_widget)
        self.stacked.addWidget(self.files_decode_widget)
        self.stacked.addWidget(self.writing_encode_widget)
        self.stacked.addWidget(self.writing_decode_widget)
        self.stacked.setCurrentWidget(self.main_widget)
        # self.setCentralWidget(self.main_widget)
        # self.stacked.setCurrentWidget(self.main_widget)

        self.encoded_sequence = ""
        self.decoded_sequence = ""

    def change_widget_to_files(self):
        # Функция вызывающая экран "Работы с файлами"
        self.stacked.setCurrentWidget(self.files_widget)

    def change_widget_to_writing(self):
        # Функция вызывающая экран "Работы вручную"
        self.stacked.setCurrentWidget(self.writing_widget)

    def change_widget_to_main(self):
        # Функция вызывающая главный экран
        self.stacked.setCurrentWidget(self.main_widget)

    def change_widget_to_params(self):
        # Функция вызывающая экран "Параметры"
        self.stacked.setCurrentWidget(self.params_widget)
        self.stacked.currentWidget().layout().itemAt(1).widget().setText(f"Средняя длина кодовых слов равна \
{self.parameters[0]:.6f}")
        self.stacked.currentWidget().layout().itemAt(2).widget().setText(f"Избыточность равна {self.parameters[1]:.6f}")
        if self.parameters[2][0]:
            check_kraft = "выполняется"
        else:
            check_kraft = "не выполняется"
        self.stacked.currentWidget().layout().itemAt(3).widget().setText(f"Неравенство Крафта {check_kraft}. \
Левая часть равна {self.parameters[2][1]:.6f}")
        self.stacked.currentWidget().layout().itemAt(4).widget().setText(f"Кодовые слова: {self.encoded_words}")

    def change_widget_to_files_encode(self):
        # Функция вызывающая экран кодировки последовательности из файла и кодировку последовательности из файла
        self.stacked.setCurrentWidget(self.files_encode_widget)
        self.stacked.currentWidget().layout().itemAt(1).widget().setText("")
        self.stacked.currentWidget().layout().itemAt(2).widget().setText("")
        self.stacked.currentWidget().layout().itemAt(3).widget().setEnabled(False)
        try:
            self.encoded_sequence = make_encoded_string(self.encoded_words, self.file_input_encode_sequence)
        except FileNotFoundError:
            content = f"В папке static не существует файла {self.file_input_encode_sequence}, пожалуйста, убедитесь \
что вы создали файл и задали правильное имя."
            self.stacked.currentWidget().layout().itemAt(1).widget().setText(content)
            #print(content)
        except ValueError as content:
            content = content.args[0]
            self.stacked.currentWidget().layout().itemAt(1).widget().setText(content)
        else:
            with open(f'./static/{self.file_input_encode_sequence}') as input_string_file:
                sequence = input_string_file.read()
            content = "Текущая последовательность в файле: " + sequence
            self.stacked.currentWidget().layout().itemAt(3).widget().setEnabled(True)
            self.stacked.currentWidget().layout().itemAt(1).widget().setText(content)

    def activate_files_encode(self):
        # Функция производящая запись закодированной последовательности в другой файл и вывод ее на экран
        try:
            write_encoded_string_in_file(self.encoded_sequence, self.file_output_encode_sequence)
        except FileNotFoundError:
            content = f"В папке static не существует файла {self.file_output_encode_sequence}, пожалуйста, убедитесь \
что вы создали файл и задали правильное имя."
            self.stacked.currentWidget().layout().itemAt(2).widget().setText(content)
        else:
            self.stacked.currentWidget().layout().itemAt(2).widget().setText("Закодированная последовательность: " +
                                                                             self.encoded_sequence)

    def change_widget_to_files_decode(self):
        # Функция вызывающая экран декодировки последовательности из файла и производящая декодировку последовательности
        self.stacked.setCurrentWidget(self.files_decode_widget)
        self.stacked.currentWidget().layout().itemAt(1).widget().setText("")
        self.stacked.currentWidget().layout().itemAt(2).widget().setText("")
        self.stacked.currentWidget().layout().itemAt(3).widget().setEnabled(False)
        try:
            self.decoded_sequence = make_decoded_string(self.encoded_words, self.file_input_decode_sequence)
        except FileNotFoundError:
            content = f"В папке static не существует файла {self.file_input_decode_sequence}, пожалуйста, убедитесь \
что вы создали файл и задали правильное имя."
            self.stacked.currentWidget().layout().itemAt(1).widget().setText(content)
            # print(content)
        except ValueError as content:
            content = content.args[0]
            self.stacked.currentWidget().layout().itemAt(1).widget().setText(content)
        else:
            with open(f'./static/{self.file_input_decode_sequence}') as input_string_file:
                sequence = input_string_file.read()
            content = "Текущая последовательность в файле: " + sequence
            self.stacked.currentWidget().layout().itemAt(3).widget().setEnabled(True)
            self.stacked.currentWidget().layout().itemAt(1).widget().setText(content)

    def activate_files_decode(self):
        # Функция производящая запись декодированной последовательности в файл и вывод ее на экран
        try:
            write_decoded_string_in_file(self.decoded_sequence, self.file_output_decode_sequence)
        except FileNotFoundError:
            content = f"В папке static не существует файла {self.file_output_decode_sequence}, пожалуйста, убедитесь \
что вы создали файл и задали правильное имя."
            self.stacked.currentWidget().layout().itemAt(2).widget().setText(content)
        else:
            self.stacked.currentWidget().layout().itemAt(2).widget().setText("Декодированная последовательность: " +
                                                                             self.decoded_sequence)
    
    def change_widget_to_writing_encode(self):
        # Функция вызывающая экран кодировки последовательности вручную
        self.stacked.setCurrentWidget(self.writing_encode_widget)
        self.stacked.currentWidget().layout().itemAt(3).widget().setText("")
        self.stacked.currentWidget().layout().itemAt(4).widget().setText("")
      
    def activate_writing_encode(self):
        # Функция вызывающая кодировку заданной пользователем оследовательности и производящая вывод ее на экран
        sequence = self.stacked.currentWidget().layout().itemAt(3).widget().text()
        try:
            self.encoded_sequence = make_encoded_string(self.encoded_words, self.file_input_encode_sequence, sequence)
            self.stacked.currentWidget().layout().itemAt(4).widget().setText(self.encoded_sequence)
        except FileNotFoundError:
            content = f"В папке static не существует файла {self.file_input_encode_sequence}, пожалуйста, убедитесь \
что вы создали файл и задали правильное имя."
            self.stacked.currentWidget().layout().itemAt(4).widget().setText(content)
        except ValueError as content:
            self.stacked.currentWidget().layout().itemAt(4).widget().setText(content.args[0])

    def change_widget_to_writing_decode(self):
        # Функция вызывающая экран декодировки последовательности вручную
        self.stacked.setCurrentWidget(self.writing_decode_widget)
        self.stacked.currentWidget().layout().itemAt(3).widget().setText("")
        self.stacked.currentWidget().layout().itemAt(4).widget().setText("")

    def activate_writing_decode(self):
        # Функция вызывающая декодировку заданной пользователем оследовательности и производящая вывод ее на экран
        sequence = self.stacked.currentWidget().layout().itemAt(3).widget().text()
        try:
            self.decoded_sequence = make_decoded_string(self.encoded_words, self.file_input_decode_sequence, sequence)
            self.stacked.currentWidget().layout().itemAt(4).widget().setText(self.decoded_sequence)
        except FileNotFoundError:
            content = f"В папке static не существует файла {self.file_input_decode_sequence}, пожалуйста, убедитесь \
что вы создали файл и задали правильное имя."
            self.stacked.currentWidget().layout().itemAt(4).widget().setText(content)
        except ValueError as content:
            self.stacked.currentWidget().layout().itemAt(4).widget().setText(content.args[0])


if __name__ == '__main__':
    # Создание графическогог приложения
    app = QApplication(sys.argv)
    # Создание главного и единственного окна
    window = MainWindow()
    # Показ главного окна
    window.show()
    # Запуск графического приложения
    app.exec()

