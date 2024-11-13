import sqlite3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QWidget, QHBoxLayout, QPushButton, QTableWidgetItem, QHeaderView, \
QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import uic


class CreateOrder:
    def __init__(self):
        # Placeholder for UI elements
        self.category_name_input = None
        self.category_list_widget = None
        self.category_table_widget = None
        self.update_dialog = None  # Dialog for updating category
        self.category_id_to_update = None  # Store ID of category to update

    def showUpdateDialog(self):
        self.create_order_dialog = QDialog()
        uic.loadUi('ui/create_order.ui', self.create_order_dialog)
        self.create_order_dialog.exec_()