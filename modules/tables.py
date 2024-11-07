import sqlite3
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QWidget, QHBoxLayout, QPushButton, QTableWidgetItem, QHeaderView, \
    QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import uic

class Tables:
    def __init__(self):
        # Placeholder for UI elements
        self.table_name_input = None
        self.table_list_widget = None
        self.table_table_widget = None
        self.update_dialog = None  # Dialog for updating tables
        self.table_id_to_update = None  # Store ID of table to update

    def set_ui_elements(self, table_name_input, table_list_widget, table_table_widget):
        """Set UI elements so we can interact with them from this class."""
        self.table_name_input = table_name_input
        self.table_list_widget = table_list_widget
        self.table_table_widget = table_table_widget

    def saveTable(self):
        """Save the table to the database."""
        table_name = self.table_name_input.text() if self.table_name_input else ""

        if table_name:
            connection = sqlite3.connect("db/database.db")
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS shop_tables (
                                table_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                table_name TEXT UNIQUE NOT NULL
                              )''')

            try:
                cursor.execute("INSERT INTO shop_tables (table_name) VALUES (?)", (table_name,))
                connection.commit()
                self.loadTableTable()
                self.loadTableList()
                print("Table saved:", table_name)
            except sqlite3.IntegrityError:
                print("Table already exists.")
            finally:
                connection.close()
        else:
            print("Table name is empty.")

    def fetch_tables(self):
        """Fetch tables from the database."""
        connection = sqlite3.connect("db/database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM shop_tables")
        tables = cursor.fetchall()
        connection.close()
        return tables

    def loadTableList(self):
        """Load tables into the QListWidget with styling."""
        tables = self.fetch_tables()
        self.table_list_widget.clear()

        for table_name in tables:
            item_text = f"{table_name[1]}"
            item = QListWidgetItem()
            icon = QIcon("icon/table.png")  # Replace with your icon file
            item.setIcon(icon)
            item.setText(item_text)
            self.table_list_widget.setIconSize(QSize(64, 64))
            self.table_list_widget.addItem(item)

    def loadTableTable(self):
        """Load tables into QTableWidget with action buttons."""
        tables = self.fetch_tables()
        self.table_table_widget.clearContents()
        self.table_table_widget.setAlternatingRowColors(True)
        self.table_table_widget.setColumnCount(3)
        self.table_table_widget.setHorizontalHeaderLabels(("#", "Name", "Action"))

        # Column setup
        self.table_table_widget.setColumnWidth(0, 5)
        self.table_table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_table_widget.verticalHeader().setVisible(False)
        self.table_table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.table_table_widget.setRowCount(0)

        for inx, table in enumerate(tables):
            cell_widget = QWidget()
            layout = QHBoxLayout(cell_widget)

            editBtn = QPushButton(self.table_table_widget)
            editBtn.setIcon(QIcon("icon/edit.png"))
            editBtn.setFixedWidth(30)

            deleteBtn = QPushButton(self.table_table_widget)
            deleteBtn.setIcon(QIcon("icon/delete.png"))
            deleteBtn.setFixedWidth(30)

            # Connect buttons to handlers with table ID
            editBtn.clicked.connect(lambda checked, table_id=table[0]: self.showUpdateDialog(table_id))
            deleteBtn.clicked.connect(lambda checked, table_id=table[0]: self.handleDelete(table_id))

            layout.addWidget(editBtn)
            layout.addWidget(deleteBtn)
            layout.setContentsMargins(0, 0, 0, 0)
            cell_widget.setLayout(layout)

            # Insert new row and add data
            self.table_table_widget.insertRow(inx)
            self.table_table_widget.setItem(inx, 0, QTableWidgetItem(str(table[0])))
            self.table_table_widget.setItem(inx, 1, QTableWidgetItem(str(table[1])))
            self.table_table_widget.setCellWidget(inx, 2, cell_widget)

    def showUpdateDialog(self, table_id):
        """Display the update dialog and load the selected table's name."""
        self.table_id_to_update = table_id
        self.updateDialog = QDialog()
        uic.loadUi('ui/table_update.ui', self.updateDialog)  # Load the update UI

        # Find and populate the table_update_input field
        table_name = self.getTableName(table_id)
        self.updateDialog.table_update_input.setText(table_name)

        # Connect the update button
        self.updateDialog.table_update_btn.clicked.connect(self.updateTable)

        # Show the dialog
        self.updateDialog.exec_()

    def getTableName(self, table_id):
        connection = sqlite3.connect("db/database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT table_name FROM shop_tables WHERE table_id = ?", (table_id,))
        table_name = cursor.fetchone()[0]
        connection.close()
        return table_name

    def updateTable(self):
        new_name = self.updateDialog.table_update_input.text()
        print(new_name)

        if new_name:
            connection = sqlite3.connect("db/database.db")
            cursor = connection.cursor()
            cursor.execute("UPDATE shop_tables SET table_name = ? WHERE table_id = ?", (new_name, self.table_id_to_update))
            connection.commit()
            connection.close()

            print(f"Table ID {self.table_id_to_update} updated to {new_name}")
            self.updateDialog.accept()  # Close the dialog

            # Refresh the list and table
            self.loadTableList()
            self.loadTableTable()
        else:
            print("New table name is empty.")

    def deleteTable(self, table_id):
        """Delete a table from the database by its ID."""
        connection = sqlite3.connect("db/database.db")
        cursor = connection.cursor()

        # Confirm deletion
        cursor.execute("DELETE FROM shop_tables WHERE table_id = ?", (table_id,))
        connection.commit()
        connection.close()
        print(f"Table with ID {table_id} deleted.")

    def handleDelete(self, table_id):
        """Handle delete action for a table."""
        # Show a confirmation dialog
        reply = QMessageBox.question(
            None,
            "Delete Table",
            "Are you sure you want to delete this table?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.deleteTable(table_id)
            # Refresh the list and table after deletion
            self.loadTableList()
            self.loadTableTable()
