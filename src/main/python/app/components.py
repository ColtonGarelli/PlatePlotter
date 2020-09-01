"""
Trying to reduce file size for readability and reusability
"""
from PyQt5.Qt import QTableWidget, QBoxLayout, QObject, QWidget, QAbstractButton, QButtonGroup, QRadioButton, QPushButton, QCheckBox, Qt


def setup_table(plate: QTableWidget):
    plate.resizeColumnsToContents()
    plate.resizeRowsToContents()
    plate.setRowCount(8)
    plate.setColumnCount(12)
    plate.setAutoScroll(True)
    plate.setHorizontalHeaderLabels([str(i) for i in range(1, 12)])
    plate.setVerticalHeaderLabels([i for i in 'ABCDEFGH'])
    return plate


def create_input_box(input_box, text):
    input_box.setMinimumSize(70, 20)
    input_box.setAlignment(Qt.AlignLeft)
    input_box.setReadOnly(False)
    input_box.setPlaceholderText(text)
    input_box.adjustSize()
    return input_box


def add_to_box_layout(layout: QBoxLayout, *items: QObject, alignment=None, stretch=None): #use kwargs?
    """

    """
    for item in items:
        if isinstance(item, QWidget):
            addQThing = layout.addWidget
        elif isinstance(item, QBoxLayout):
            addQThing = layout.addLayout
        else:
            print("Something is seriously wrong")
            break
        if stretch is None and alignment is None:
            addQThing(item)
        elif stretch is None and alignment is not None:
            addQThing(item, alignment=alignment)
        elif stretch is not None and alignment is None:
            addQThing(item, stretch=stretch)
        elif stretch is not None and alignment is not None:
            addQThing(item, alignment=alignment, stretch=stretch)
        else:
            print("Something else just went wrong man")


def add_button(group: QButtonGroup, *buttons: [QAbstractButton]):
    """

    """
    for button in buttons:
        group.addButton(button)


def make_buttons(button_type, *names: str):
    """

    """
    buttons = []
    if button_type == 'radio':
        for name in names:
            buttons.append(QRadioButton(name))
    elif button_type == 'push':
        for name in names:
            buttons.append(QPushButton(name))
    elif button_type == 'check':
        for name in names:
            buttons.append(QCheckBox(name))
    return buttons

