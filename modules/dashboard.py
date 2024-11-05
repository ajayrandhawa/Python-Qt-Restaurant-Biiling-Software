from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from modules.category import Category


class Dashboard(QMainWindow):
    def __init__(self):
        super(Dashboard, self).__init__()
        uic.loadUi('ui/dashboard.ui', self)
        self.showMaximized()

        # Initialize Category class instance
        self.category_manager = Category()

        # Set UI elements for the Category instance
        self.category_manager.set_ui_elements(
            self.category_name_input,
            self.category_list_widget,
            self.category_table_widget
        )

        # Connect add_category_btn to the saveCategory method in Category
        self.add_category_btn.clicked.connect(self.category_manager.saveCategory)

        # Connect actionCategory to the show_category_section method
        self.actionCategory.triggered.connect(self.show_category_section)

    def show_category_section(self):
        # Show the category section and load the categories
        self.uimanager.setCurrentIndex(2)  # Assuming the Category page index is 2
        self.category_manager.loadCategoryList()  # Load list of categories
        self.category_manager.loadCategoryTable()  # Load table of categories with actions
