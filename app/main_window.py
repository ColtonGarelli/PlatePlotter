import csv
import os
import sys

import pandas as pd
from PyQt5.Qt import QApplication, QButtonGroup, QTableWidget, QVBoxLayout, QLineEdit, QMainWindow, QHBoxLayout,\
    QLabel, QWidget, QCheckBox, QPushButton, QAbstractItemView, QActionGroup, QTableWidgetItem, QFileDialog, \
    QMessageBox, Qt, QRadioButton, QHeaderView, QAction

from app import actions
from app import components, connect_to_robot


# input group names
# check boxes to highlight groups on plate
# explicit deselect aka click to deselect cells


# make sure boxes dont belong to multiple groups
# resize side panel
# any more features?
# output plate


class platePlot(QMainWindow):
    # resize_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        #
        # Initialize variables
        self.current_selection = []
        self.groups = []
        self.group_buttons = []
        self.groups_dict = {}
        self.save_path = ""
        #
        # initialize components
        self.main_widg = QWidget()
        self.main_layout = QHBoxLayout()
        self.table = QTableWidget()
        self.table_layout = QHBoxLayout()
        self.side_layout = QVBoxLayout()
        self.input_box = QLineEdit()
        self.box_label = QLabel()
        self.group_button_group = QButtonGroup()
        self.expr_button_group = QButtonGroup()
        #
        # set up buttons
        self.select_elisa, self.select_facs, self.select_qpcr = components.make_buttons('check', 'ELISA', 'qPCR', 'FACS')
        self.robot_save, self.done_button = components.make_buttons('push', 'Save to robot', 'Save',)
        self.load_map_button, self.clear_cells_button, self.enter_button = components.make_buttons('push', 'Load a map', 'Clear', 'Enter')
        self.table.setSelectionMode(QAbstractItemView.MultiSelection)
        self.group_button_group.setExclusive(True)
        #
        # Init plate stuff
        self.setup_window()
        self.setup_expr_selection()
        self.init_plate()
        self.create_window()
        self.entry_done()
        self.load_map_button.clicked.connect(self.load_map_from_file)
        self.robot_save.clicked.connect(self.save_expr_to_robot)
        self.table.clicked.connect(self.deselect)
        self.clear_cells_button.clicked.connect(self.clear_cells)
        self.group_button_group.buttonClicked.connect(self.select_group)
        self.done_button.clicked.connect(self.save_and_quit)
        #
        # Add the display to the general layout
        self.selections = QActionGroup(self.input_box)
        self.select = [self.selections.addAction(QAction(i)) for i in self.groups]

    def load_map_from_file(self):
        self.groups = []
        plate_path, _ = QFileDialog.getOpenFileName(self, caption='Load plate')
        if os.path.isfile(plate_path):
            with open(os.path.join(plate_path), 'r+') as file:
                plate = list()
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    plate.append(row[1:])
            for row in range(len(plate)):
                for i in range(len(plate[row])):
                    if plate[row][i].strip():
                        self.table.setItem(row, i, QTableWidgetItem(plate[row][i]))
                        if plate[row][i] not in self.groups:
                            self.store_groups(plate[row][i])
                    else:
                        self.table.setItem(row, i, QTableWidgetItem(""))

