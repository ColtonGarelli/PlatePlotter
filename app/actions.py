from PyQt5.Qt import QTableWidget
import pandas as pd
import csv, os


def deselect_boxes(table):
    selections = [(i.row(), i.column()) for i in table.selectedIndexes()]
    for i in selections:
        if table.item(*i) is None:
            table.setItem(*i, QTableWidgetItem())
            table.item(*i).setSelected(True)
        elif table.item(*i).text() != "":
            table.item(*i).setSelected(False)
    return table


def fill_cells(items, table, button_group):
    for i in items:
        # Fill and remove TableWidgetItem objects rather than fill text
        if table.item(*i) is None:
            filler = QTableWidgetItem(button_group.checkedButton().text())
            table.setItem(*i, filler)
        else:
            table.item(*i).setText(button_group.checkedButton().text())
    table.clearSelection()


def file_handler(path, table: QTableWidget, write: bool):
    if path is not None and os.path.isfile(path) or os.path.isdir(path):
        if write:
            data = []
            for row in range(table.rowCount()):
                rows = []
                for col in range(table.columnCount()):
                    to_save = table.item(row, col)
                    if isinstance(to_save, QTableWidgetItem):
                        rows.append(to_save.text())
                    else:
                        rows.append("")
                data.append(rows)
            df = pd.DataFrame(data, index=pd.Index(list('ABCDEFGH')), columns=range(1, 13))
            df.to_csv(path)
            return path
        else:
            with open(os.path.join(path), 'r+') as file:
                plate = list()
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    plate.append(row[1:])
            return plate


#
# def right_click(right_click_event):
#
#     elif QMouseEvent.button() == Qt.RightButton:
#     # do what you want here
#     print("Right Button Clicked")
