import sqlite3
from traceback import print_exc

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QWidget, QHBoxLayout, QPushButton, QTableWidgetItem, QHeaderView, \
    QMessageBox, QVBoxLayout, QLabel, QListWidget
from PyQt5.QtGui import QIcon, QBrush, QColor, QPixmap
from PyQt5 import uic
from PyQt5.uic.properties import QtGui


class Items:
    def __init__(self):
        # Placeholder for UI elements
        self.items_name_input = None
        self.items_category_combo = None
        self.items_price_input = None
        self.items_description_input = None
        self.items_mtype_combo = None
        self.items_table_widget = None
        self.items_list_widget = None
        self.updateDialog = None  # Dialog for updating items
        self.item_id_to_update = None  # Store ID of item to update

    def set_ui_elements(self, items_name_input, items_category_combo, items_price_input, items_description_input, items_mtype_combo, items_table_widget, items_list_widget):
        """Set UI elements so we can interact with them from this class."""
        self.items_name_input = items_name_input
        self.items_category_combo = items_category_combo
        self.items_price_input = items_price_input
        self.items_description_input = items_description_input
        self.items_mtype_combo = items_mtype_combo
        self.items_table_widget = items_table_widget
        self.items_list_widget = items_list_widget


    def createItem(self):
        """Save the item to the database."""
        item_name = self.items_name_input.text() if self.items_name_input else ""
        category = self.items_category_combo.currentText() if self.items_category_combo else ""
        item_description = self.items_description_input.text() if self.items_description_input else ""
        item_price = self.items_price_input.text() if self.items_price_input else ""
        mtype = self.items_mtype_combo.currentText() if self.items_mtype_combo.currentText() else "Veg"

        if item_name:
            connection = sqlite3.connect("db/database.db")
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                item_name TEXT UNIQUE NOT NULL,
                                category TEXT NOT NULL,
                                item_description TEXT,
                                item_qty TEXT,
                                item_price TEXT,
                                mtype TEXT
                              )''')

            try:
                cursor.execute(
                    "INSERT INTO items (item_name, category, item_description, item_price, mtype) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (item_name, category, item_description, item_price, mtype))
                connection.commit()
                self.loadItemTable()
                self.loadItemsList()
            except sqlite3.IntegrityError:
                print("Item already exists.")
            finally:
                connection.close()
        else:
            print("Item name is empty.")

    def fetch_items(self):
        connection = sqlite3.connect("db/database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        connection.close()
        return items

    def loadItemsList(self):

        self.items_list_widget.clear()
        items = self.fetch_items()

        for index, (item_id, item_name, item_category, _, _, mtype) in enumerate(items):
            item_widget = QWidget()
            item_layout = QVBoxLayout()

            background_color = "#D4F7C5" if mtype == "Veg" else "#FFD1D1"
            item_widget.setStyleSheet(f"background-color: {background_color}; border-radius: 10px;")

            text_up_label = QLabel(item_name)
            text_up_label.setStyleSheet("font-size: 16px; color: #333; font-weight: bold;")
            text_up_label.setAlignment(Qt.AlignTop)
            text_up_label.setWordWrap(True)
            text_up_label.setFixedWidth(100)
            text_up_label.setFixedHeight(150)
            text_up_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

            text_down_label = QLabel(item_category)
            text_down_label.setStyleSheet("font-size: 12px; color: #666;")
            text_down_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

            item_layout.addWidget(text_up_label)
            item_layout.addWidget(text_down_label)
            item_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
            item_widget.setLayout(item_layout)

            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())

            self.items_list_widget.addItem(list_item)
            self.items_list_widget.setItemWidget(list_item, item_widget)

    def loadItemTable(self):
        items = self.fetch_items()

        self.items_table_widget.clearContents()
        self.items_table_widget.setAlternatingRowColors(True)
        self.items_table_widget.setColumnCount(6)
        self.items_table_widget.setHorizontalHeaderLabels(("#", "Name", "Category", "Price", "V/N", "Action"))

        # Column setup
        self.items_table_widget.setColumnWidth(0, 5)
        self.items_table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.items_table_widget.verticalHeader().setVisible(False)
        self.items_table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        self.items_table_widget.setRowCount(0)

        for inx, item in enumerate(items):
            cell_widget = QWidget()
            layout = QHBoxLayout(cell_widget)

            editBtn = QPushButton(self.items_table_widget)
            editBtn.setIcon(QIcon("icon/edit.png"))
            editBtn.setFixedWidth(30)

            deleteBtn = QPushButton(self.items_table_widget)
            deleteBtn.setIcon(QIcon("icon/delete.png"))
            deleteBtn.setFixedWidth(30)

            # Connect buttons to handlers with item ID
            editBtn.clicked.connect(lambda checked, item_id=item[0]: self.showUpdateDialog(item_id))
            deleteBtn.clicked.connect(lambda checked, item_id=item[0]: self.handleDelete(item_id))

            layout.addWidget(editBtn)
            layout.addWidget(deleteBtn)
            layout.setContentsMargins(0, 0, 0, 0)
            cell_widget.setLayout(layout)
            self.items_table_widget.insertRow(inx)
            self.items_table_widget.setItem(inx, 0, QTableWidgetItem(str(item[0])))
            self.items_table_widget.setItem(inx, 1, QTableWidgetItem(item[1]))
            self.items_table_widget.setItem(inx, 2, QTableWidgetItem(item[2]))
            self.items_table_widget.setItem(inx, 3, QTableWidgetItem(str(item[3])))
            self.items_table_widget.setItem(inx, 4, QTableWidgetItem(str(item[5])))
            self.items_table_widget.setCellWidget(inx, 5, cell_widget)

    def showUpdateDialog(self, item_id):
        self.item_id_to_update = item_id
        self.updateDialog = QDialog()
        uic.loadUi('ui/item_update.ui', self.updateDialog)  # Load the update UI

        item = self.getItemDetails(item_id)
        self.updateDialog.items_update_name_input.setText(item[1])
        self.updateDialog.items_update_price_input.setText(str(item[3]))
        self.updateDialog.items_update_description_input.setText(item[4])
        self.updateDialog.items_update_mtype_combo.setCurrentText(item[5])
        self.updateDialog.item_update_btn.clicked.connect(self.updateItem)
        self.load_categories_in_item_update(item[2])
        self.updateDialog.exec_()

    def getItemDetails(self, item_id):
        connection = sqlite3.connect("db/database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM items WHERE item_id = ?", (item_id,))
        item = cursor.fetchone()
        connection.close()
        return item

    def updateItem(self):
        """Update the item details in the database."""
        item_name = self.updateDialog.items_update_name_input.text()
        category = self.updateDialog.items_update_category_combo.currentText()
        item_description = self.updateDialog.items_update_description_input.text()
        item_price = self.updateDialog.items_update_price_input.text()
        mtype = self.updateDialog.items_update_mtype_combo.currentText()

        if item_name:
            connection = sqlite3.connect("db/database.db")
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE items SET item_name = ?, category = ?, item_description = ?, item_price = ?, mtype = ? WHERE item_id = ?",
                (item_name, category, item_description, item_price, mtype, self.item_id_to_update))
            connection.commit()
            connection.close()

            print(f"Item ID {self.item_id_to_update} updated.")
            self.updateDialog.accept()

            self.loadItemTable()
        else:
            print("Item name is empty.")

    def deleteItem(self, item_id):
        connection = sqlite3.connect("db/database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
        connection.commit()
        connection.close()
        print(f"Item with ID {item_id} deleted.")

    def handleDelete(self, item_id):
        reply = QMessageBox.question(
            None,
            "Delete Item",
            "Are you sure you want to delete this item?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.deleteItem(item_id)
            self.loadItemTable()
            self.loadItemsList()

    def fetch_all_categories(self):
        connection = sqlite3.connect("db/database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
        connection.close()
        return categories

    def load_categories_in_combo(self):
        categories = self.fetch_all_categories()
        self.items_category_combo.clear()
        for category in categories:
            self.items_category_combo.addItem(category[1], category[0])

    def load_categories_in_item_update(self, selected_category_name):
        categories = self.fetch_all_categories()
        self.updateDialog.items_update_category_combo.clear()
        for category in categories:
            self.updateDialog.items_update_category_combo.addItem(category[1])

        index = self.updateDialog.items_update_category_combo.findText(selected_category_name)
        if index != -1:
            self.updateDialog.items_update_category_combo.setCurrentIndex(index)