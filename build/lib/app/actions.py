from PyQt5.Qt import *
import pandas as pd


def deselect_boxes(table):
    selections = [(i.row(), i.column()) for i in table.selectedIndexes()]
    for i in selections:
        if table.item(*i) is None:
            table.setItem(*i, QTableWidgetItem())
            table.item(*i).setSelected(True)
        elif table.item(*i).text() != "":
            table.item(*i).setSelected(False)
    return table

#
# def right_click(right_click_event):
#
#     elif QMouseEvent.button() == Qt.RightButton:
#     # do what you want here
#     print("Right Button Clicked")
