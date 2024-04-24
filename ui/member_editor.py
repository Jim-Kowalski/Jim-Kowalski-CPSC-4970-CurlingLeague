from model.custom_exceptions import DuplicateEmail
from model.team_member import TeamMember
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from ui.ui_base import UIBase

UI_MemberEditorWindow, QtBaseWindow = uic.loadUiType("member_editor.ui")



class MemberEditorWindow(UI_MemberEditorWindow, QtBaseWindow, UIBase):
    closed = pyqtSignal()
    update_mode = False
    member_to_update = None

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
        
    def __init__(self, team, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self._team = team

        if team:
            self.setWindowTitle(f"Editing team: {team.name}")

        # setup the table widget
        super().initialize_table_widget(self.member_table_widget, ["OID", "Member Name", "Member Email"])

        #Connect button signals to slots
        self.member_table_widget.itemSelectionChanged.connect(self.on_selection_changed)
        self.add_save_member_button.clicked.connect(self.add_save_member_button_clicked)
        self.delete_member_button.clicked.connect(self.delete_member_button_clicked)
        self.update_member_button.clicked.connect(self.update_member_button_clicked)

        self.refresh_member_list()

        #On __init__ set the selected row to the first row in the grid
        if self.member_table_widget.rowCount() > 0:
            self.member_table_widget.setCurrentCell(0, 0)



    def set_update_button_state(self):
        selected_items = self.member_table_widget.selectedItems()
        if selected_items:
            self.update_member_button.setEnabled(not self.update_mode)
        else:
            self.update_member_button.setEnabled(False)

    def on_selection_changed(self):
        self.set_update_button_state()


    def update_member_button_clicked(self):
        self.member_to_update = self.get_member_from_selected_row()
        if self.member_to_update:
            self.member_name_line_edit.setText(self.member_to_update.name)
            self.member_email_line_edit.setText(self.member_to_update.email)
            self.update_mode = True
            self.set_update_mode_UI(True)

    def set_update_mode_UI(self, state):
        self.add_save_member_button.setText("Save Member" if state else "Add Member")
        self.delete_member_button.setEnabled(not state)
        self.member_table_widget.setEnabled(not state)
        self.set_update_button_state()

    def add_save_member_button_clicked(self):
        member_name = self.member_name_line_edit.text()
        member_email = self.member_email_line_edit.text()
        reset_update_ui = False
        if self.update_mode:
            if self.member_to_update:
                try:
                    for team_member in self._team.members:
                        if team_member != self.member_to_update:
                            if team_member.email.lower() == member_email.lower():
                                raise DuplicateEmail(member_email)

                    self.member_to_update.name = member_name
                    self.member_to_update.email = member_email
                    reset_update_ui =True
                except DuplicateEmail:
                    dialog = QMessageBox(QMessageBox.Icon.Critical,
                                         "Error! Duplicate email address!",
                                         f"Another team member has the same email address: {member_email}",
                                         QMessageBox.StandardButton.Ok)
                    result = dialog.exec()
                    self.member_email_line_edit.selectAll()
                    self.member_email_line_edit.setFocus()
            else:
                reset_update_ui = True

            if reset_update_ui:
                self.update_mode = False
                self.set_update_mode_UI(False)
                self.refresh_member_list()

                super().select_row_by_oid(self.member_table_widget,self.member_to_update.oid)

                self.member_name_line_edit.clear()
                self.member_email_line_edit.clear()
                self.member_table_widget.setFocus()

        else:
            member = self._team.member_named(member_name)
            if not member:
                # Find a free oid from the list of teams
                new_oid = self._team.find_free_member_oid()
                # instantiate a new member using the free oid and email
                new_team_member = TeamMember(new_oid, member_name, member_email)

                try:
                    self._team.add_member(new_team_member)
                    super().add_item_to_table_widget(self.member_table_widget, new_team_member, new_team_member.email)
                    super().select_row_by_oid(self.member_table_widget, new_oid)
                    # clear member_name_line_edit & member_email_line_edit
                    # and set focus to member_name_line_edit
                    self.member_name_line_edit.clear()
                    self.member_email_line_edit.clear()
                    self.member_table_widget.setFocus()

                except DuplicateEmail:
                    dialog = QMessageBox(QMessageBox.Icon.Critical,
                                         "Error! Duplicate email address!",
                                         f"Cannot add team member. Email in use: {member_email}",
                                         QMessageBox.StandardButton.Ok)
                    result = dialog.exec()
                    self.member_email_line_edit.selectAll()
                    self.member_email_line_edit.setFocus()

    def delete_member_button_clicked(self):
        member = self.get_member_from_selected_row()
        if member:
            # --------------------------------------------------------
            # Create a confirmation dialog before deleting the member.
            # --------------------------------------------------------
            dialog = QMessageBox()
            dialog.setWindowTitle("Remove team?")
            dialog.setText(f"Are you sure you want to remove member: {member.name} <{member.email}>?")
            dialog.setIcon(QMessageBox.Icon.Question)
            no_button = dialog.addButton("No", QMessageBox.ButtonRole.RejectRole)
            yes_button = dialog.addButton("Yes", QMessageBox.ButtonRole.AcceptRole)
            dialog.exec()
            if dialog.clickedButton()==yes_button:
                self._team.remove_member(member)
                self.refresh_member_list()

    def get_member_from_selected_row(self):
        selected_items = self.member_table_widget.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            # Get the name of the league from the selected row
            item_member_name = self.member_table_widget.item(selected_row, 1)
            if item_member_name:
                selected_member_name = item_member_name.text()
                member = self._team.member_named(selected_member_name)
                return member
        return None

    def refresh_member_list(self):
        self.member_table_widget.setRowCount(0)
        for member in self._team.members:
            super().add_item_to_table_widget(self.member_table_widget, member, member.email)
        self.member_table_widget.sortItems(0)
        self.member_table_widget.resizeColumnsToContents()  # Resizes the table to its contents

