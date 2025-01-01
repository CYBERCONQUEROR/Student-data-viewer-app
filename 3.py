import kivy
import kivy.app
import kivy.uix.boxlayout
import kivy.uix.label
import kivy.uix.button
import kivy.uix.textinput
import kivy.uix.spinner
import kivy.uix.scrollview
import kivy.uix.popup
import kivy.uix.screenmanager
import kivy.metrics
import kivy.core.window
import csv
import ctypes
from kivy.metrics import dp
from kivy.clock import Clock


# Utility functions
def trim(s):
    return s.strip()


def to_lowercase(s):
    return s.lower()


class StudentSearchApp(kivy.app.App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.admin_password = "admin123"  # Password for Admin access
        self.students_data = []  # Will be populated with data from the CSV file
        self.current_user = None  # Store the currently logged-in user

    def build(self):
        self.icon = 'hi.png'  # Replace with your image path
        self.screen_manager = kivy.uix.screenmanager.ScreenManager()

        # Create screens
        self.login_screen = kivy.uix.screenmanager.Screen(name="login_screen")
        self.search_screen = kivy.uix.screenmanager.Screen(name="search_screen")
        self.results_screen = kivy.uix.screenmanager.Screen(name="results_screen")
        self.student_details_screen = kivy.uix.screenmanager.Screen(name="student_details_screen")

        # Add screens to the manager
        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.search_screen)
        self.screen_manager.add_widget(self.results_screen)
        self.screen_manager.add_widget(self.student_details_screen)

        # Setup screens
        self.setup_login_screen()
        self.setup_search_screen()
        self.setup_results_screen()
        self.setup_student_details_screen()

        # Load CSV data
        self.load_csv_data()

        return self.screen_manager

    def load_csv_data(self):
        """Load CSV data into memory."""
        try:
            with open("hi.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    if len(row) >= 10:
                        self.students_data.append({
                            'Name': row[2].strip(),
                            'Password': row[9].strip(),  # Assuming password is in the 10th column
                            'Course': row[0].strip(),
                            'Branch': row[1].strip(),
                            'FatherName': row[3].strip(),
                            'MotherName': row[4].strip(),
                            'Dob': row[5].strip(),
                            'Category': row[6].strip(),
                            'MobileNumber': row[7].strip(),
                            'Religion': row[8].strip(),
                        })
        except FileNotFoundError:
            self.show_error_popup("Error", "The student data file (hi.csv) is missing.")

    def setup_login_screen(self):
        layout = kivy.uix.boxlayout.BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header
        header_label = kivy.uix.label.Label(
            text="Login as Admin or Student",
            font_size=24,
            bold=True,
            size_hint=(1, None),
            height=dp(50)
        )
        layout.add_widget(header_label)

        # Buttons for Admin and Student
        admin_button = kivy.uix.button.Button(
            text="Admin Login",
            size_hint=(1, None),
            height=dp(50)
        )
        admin_button.bind(on_press=lambda instance: self.show_admin_login())

        student_button = kivy.uix.button.Button(
            text="Student Login",
            size_hint=(1, None),
            height=dp(50)
        )
        student_button.bind(on_press=lambda instance: self.show_student_login())

        layout.add_widget(admin_button)
        layout.add_widget(student_button)

        self.login_screen.add_widget(layout)

    def show_admin_login(self):
        layout = kivy.uix.boxlayout.BoxLayout(orientation='vertical', padding=10, spacing=10)

        password_input = kivy.uix.textinput.TextInput(
            hint_text="Enter Admin Password",
            password=True,
            size_hint=(1, None),
            height=dp(50)
        )
        layout.add_widget(password_input)

        submit_button = kivy.uix.button.Button(
            text="Submit",
            size_hint=(1, None),
            height=dp(50)
        )
        submit_button.bind(on_press=lambda instance: self.validate_admin_password(password_input.text))

        layout.add_widget(submit_button)

        self.login_screen.clear_widgets()
        self.login_screen.add_widget(layout)

    def validate_admin_password(self, password):
        if password == self.admin_password:
            self.screen_manager.current = "search_screen"
        else:
            self.show_error_popup("Login Failed", "Incorrect Admin Password!")

    def show_student_login(self):
        layout = kivy.uix.boxlayout.BoxLayout(orientation='vertical', padding=10, spacing=10)

        name_input = kivy.uix.textinput.TextInput(
            hint_text="Enter Name",
            size_hint=(1, None),
            height=dp(50)
        )
        password_input = kivy.uix.textinput.TextInput(
            hint_text="Enter Password",
            password=True,
            size_hint=(1, None),
            height=dp(50)
        )
        layout.add_widget(name_input)
        layout.add_widget(password_input)

        submit_button = kivy.uix.button.Button(
            text="Submit",
            size_hint=(1, None),
            height=dp(50)
        )
        submit_button.bind(on_press=lambda instance: self.validate_student_login(name_input.text, password_input.text))

        layout.add_widget(submit_button)

        self.login_screen.clear_widgets()
        self.login_screen.add_widget(layout)

    def validate_student_login(self, name, password):
        for student in self.students_data:
            if student['Name'].lower() == name.lower() and student['Password'] == password:
                self.current_user = student
                self.display_student_details(student)
                self.screen_manager.current = "student_details_screen"
                return

        self.show_error_popup("Login Failed", "Incorrect Name or Password!")

    def setup_search_screen(self):
        # Existing search screen setup logic
        pass

    def setup_results_screen(self):
        # Existing results screen setup logic
        pass

    def setup_student_details_screen(self):
        layout = kivy.uix.boxlayout.BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.student_details_label = kivy.uix.label.Label(
            text="",
            size_hint=(1, None),
            height=dp(200)
        )
        layout.add_widget(self.student_details_label)

        back_button = kivy.uix.button.Button(
            text="Back to Login",
            size_hint=(1, None),
            height=dp(50)
        )
        back_button.bind(on_press=lambda instance: self.screen_manager.current = "login_screen")

        layout.add_widget(back_button)
        self.student_details_screen.add_widget(layout)

    def display_student_details(self, student):
        details = "\n".join([f"{key}: {value}" for key, value in student.items()])
        self.student_details_label.text = details

    def show_error_popup(self, title, message):
        popup = kivy.uix.popup.Popup(
            title=title,
            content=kivy.uix.label.Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()


if __name__ == '__main__':
    StudentSearchApp().run()
