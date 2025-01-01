import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.metrics import dp
import csv
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup  # Corrected import



class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Login Header
        header = Label(
            text="Login",
            font_size='24sp',
            bold=True,
            size_hint=(1, 0.2),
        )
        layout.add_widget(header)

        # Admin and Student Buttons
        admin_button = Button(text="Admin Login", size_hint=(1, None), height=dp(50))
        admin_button.bind(on_press=self.admin_login)
        layout.add_widget(admin_button)

        student_button = Button(text="Student Login", size_hint=(1, None), height=dp(50))
        student_button.bind(on_press=self.student_login)
        layout.add_widget(student_button)

        self.add_widget(layout)

    def admin_login(self, instance):
        self.manager.current = "admin_login_screen"

    def student_login(self, instance):
        self.manager.current = "student_login_screen"


class AdminLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.admin_password = "ko"  # Set your admin password here

        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Password Input
        self.password_input = TextInput(
            hint_text="Enter Admin Password",
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
        )
        layout.add_widget(self.password_input)

        # Submit Button
        submit_button = Button(text="Submit", size_hint=(1, None), height=dp(50))
        submit_button.bind(on_press=self.validate_password)
        layout.add_widget(submit_button)

        # Back Button
        back_button = Button(text="Back", size_hint=(1, None), height=dp(50))
        back_button.bind(on_press=self.go_back)  # Corrected syntax
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "login_screen"

    def validate_password(self, instance):
        if self.password_input.text == self.admin_password:
            # Correct password, switch to the admin's dashboard or any other screen
            self.manager.current = "student_results_screen"  # or change to your desired screen
        else:
            self.show_error_popup("Invalid Password", "Please try again.")

    def show_error_popup(self, title, message):
        popup = kivy.uix.popup.Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4),
        )
        popup.open()



class StudentLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.students_data = []  # This will hold the CSV data
        self.load_csv_data()

        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Name Input
        self.name_input = TextInput(
            hint_text="Enter Your Name",
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
        )
        layout.add_widget(self.name_input)

        # Password Input
        self.password_input = TextInput(
            hint_text="Enter Your Password",
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
        )
        layout.add_widget(self.password_input)

        # Submit Button
        submit_button = Button(text="Submit", size_hint=(1, None), height=dp(50))
        submit_button.bind(on_press=self.validate_student)
        layout.add_widget(submit_button)

        # Back Button
        back_button = Button(text="Back", size_hint=(1, None), height=dp(50))
        back_button.bind(on_press=self.go_back)  # Corrected syntax
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "login_screen"

    def load_csv_data(self):
        try:
            with open("hi.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    if len(row) >= 10:
                        name = row[2].strip()
                        phone = row[7].strip()
                        password = name[:4].lower() + phone[:4]
                        self.students_data.append({
                            'Name': name,
                            'Password': password,
                            'Data': row
                        })
        except FileNotFoundError:
            self.show_error_popup("Error", "The student data file (hi.csv) is missing.")

    def validate_student(self, instance):
        name = self.name_input.text.strip()
        password = self.password_input.text.strip()

        for student in self.students_data:
            if student['Name'].lower() == name.lower() and student['Password'] == password:
                # Valid student, show their data
                self.manager.current = "student_results_screen"
                self.manager.get_screen("student_results_screen").display_student_data(student['Data'])
                return

        self.show_error_popup("Invalid Login", "Name or password is incorrect.")

    def show_error_popup(self, title, message):
        popup = kivy.uix.popup.Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4),
        )
        popup.open()


class StudentResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.result_label = Label(size_hint_y=None, markup=True)
        self.scroll = kivy.uix.scrollview.ScrollView()
        self.scroll.add_widget(self.result_label)

        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        layout.add_widget(self.scroll)

        back_button = Button(text="Back", size_hint=(1, None), height=dp(50))
        back_button.bind(on_press=self.go_back)  # Corrected syntax
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "login_screen"

    def display_student_data(self, data):
        self.result_label.text = "\n".join(f"{key}: {value}" for key, value in zip(
            ["Course", "Branch", "Name", "Father Name", "Mother Name", "DOB", "Category", "Mobile Number", "Religion", "Email Id"], data
        ))


class MyStudentApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login_screen"))
        sm.add_widget(AdminLoginScreen(name="admin_login_screen"))
        sm.add_widget(StudentLoginScreen(name="student_login_screen"))
        sm.add_widget(StudentResultsScreen(name="student_results_screen"))

        return sm


if __name__ == "__main__":
    MyStudentApp().run()
