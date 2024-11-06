from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from modules.category import Category
from modules.items import Items


class Dashboard(QMainWindow):
    def __init__(self):
        super(Dashboard, self).__init__()
        uic.loadUi('ui/dashboard.ui', self)
        self.showMaximized()

        # Initialize Category class instance
        self.category_manager = Category()
        self.items_manager = Items()

        # Set UI elements for the Category instance
        self.category_manager.set_ui_elements(self.category_name_input, self.category_list_widget, self.category_table_widget)
        self.items_manager.set_ui_elements(self.items_name_input, self.items_category_combo, self.items_price_input, self.items_description_input, self.items_mtype_combo, self.items_table_widget, self.items_list_widget)

        # Connect add_category_btn to the saveCategory method in Category
        self.add_category_btn.clicked.connect(self.category_manager.saveCategory)
        self.add_items_btn.clicked.connect(self.items_manager.createItem)

        self.actionCategory.triggered.connect(self.show_category_section)
        self.actionItems.triggered.connect(self.show_items_section)
        self.actionDashboard.triggered.connect(self.show_dashboard_section)


    def show_category_section(self):
        self.uimanager.setCurrentIndex(2)
        self.category_manager.loadCategoryList()
        self.category_manager.loadCategoryTable()

    def show_items_section(self):
        self.uimanager.setCurrentIndex(1)
        self.items_manager.loadItemsList()
        self.items_manager.loadItemTable()
        self.items_manager.load_categories_in_combo()

    def show_dashboard_section(self):
        self.uimanager.setCurrentIndex(0)