from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QWidget, QHBoxLayout, QPushButton, QTableWidgetItem, \
    QHeaderView
from PyQt5 import uic

#Modules
from modules.category import Category


class Dashboard(QMainWindow):
    def __init__(self):
        super(Dashboard, self).__init__()
        uic.loadUi('ui/dashboard.ui', self)  # Load the dashboard UI
        self.showMaximized()

        # Initialize Category class instance
        self.category_manager = Category()

        # Connect add_category_btn to the saveCategory method in Category
        self.add_category_btn.clicked.connect(self.category_manager.saveCategory)
        self.category_manager.set_ui_elements(self.category_name_input)
        self.actionCategory.triggered.connect(self.show_category_section)

    def show_category_section(self):
        # Change QStackedWidget current index to the Category page
        self.uimanager.setCurrentIndex(2)  # Assuming the Category page is at index 1
        self.loadCategories()  # Load categories into the list widget

    def loadCategories(self):
        # Fetch category names from Category class
        categories = self.category_manager.fetch_categories()

        self.category_list_widget.clear()

        for category_name in categories:
            # Apply basic styling with HTML
            item_text = f"{category_name[1]}"  # Bold and blue text
            item = QListWidgetItem()
            item.setText(item_text)
            self.category_list_widget.addItem(item)

        self.category_table_widget.setAlternatingRowColors(True)
        self.category_table_widget.setColumnCount(3)
        self.category_table_widget.horizontalHeader().setCascadingSectionResizes(False)
        self.category_table_widget.horizontalHeader().setSortIndicatorShown(True)
        self.category_table_widget.horizontalHeader().setStretchLastSection(False)  # Disable stretching for manual width
        self.category_table_widget.verticalHeader().setVisible(False)
        self.category_table_widget.verticalHeader().setCascadingSectionResizes(True)
        self.category_table_widget.verticalHeader().setStretchLastSection(False)
        self.category_table_widget.setHorizontalHeaderLabels(("#", "Name", "Action"))
        self.category_table_widget.setColumnWidth(0, 5)
        self.category_table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.category_table_widget.setRowCount(0)

        for inx, category in enumerate(categories):
            print(category)
            cell_widget = QWidget()
            layout = QHBoxLayout(cell_widget)

            editBtn = QPushButton(self.category_table_widget)
            editBtn.setIcon(QIcon("icon/edit.png"))
            editBtn.setFixedWidth(50)

            deleteBtn = QPushButton(self.category_table_widget)
            deleteBtn.setIcon(QIcon("icon/delete.png"))
            deleteBtn.setFixedWidth(50)

            # Connect buttons to the event handler with the student ID
            editBtn.clicked.connect(lambda checked, category_id=category[0]: self.handleEdit(category_id))
            deleteBtn.clicked.connect(lambda checked, category_id=category[0]: self.handleDelete(category_id))

            layout.addWidget(editBtn)
            layout.addWidget(deleteBtn)

            # Set layout properties
            layout.setContentsMargins(0, 0, 0, 0)  # Optional: adjust spacing as needed
            cell_widget.setLayout(layout)

            # Insert a new row at the index 'inx'
            self.category_table_widget.insertRow(inx)

            # Populate the remaining columns with data from 'student'
            self.category_table_widget.setItem(inx, 0, QTableWidgetItem(str(category[0])))
            self.category_table_widget.setItem(inx, 1, QTableWidgetItem(str(category[1])))
            self.category_table_widget.setCellWidget(inx, 2, cell_widget)

        # Optionally, update the table widget after loading all rows
        self.category_table_widget.update()




