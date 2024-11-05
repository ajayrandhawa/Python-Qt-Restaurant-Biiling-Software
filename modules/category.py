import sqlite3
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QWidget, QHBoxLayout, QPushButton, QTableWidgetItem, QHeaderView, \
    QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import uic


class Category:
    def __init__(self):
        # Placeholder for UI elements
        self.category_name_input = None
        self.category_list_widget = None
        self.category_table_widget = None
        self.update_dialog = None  # Dialog for updating category
        self.category_id_to_update = None  # Store ID of category to update

    def set_ui_elements(self, category_name_input, category_list_widget, category_table_widget):
        """Set UI elements so we can interact with them from this class."""
        self.category_name_input = category_name_input
        self.category_list_widget = category_list_widget
        self.category_table_widget = category_table_widget

    def saveCategory(self):
        """Save the category to the database."""
        category_name = self.category_name_input.text() if self.category_name_input else ""

        if category_name:
            connection = sqlite3.connect("db/database.db")
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS category (
                                catgeory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                category_name TEXT UNIQUE NOT NULL
                              )''')

            try:
                cursor.execute("INSERT INTO category (category_name) VALUES (?)", (category_name,))
                connection.commit()
                self.loadCategoryTable()
                self.loadCategoryList()
                print("Category saved:", category_name)
            except sqlite3.IntegrityError:
                print("Category already exists.")
            finally:
                connection.close()
        else:
            print("Category name is empty.")

    def fetch_categories(self):
        """Fetch categories from the database."""
        connection = sqlite3.connect("db/database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
        connection.close()
        return categories

    def loadCategoryList(self):
        """Load categories into the QListWidget with styling."""
        categories = self.fetch_categories()
        self.category_list_widget.clear()

        for category_name in categories:
            item_text = f"{category_name[1]}"
            item = QListWidgetItem()
            item.setText(item_text)
            self.category_list_widget.addItem(item)

    def loadCategoryTable(self):
        """Load categories into QTableWidget with action buttons."""
        categories = self.fetch_categories()
        self.category_table_widget.clearContents()
        self.category_table_widget.setAlternatingRowColors(True)
        self.category_table_widget.setColumnCount(3)
        self.category_table_widget.setHorizontalHeaderLabels(("#", "Name", "Action"))

        # Column setup
        self.category_table_widget.setColumnWidth(0, 5)
        self.category_table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.category_table_widget.verticalHeader().setVisible(False)

        self.category_table_widget.setRowCount(0)

        for inx, category in enumerate(categories):
            cell_widget = QWidget()
            layout = QHBoxLayout(cell_widget)

            editBtn = QPushButton(self.category_table_widget)
            editBtn.setIcon(QIcon("icon/edit.png"))
            editBtn.setFixedWidth(30)

            deleteBtn = QPushButton(self.category_table_widget)
            deleteBtn.setIcon(QIcon("icon/delete.png"))
            deleteBtn.setFixedWidth(30)

            # Connect buttons to handlers with category ID
            editBtn.clicked.connect(lambda checked, category_id=category[0]: self.showUpdateDialog(category_id))
            deleteBtn.clicked.connect(lambda checked, category_id=category[0]: self.handleDelete(category_id))

            layout.addWidget(editBtn)
            layout.addWidget(deleteBtn)
            layout.setContentsMargins(0, 0, 0, 0)
            cell_widget.setLayout(layout)

            # Insert new row and add data
            self.category_table_widget.insertRow(inx)
            self.category_table_widget.setItem(inx, 0, QTableWidgetItem(str(category[0])))
            self.category_table_widget.setItem(inx, 1, QTableWidgetItem(str(category[1])))
            self.category_table_widget.setCellWidget(inx, 2, cell_widget)

    def showUpdateDialog(self, category_id):
        """Display the update dialog and load the selected category's name."""
        self.category_id_to_update = category_id
        self.updateDialog = QDialog()
        uic.loadUi('ui/category_update.ui', self.updateDialog)  # Load the update UI

        # Find and populate the category_update_input field
        category_name = self.getCategoryName(category_id)
        self.updateDialog.category_update_input.setText(category_name)

        # Connect the update button
        self.updateDialog.category_update_btn.clicked.connect(self.updateCategory)

        # Show the dialog
        self.updateDialog.exec_()

    def getCategoryName(self, category_id):
        connection = sqlite3.connect("db/database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT category_name FROM category WHERE category_id = ?", (category_id,))
        category_name = cursor.fetchone()[0]
        connection.close()
        return category_name

    def updateCategory(self):
        new_name = self.updateDialog.category_update_input.text()
        print(new_name)

        if new_name:
            connection = sqlite3.connect("db/database.db")
            cursor = connection.cursor()
            cursor.execute("UPDATE category SET category_name = ? WHERE category_id = ?", (new_name, self.category_id_to_update))
            connection.commit()
            connection.close()

            print(f"Category ID {self.category_id_to_update} updated to {new_name}")
            self.updateDialog.accept()  # Close the dialog

            # Refresh the list and table
            self.loadCategoryList()
            self.loadCategoryTable()
        else:
            print("New category name is empty.")

    def deleteCategory(self, category_id):
        """Delete a category from the database by its ID."""
        connection = sqlite3.connect("db/database.db")
        cursor = connection.cursor()

        # Confirm deletion
        cursor.execute("DELETE FROM category WHERE category_id = ?", (category_id,))
        connection.commit()
        connection.close()
        print(f"Category with ID {category_id} deleted.")

    def handleDelete(self, category_id):
        """Handle delete action for a category."""
        # Show a confirmation dialog
        reply = QMessageBox.question(
            None,
            "Delete Category",
            f"Are you sure you want to delete category",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.deleteCategory(category_id)
            # Refresh the list and table after deletion
            self.loadCategoryList()
            self.loadCategoryTable()
