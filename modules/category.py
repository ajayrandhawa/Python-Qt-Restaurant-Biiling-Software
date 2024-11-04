import sqlite3

class Category:
    def __init__(self):
        # Placeholder for UI elements
        self.category_name_input = None
        self.fetch_categories()

    def set_ui_elements(self, category_name_input):
        # Set the UI elements passed from Dashboard
        self.category_name_input = category_name_input

    def saveCategory(self):
        if not self.category_name_input:
            print("UI elements not set")
            return

        # Get the text from category_name_input
        category_name = self.category_name_input.text()

        if category_name:  # Check if the input is not empty
            # Connect to SQLite database
            connection = sqlite3.connect("db/database.db")
            cursor = connection.cursor()

            try:
                # Insert the new category into the category table
                cursor.execute("INSERT INTO category (category_name) VALUES (?)", (category_name,))
                connection.commit()
                print("Category saved:", category_name)
            except sqlite3.IntegrityError:
                print("Category already exists.")
            finally:
                connection.close()
        else:
            print("Category name is empty.")

    def fetch_categories(self):
        database_path = "db/database.db"
        query = "SELECT * FROM category"

        try:
            # Establish a connection to the database
            with sqlite3.connect(database_path) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                categories = cursor.fetchall()
                return categories

        except sqlite3.Error as e:
            print(f"SQLite Error {e.args[0]}: {e}")
            return None