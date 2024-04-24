import sys
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from model.league import League
from model.league_database import LeagueDatabase
from model.custom_exceptions import DuplicateOid
from ui.ui_base import UIBase
from ui.league_editor import LeagueEditorWindow

UI_MainWindow, QtBaseWindow = uic.loadUiType("main.ui")


class MainWindow(UI_MainWindow, QtBaseWindow, UIBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.db = LeagueDatabase.instance()

        # set up the table widget
        super().initialize_table_widget(self.league_table_widget, ["OID", "League Name", "Number of Teams"])

        # Connect the button clicked signals to slots.
        self.add_league_button.clicked.connect(self.add_league_button_clicked)
        self.edit_league_button.clicked.connect(self.edit_league_button_clicked)
        self.delete_league_button.clicked.connect(self.delete_league_button_clicked)

        # Connect the menu item triggered signals to slots
        self.quit_menu_item.triggered.connect(self.quit_menu_item_triggered)
        self.save_menu_item.triggered.connect(self.save_menu_item_triggered)
        self.load_menu_item.triggered.connect(self.load_menu_item_triggered)

        # On __init__ set the selected row to the first row in the grid
        if self.league_table_widget.rowCount() > 0:
            self.league_table_widget.setCurrentCell(0, 0)

    # --------------------------------------------------------------------------
    # QPushbutton slot methods
    # --------------------------------------------------------------------------
    def add_league_button_clicked(self):
        """
        This function handles the add_league_button QPushbutton Click() signal
        :return: None
        """
        try:
            # Get the name of the league from the control.
            league_name = self.league_name_line_edit.text()

            # Determine if there is a duplicate league with the
            # same name.
            league = self.db.league_named(league_name)

            # If the league name is unique, proceed to adding the
            # league to the database.
            if not league:

                # Find a free oid from the database
                new_oid = self.db.find_free_league_oid()

                # instantiate a new league using the free oid and the
                # unique league name.
                new_league = League(new_oid, league_name)

                # add the league to the database and add the league to
                # the widget
                self.db.add_league(new_league)

                super().add_item_to_table_widget(self.league_table_widget, new_league, str(len(new_league.teams)))
                super().select_row_by_oid(self.league_table_widget, new_oid)

                # clear league_name_line_edit and set focus
                self.league_name_line_edit.clear()
                self.league_name_line_edit.setFocus()

            else:
                # If the league is already present in the database, we
                # will not accept duplicate named leagues. So, display
                # a dialog, highlight the text in the league_name_line_edit
                # widget and set focus to it.
                dialog = QMessageBox(QMessageBox.Icon.Critical,
                                     "Error! Duplicate league!",
                                     f"There is already a league named: '{league_name}'. Please pick a unique league "
                                     f"name! ",
                                     QMessageBox.StandardButton.Ok)
                result = dialog.exec()
                self.league_name_line_edit.selectAll()
                self.league_name_line_edit.setFocus()

        except DuplicateOid:
            # this should not happen since we are finding an OID
            # however, if for some odd reason it does occur, it is
            # being handled.
            self.show_duplicate_oid_message_box(
                f"League OID '{self.oid_spin_box.value()}' already used. Please choose a different OID.")

    def on_league_editor_closed(self):
        self.refresh_league_list()
        self.setEnabled(True)

    def edit_league_button_clicked(self):
        league = self.get_league_from_selected_row()
        if league:
            self.setEnabled(False)
            league_editor_window = LeagueEditorWindow(league, self)
            league_editor_window.setWindowModality(Qt.ApplicationModal)
            league_editor_window.closed.connect(self.on_league_editor_closed)
            league_editor_window.show()

    def delete_league_button_clicked(self):
        """
        This function returns the League object
        :return:
        """
        league = self.get_league_from_selected_row()

        if league:
            # ------------------------------------------------------
            # Create a confirmation dialog before deleting the team.
            # ------------------------------------------------------
            dialog = QMessageBox()
            dialog.setWindowTitle("Remove league?")
            dialog.setText(f"Are you sure you want to remove league: {league.name}?")
            dialog.setIcon(QMessageBox.Icon.Question)
            no_button = dialog.addButton("No", QMessageBox.ButtonRole.RejectRole)
            yes_button = dialog.addButton("Yes", QMessageBox.ButtonRole.AcceptRole)
            dialog.exec()

            # If the end-user clicked yes to the dialog, delete the league out of the
            # database and also remove the row.
            if dialog.clickedButton() == yes_button:
                self.db.remove_league(league)
                self.refresh_league_list()
            else:
                print("No pressed")

    def get_league_from_selected_row(self):
        selected_items = self.league_table_widget.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            # Get the name of the league from the selected row
            item_league_name = self.league_table_widget.item(selected_row, 1)
            if item_league_name:
                selected_league_name = item_league_name.text()
                league = self.db.league_named(selected_league_name)
                return league
        return None

    def show_duplicate_oid_message_box(self, text):
        """
        This function instantiates a QMessageBox displaying
        that there is a duplicate OID.
        :param text: Specifies a custom message to display
        :return: None
        """
        dialog = QMessageBox(QMessageBox.Icon.Critical,
                             "Duplicate OID",
                             text,
                             QMessageBox.StandardButton.Ok)
        result = dialog.exec()

    def refresh_league_list(self):
        """
        This function clears the rows in the league_table_widget and
        repopulates all the leagues in the league database
        :return: None
        """
        self.league_table_widget.setRowCount(0)
        for league in self.db.leagues:
            super().add_item_to_table_widget(self.league_table_widget, league, str(len(league.teams)))

        self.league_table_widget.sortItems(0)
        self.league_table_widget.resizeColumnsToContents()  # Resizes the table to its contents

    # --------------------------------------------------------------------------
    # MENU Item Trigger slots
    # --------------------------------------------------------------------------
    def quit_menu_item_triggered(self):
        sys.exit(app.exec_())

    def save_menu_item_triggered(self):
        if self.db:
            file_dialog = QFileDialog()
            file_dialog.setNameFilter("Pickle files (*.pkl)")
            file_dialog.setViewMode(QFileDialog.Detail)
            file_dialog.setAcceptMode(QFileDialog.AcceptSave)
            if file_dialog.exec_():
                file_name = file_dialog.selectedFiles()[0]
                if not file_name.endswith(".pkl"):
                    file_name += ".pkl"
                self.db.save(file_name)

    def load_menu_item_triggered(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Pickle files (*.pkl)")
        file_dialog.setViewMode(QFileDialog.Detail)
        if file_dialog.exec_():
            file_name = file_dialog.selectedFiles()[0]
            self.db.load(file_name)
            self.db = LeagueDatabase.instance()
            self.refresh_league_list()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
