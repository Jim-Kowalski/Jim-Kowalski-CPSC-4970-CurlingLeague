import sys
from model.league import League
from model.team import Team
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt
from ui.member_editor import MemberEditorWindow
from ui.ui_base import UIBase

UI_LeagueEditorWindow, QtBaseWindow = uic.loadUiType("league_editor.ui")


class LeagueEditorWindow(UI_LeagueEditorWindow, QtBaseWindow, UIBase):
    closed = pyqtSignal()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

    def __init__(self, league, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self._league = league

        if league:
            self.setWindowTitle(f"Editing League: {league.name}")

        # setup the table widget
        super().initialize_table_widget(self.team_table_widget, ["OID", "Team Name", "Number of Players"])

        # # Connect the button clicked signals to slots.
        self.add_team_button.clicked.connect(self.add_team_button_clicked)
        self.edit_team_button.clicked.connect(self.edit_team_button_clicked)
        self.delete_team_button.clicked.connect(self.delete_team_button_clicked)

        # #Connect the menu item triggered signals to slots
        self.exit_menu_item.triggered.connect(self.exit_menu_item_triggered)
        self.import_team_menu_item.triggered.connect(self.import_team_menu_item_triggered)
        self.export_team_menu_item.triggered.connect(self.export_team_menu_item_triggered)
        self.refresh_team_list()

        # On __init__ set the selected row to the first row in the grid
        if self.team_table_widget.rowCount() > 0:
            self.team_table_widget.setCurrentCell(0, 0)

    def exit_menu_item_triggered(self):
        pass

    def import_team_menu_item_triggered(self):
        if self._league:
            file_dialog = QFileDialog()
            file_dialog.setNameFilter("Csv files (*.csv)")
            file_dialog.setViewMode(QFileDialog.Detail)
            if file_dialog.exec_():
                file_name = file_dialog.selectedFiles()[0]
                self._league.import_league_team(file_name)
        self.refresh_team_list()

    def export_team_menu_item_triggered(self):
        if self._league:
            team = self.get_team_from_selected_row()
            if team:
                file_dialog = QFileDialog()
                file_dialog.setNameFilter("CSV file (*.csv)")
                file_dialog.setViewMode(QFileDialog.Detail)
                file_dialog.setAcceptMode(QFileDialog.AcceptSave)
                if file_dialog.exec_():
                    file_name = file_dialog.selectedFiles()[0]
                    if not file_name.endswith(".csv"):
                        file_name += ".csv"
                    self._league.export_league_team(team, file_name)

    def add_team_button_clicked(self):
        # 1- get a unique oid
        # 2- Ensure the team name is unique.
        # Get the name of the league from the control.
        team_name = self.team_name_line_edit.text()

        team = self._league.team_named(team_name)

        if not team:
            # Find a free oid from the list of teams
            new_oid = self._league.find_free_team_oid()

            # instantiate a new team using the free oid and unique
            # team name.
            new_team = Team(new_oid, team_name)

            self._league.add_team(new_team)
            super().add_item_to_table_widget(self.team_table_widget, new_team, str(len(new_team.members)))
            super().select_row_by_oid(self.team_table_widget, new_oid)

            # clear league_name_line_edit and set focus
            self.team_name_line_edit.clear()
            self.team_table_widget.setFocus()

        else:
            # If the league is already present in the database, we
            # will not accept duplicate named leagues. So, display
            # a dialog, highlight the text in the league_name_line_edit
            # widget and set focus to it.
            dialog = QMessageBox(QMessageBox.Icon.Critical,
                                 "Error! Duplicate team name!",
                                 f"There is already a team named: '{team_name}'. Please pick a unique team name! ",
                                 QMessageBox.StandardButton.Ok)
            result = dialog.exec()
            self.team_name_line_edit.selectAll()
            self.team_name_line_edit.setFocus()

    def on_team_editor_closed(self):
        self.refresh_team_list()
        self.setEnabled(True)

    def edit_team_button_clicked(self):
        team = self.get_team_from_selected_row()
        if team:
            self.setEnabled(False)
            member_editor_window = MemberEditorWindow(team, self)
            member_editor_window.setWindowModality(Qt.ApplicationModal)
            member_editor_window.closed.connect(self.on_team_editor_closed)
            member_editor_window.show()

    def delete_team_button_clicked(self):

        team = self.get_team_from_selected_row()

        if team:
            # ------------------------------------------------------
            # Create a confirmation dialog before deleting the team.
            # ------------------------------------------------------
            dialog = QMessageBox()
            dialog.setWindowTitle("Remove team?")
            dialog.setText(f"Are you sure you want to remove team: {team.name}?")
            dialog.setIcon(QMessageBox.Icon.Question)
            no_button = dialog.addButton("No", QMessageBox.ButtonRole.RejectRole)
            yes_button = dialog.addButton("Yes", QMessageBox.ButtonRole.AcceptRole)
            dialog.exec()

            # If the end-user clicked yes to the dialog, delete the team out of the
            # league object and also remove the row.
            if dialog.clickedButton() == yes_button:
                self._league.remove_team(team)
                self.refresh_team_list()
            else:
                print("No pressed")

    def get_team_from_selected_row(self):
        selected_items = self.team_table_widget.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            # Get the name of the league from the selected row
            item_team_name = self.team_table_widget.item(selected_row, 1)
            if item_team_name:
                selected_team_name = item_team_name.text()
                team = self._league.team_named(selected_team_name)
                return team
        return None

    def refresh_team_list(self):
        """
        This function clears the rows in the league_table_widget and
        repopulates all the leagues in the league database
        :return: None
        """
        self.team_table_widget.setRowCount(0)
        for team in self._league.teams:
            super().add_item_to_table_widget(self.team_table_widget, team, str(len(team.members)))

        self.team_table_widget.sortItems(0)  # Sort items based on OID
        self.team_table_widget.resizeColumnsToContents()  # Resizes the table to its contents


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    _league = League(1, "MyLeague")

    window = LeagueEditorWindow(_league)
    window.show()
    sys.exit(app.exec_())
