from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget
class UIBase:

    def get_oid_from_selected_row(self, table_widget):
        selected_items = table_widget.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            item_oid = table_widget.item(selected_row, 0)
            if item_oid:
                return item_oid.text()
        return -1

    def initialize_table_widget(self, table_widget, horiz_labels):
        table_widget.setColumnCount(3)
        table_widget.setHorizontalHeaderLabels(horiz_labels) #["OID", "League Name", "Number of Teams"]
        table_widget.resizeColumnsToContents() #Resizes the table to its contents
        table_widget.verticalHeader().setVisible(False) # turn off the vertical header showing the row number
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable editing

    def select_row_by_oid(self, table_widget, oid):
        for row in range(table_widget.rowCount()):
            oid_item = table_widget.item(row, 0)
            if oid_item:
                # Access the text value of the QTableWidgetItem
                current_oid = int(oid_item.text())
                if current_oid==oid:
                    table_widget.setCurrentCell(row, 0)
                    return
            

    def add_item_to_table_widget(self, table_widget, new_item, custom_item):
        """
        This function adds the specified item to the given table_widget
        :param table_widget: Specifies the QTableWidget object
        :param new_item: Specifies the item to be added (League or Team object)
        :return: None
        """
        row_count = table_widget.rowCount()  # get the number of rows in the QTableWidget
        table_widget.insertRow(row_count)  # create a new row based on the number of rows in the QTableWidget
        table_widget.setItem(row_count, 0, QTableWidgetItem(str(new_item.oid)))  # Set the OID
        table_widget.setItem(row_count, 1, QTableWidgetItem(new_item.name))  # Set the name
        table_widget.setItem(row_count, 2, QTableWidgetItem(custom_item))  # Set the editor specific item
        table_widget.setCurrentCell(row_count, 0)  # Select the row that was added
        table_widget.sortItems(0)  # Sort the items based on OID (just to keep things sorted)
        table_widget.resizeColumnsToContents()  # Resizes the table to its contents