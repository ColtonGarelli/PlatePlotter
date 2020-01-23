from PyQt5.Qt import *
import pandas as pd


def create_input_box(input_box):
    input_box.setMinimumSize(70, 20)
    input_box.setAlignment(Qt.AlignLeft)
    input_box.setReadOnly(False)
    input_box.setPlaceholderText("Enter group name")
    input_box.adjustSize()
    return input_box