# Initialization and setup methods

    def setup_expr_selection(self):
        self.select_facs.setChecked(True)
        components.add_button(self.expr_button_group, self.select_facs, self.select_elisa, self.select_qpcr)
        components.add_to_box_layout(self.side_layout, self.select_elisa, self.select_qpcr, self.select_facs)

    def setup_window(self):
        self.resize(1112, 450)
        self.setWindowTitle("Plate Plotter")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.input_box = components.create_input_box(self.input_box, "Enter group name")

    def save_expr_to_robot(self):
        saved_path = self.save_and_quit()
        success = self.copy_file_to_robot(saved_file_path=saved_path, expr_type=self.expr_button_group.checkedButton().text())
        if success:
            reply = QMessageBox.question(self, 'Done plotting?', "Press yes to quit or no to continue ",
                                         QMessageBox.No, QMessageBox.Yes)
            if reply == "Yes":
                self.quit_app()
            else:
                self.reset_plate()
        else:
            QMessageBox.about(self, 'Connection problem',
                                       'Try again. If the problem persists, check connection with Opentrons app'
                                 )

    def copy_file_to_robot(self, saved_file_path, expr_type: str):
        robot = connect_to_robot.OT2Connect(local_path=saved_file_path, file_name=os.path.split(saved_file_path)[-1],
                                            expr_type=expr_type)
        if robot.connection is not None:
            robot.save_file_to_robot()
            return True

        else:
            # Should address this with a small popup
            return False



    def init_plate(self):
        self.table = components.setup_table(self.table)



    def create_window(self):
        self.table_layout.addWidget(self.table, stretch=0)
        components.add_to_box_layout(self.side_layout, self.clear_cells_button, self.done_button, self.robot_save,
                                     self.load_map_button, self.box_label, self.input_box, self.enter_button,
                                     alignment=Qt.AlignBottom)
        self.main_layout.addLayout(self.side_layout, stretch=15)
        self.main_layout.addLayout(self.table_layout, stretch=85)
        self.main_widg.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widg)

# Cell modification methods
    def clear_cells(self):
        for i in self.table.selectedItems():
            i.setText('')

    def deselect(self):
        self.table = actions.deselect_boxes(self.table)

    # if cell has items and is clicked, delete them
    # if cell is empty, populate with text from selected button
    def fill_cells(self, items):
        for i in items:
            # Fill and remove TableWidgetItem objects rather than fill text
            if self.table.item(*i) is None:
                filler = QTableWidgetItem(self.group_button_group.checkedButton().text())
                self.table.setItem(*i, filler)
            else:
                self.table.item(*i).setText(self.group_button_group.checkedButton().text())
                self.table_layout.update()
        self.table.clearSelection()

    def entry_done(self):
        self.input_box.returnPressed.connect(lambda: self.store_groups(self.input_box.text()))
        self.enter_button.clicked.connect(lambda: self.store_groups(self.input_box.text()))

# data storage and export
    def save_and_quit(self):
        path, _ = QFileDialog.getSaveFileName(self)
        if path != "" and path is not None:
            data = []
            for row in range(self.table.rowCount()):
                rows = []
                for col in range(self.table.columnCount()):
                    to_save = self.table.item(row, col)
                    if to_save is not None:
                        rows.append(to_save.text())
                    else:
                        rows.append("")
                data.append(rows)
    #   else statement
            df = pd.DataFrame(data, index=pd.Index(list('ABCDEFGH')), columns=range(1, 13))
            df.to_csv(path)
            self.save_path = path
        return path

# Update and store user entered data
    def store_groups(self, group):
        if group not in self.groups:
            self.box_label.setText("")
            if group.strip() != '':
                self.groups.append(group.lstrip().rstrip())
                self.add_checkbox()
                self.input_box.clear()
        else:
            self.box_label.setText("That group already exists")

    def add_checkbox(self):
        button = QRadioButton(self.groups[-1])
        self.group_buttons.append(button)
        self.group_button_group.addButton(button)
        self.side_layout.addWidget(button)

    def reset_plate(self):
        self.table.clear()
        # self.side_layout.removeWidget(self.group_button_group.buttons()[0])
        [i.close() for i in self.group_button_group.buttons()]
        self.groups.clear()
        self.update()


    def init_toolbar(self):
        pass

    # def table_click(self):
    #     print(self.table.currentColumn(), self.table.currentRow())

    def select_group(self):
        checked = self.group_button_group.checkedButton().text()
        selections = [(i.row(), i.column()) for i in self.table.selectedIndexes()]
        # checked ends up
        # TODO: check replacing list comprehension in generators. Generators are better if idxing not necessary
        self.groups_dict.update({'{}'.format(checked): selections})
        self.fill_cells(selections)

    def quit_app(self):
        sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plate = platePlot()
    plate.show()
    if plate is not None:
        sys.exit(app.exec_())

