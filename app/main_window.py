import os
import sys
# from fbs_runtime.application_context.PyQt5 import ApplicationContext

from PyQt5.Qt import QApplication, QButtonGroup, QTableWidget, QVBoxLayout, QLineEdit, QMainWindow, QHBoxLayout,\
    QLabel, QWidget, QAbstractItemView, QActionGroup, QTableWidgetItem, QFileDialog, \
    QMessageBox, Qt, QHeaderView, QAction
from PyQt5 import QtGui, QtWidgets
from app import connect_to_robot
from app import components, actions



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
        checks = components.make_buttons('check', 'ELISA', 'qPCR', 'FACS')
        self.select_elisa, self.select_facs, self.select_qpcr = checks
        buttons = components.make_buttons('push', 'Save to robot', 'Save', 'Load a map', 'Clear', 'Enter')
        self.robot_save, self.done_button, self.load_map_button, self.clear_cells_button, self.enter_button = buttons
        self.table.setSelectionMode(QAbstractItemView.MultiSelection)
        self.group_button_group.setExclusive(True)
        #
        # Init plate stuff
        self.setup_window()
        self.setup_expr_selection()
        self.init_plate()
        self.create_window()
        #
        # signals and actions
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
        if plate_path != '':
            plate = actions.file_handler(plate_path, self.table, write=False)
            for y, row in enumerate(plate):
                for x, well in enumerate(row):
                    if well.strip():
                        self.table.setItem(y, x, QTableWidgetItem(well))
                        if well not in self.groups:
                            self.store_groups(well)
                    else:
                        self.table.setItem(y, x, QTableWidgetItem(""))
        else:
            pass


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

    def init_plate(self):
        self.table = components.setup_table(self.table)

# robot stuff

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
                              "Try again. If the problem persists, check connection with Opentrons app")

    def copy_file_to_robot(self, saved_file_path, expr_type: str):
        robot = connect_to_robot.OT2Connect(local_path=saved_file_path, file_name=os.path.split(saved_file_path)[-1],
                                            expr_type=expr_type)
        if robot.connection is not None:
            robot.save_file_to_robot()
            return True

        else:
            # Should address this with a small popup
            return False

    def create_window(self):
        self.table_layout.addWidget(self.table, stretch=0)
        components.add_to_box_layout(self.side_layout, self.clear_cells_button, self.done_button, self.robot_save,
                                     self.load_map_button, self.box_label, self.input_box, self.enter_button,
                                     alignment=Qt.AlignBottom)
        components.add_to_box_layout(self.main_layout, self.side_layout, alignment=None, stretch=15)
        components.add_to_box_layout(self.main_layout, self.table_layout, alignment=None, stretch=85)
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
        actions.fill_cells(items=items, table=self.table, button_group=self.group_button_group)

    def entry_done(self):
        self.input_box.returnPressed.connect(lambda: self.store_groups(self.input_box.text()))
        self.enter_button.clicked.connect(lambda: self.store_groups(self.input_box.text()))

# data storage and export
    def save_and_quit(self):
        path, _ = QFileDialog.getSaveFileName(self)
        self.save_path = actions.file_handler(path=path, table=self.table, write=True)
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
        buttons = components.make_buttons('radio', self.groups[-1])
        self.group_buttons.append(buttons)  # might not need this self var
        components.add_button(self.group_button_group, *buttons)
        components.add_to_box_layout(self.side_layout, *buttons)

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
        QtWidgets.qApp.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app = ApplicationContext()
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), '../resources/smiley.jpg')
    # app.setWindowIcon(QtGui.QIcon(path))
    # app.setApplicationName('Pl8 Plo0t3r')
    # app.setApplicationDisplayName('Pl8 Plo0t3r')
    #
    # app.applicationDisplayName()
    plate = platePlot()
    plate.setWindowIcon(QtGui.QIcon(path))
    plate.show()
    plate.raise_()
    if plate is not None:
        # sys.exit(app.exec_())
        sys.exit(app.exec_())

