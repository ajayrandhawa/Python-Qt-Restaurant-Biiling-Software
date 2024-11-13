import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QWidget, QVBoxLayout, QLabel, QComboBox, QListWidget
from PyQt5 import uic, QtWidgets


class CreateOrder:
    def __init__(self):
        self.create_order_dialog = QDialog()

        uic.loadUi('ui/create_order.ui', self.create_order_dialog)
        self.items_browser_list_widget = self.create_order_dialog.findChild(QtWidgets.QListWidget, 'itemsBrowserListWidget')

    def showDialog(self):
        self.create_order_dialog.show()
        self.loadItemsList()

    def loadItemsList(self, category_filter=None, search_term=None):

        if not self.items_browser_list_widget:
            print("List widget not initialized.")
            return

        self.items_browser_list_widget.clear()  # Clear existing items
        items = self.fetch_items(category_filter=category_filter, search_term=search_term)

        print(items)
        for index, (item_id, item_name, item_category, _, _, mtype) in enumerate(items):
            # Create item widget for each item
            item_widget = QWidget()
            item_layout = QVBoxLayout()

            # Set background color based on type (Veg/Non-Veg)
            background_color = "#D4F7C5" if mtype == "Veg" else "#FFD1D1"
            item_widget.setStyleSheet(f"background-color: {background_color}; border-radius: 10px;")

            # Item name label
            text_up_label = QLabel(item_name)
            text_up_label.setStyleSheet("font-size: 16px; color: #333; font-weight: bold;")
            text_up_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
            text_up_label.setWordWrap(True)
            text_up_label.setFixedWidth(100)
            text_up_label.setFixedHeight(150)

            # Item category label
            text_down_label = QLabel(item_category)
            text_down_label.setStyleSheet("font-size: 12px; color: #666;")
            text_down_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

            # Add labels to layout
            item_layout.addWidget(text_up_label)
            item_layout.addWidget(text_down_label)
            item_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
            item_widget.setLayout(item_layout)

            # Add item to the list widget
            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
            self.items_browser_list_widget.addItem(list_item)
            self.items_browser_list_widget.setItemWidget(list_item, item_widget)



    def fetch_items(self, category_filter=None, search_term=None):
        connection = sqlite3.connect("db/database.db")
        cursor = connection.cursor()

        # Use specific queries based on the filters
        if category_filter and search_term:
            # Both category and search term filters
            query = "SELECT * FROM items WHERE category = ? AND item_name LIKE ?"
            params = [category_filter, f"%{search_term}%"]
        elif category_filter:
            # Only category filter
            query = "SELECT * FROM items WHERE category = ?"
            params = [category_filter]
        elif search_term:
            # Only search term filter
            query = "SELECT * FROM items WHERE item_name LIKE ?"
            params = [f"%{search_term}%"]
        else:
            # No filters, fetch all items
            query = "SELECT * FROM items"
            params = []

        cursor.execute(query, params)
        items = cursor.fetchall()
        connection.close()
        return items
