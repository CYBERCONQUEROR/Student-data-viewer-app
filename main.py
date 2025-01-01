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
        self.debounce_interval = 0.3  # Delay of 300ms between keystrokes
        self.debounce_event = None  # Store the Clock event for debouncing

    def build(self):
        self.icon = 'hi.png'  # Replace with your image path
        self.screen_manager = kivy.uix.screenmanager.ScreenManager()

        # Create screens
        self.search_screen = kivy.uix.screenmanager.Screen(name="search_screen")
        self.results_screen = kivy.uix.screenmanager.Screen(name="results_screen")
        self.searching_screen = kivy.uix.screenmanager.Screen(name="searching_screen")

        # Add screens to the manager
        self.screen_manager.add_widget(self.search_screen)
        self.screen_manager.add_widget(self.results_screen)
        self.screen_manager.add_widget(self.searching_screen)

        # Setup screens
        self.setup_search_screen()
        self.setup_searching_screen()
        self.setup_results_screen()

        # Load CSV data into memory for efficient searching
        self.load_csv_data()

        return self.screen_manager

    def load_csv_data(self):
        """Load CSV data into memory."""
        self.students_data = []
        try:
            with open("NOW.csv", "r") as file:
                reader = csv.reader(file)
         
                next(reader)  # Skip header row
                for row in reader:
                    if len(row) >= 10:
                        self.students_data.append({
                            'Name': row[2].strip(),
                            'Course': row[0].strip(),
                            'Branch': row[1].strip(),
                            'FatherName': row[3].strip(),
                            'MotherName': row[4].strip(),
                            'Dob': row[5].strip(),
                            'Category': row[6].strip(),
                            'MobileNumber': row[7].strip(),
                            'Religion': row[8].strip(),
                            'EmailId': row[9].strip()
                        })
        except FileNotFoundError:
            self.show_error_popup("Error", "The student data file (NOW.csv) is missing.")

    def setup_search_screen(self):
        layout = kivy.uix.boxlayout.BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Header Section
        header_label = kivy.uix.label.Label(
            text="Welcome",
            color=(1, 1, 1, 1),
            font_size=kivy.metrics.sp(24),
            bold=True,
            size_hint=(1, None),
            height=dp(100)
        )
        layout.add_widget(header_label)

        # ScrollView wrapping the form
        scroll = kivy.uix.scrollview.ScrollView(size_hint=(1, None), size=(kivy.core.window.Window.width, dp(500)))
        form_card = kivy.uix.boxlayout.BoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(10),
            size_hint=(1, None)
        )
        form_card.bind(minimum_height=form_card.setter('height'))

        self.course_spinner = kivy.uix.spinner.Spinner(
            text='Select Course',
            values=('B.Tech', 'B.Pharm', 'MBA'),
            size_hint=(1, None),
            height=dp(40)
        )
        form_card.add_widget(self.course_spinner)

        self.branch_spinner = kivy.uix.spinner.Spinner(
            text='Select Branch',
            values=[],
            size_hint=(1, None),
            height=dp(40)
        )
        form_card.add_widget(self.branch_spinner)

        form_card.add_widget(kivy.uix.label.Label(text="Enter Name:", font_size=kivy.metrics.sp(16)))
        self.name_input = kivy.uix.textinput.TextInput(
            hint_text="Enter Name",
            multiline=False,
            size_hint=(1, None),
            height=dp(40)
        )
        self.name_input.bind(text=self.on_name_input)
        form_card.add_widget(self.name_input)

        # Search Button
        self.search_button = kivy.uix.button.Button(
            text="Search",
            size_hint=(1, None),
            height=dp(50),
            background_normal='',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.search_button.bind(on_press=self.on_search_click)
        form_card.add_widget(self.search_button)

        scroll.add_widget(form_card)
        layout.add_widget(scroll)
        self.search_screen.add_widget(layout)

        # Bind course spinner selection to update branch options
        self.course_spinner.bind(text=self.on_course_select)

        # Initialize dropdown for name input
        self.suggestion_dropdown = kivy.uix.dropdown.DropDown()

    def setup_searching_screen(self):
        layout = kivy.uix.boxlayout.BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        searching_label = kivy.uix.label.Label(
            text="Please wait...",
            color=(1, 1, 1, 1),
            font_size=kivy.metrics.sp(24),
            bold=True,
            size_hint=(1, 1),
        )
        layout.add_widget(searching_label)
        self.searching_screen.add_widget(layout)

    def setup_results_screen(self):
        layout = kivy.uix.boxlayout.BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Scrollable results section with a Label
        self.result_label = kivy.uix.label.Label(
            text="Results will be shown here.",
            size_hint_y=None,
            markup=True,
        )
        self.result_label.bind(texture_size=self.update_label_height)

        result_scroll = kivy.uix.scrollview.ScrollView(size_hint=(1, 1))
        result_scroll.add_widget(self.result_label)
        layout.add_widget(result_scroll)

        # Add a Back Button to the results screen
        back_button = kivy.uix.button.Button(
            text="Back",
            size_hint=(None, None),
            size=(dp(100), dp(50)),
            background_normal='',
            background_color=(0.8, 0.2, 0.2, 1),
        )
        back_button.bind(on_press=self.go_back_to_search_screen)
        layout.add_widget(back_button)

        self.result_scroll = result_scroll
        self.results_screen.add_widget(layout)

    def update_label_height(self, instance, value):
        instance.height = instance.texture_size[1]
        self.result_scroll.scroll_y = 0

    def on_course_select(self, spinner, text):
        if text == "B.Tech":
            branches = ["CSE", "CSE-DS", "CSE-AIML", "CS", "IT", "CSE-IOT", "ECE", "ME"]
            self.branch_spinner.values = branches
        else:
            self.branch_spinner.values = []

    def get_suggestions(self, value):
        """Get suggestions based on course, branch, and partial name."""
        if not value:
            return []

        course = self.course_spinner.text.strip()
        branch = self.branch_spinner.text.strip()

        if course == "Select Course" or (course == "B.Tech" and branch == "Select Branch"):
            return []

        suggestions = []
        for student in self.students_data:
            # Filter by course and branch
            if to_lowercase(student['Course']) == to_lowercase(course):
                if course == "B.Tech" and to_lowercase(student['Branch']) != to_lowercase(branch):
                    continue
                if value.lower() in student['Name'].lower():
                    suggestions.append(student['Name'])

            # Stop once we have enough suggestions
            if len(suggestions) >= 10:
                break

        return suggestions

    def on_name_input(self, instance, value):
        # Cancel previous debounce event if any
        if self.debounce_event:
            self.debounce_event.cancel()

        # Schedule the debounce event
        self.debounce_event = Clock.schedule_once(
            lambda dt: self.update_suggestions(value), self.debounce_interval
        )

    def update_suggestions(self, value):
        # Dismiss the dropdown if it's already open
        if self.suggestion_dropdown.parent:
            self.suggestion_dropdown.dismiss()

        # Get the suggestions based on the input value
        suggestions = self.get_suggestions(value)

        # Clear any previous widgets in the dropdown
        self.suggestion_dropdown.clear_widgets()

        # If there are suggestions, add them to the dropdown
        for suggestion in suggestions:
            button = kivy.uix.button.Button(text=suggestion, size_hint_y=None, height=dp(40))
            button.bind(on_release=self.on_suggestion_selected)
            self.suggestion_dropdown.add_widget(button)

        # Open the dropdown if there are any suggestions
        if suggestions:
            if self.suggestion_dropdown.parent:
                self.suggestion_dropdown.parent.remove_widget(self.suggestion_dropdown)
            self.suggestion_dropdown.open(self.name_input)

    def on_suggestion_selected(self, instance):
        self.name_input.text = instance.text
        self.suggestion_dropdown.dismiss()

    def on_search_click(self, instance):
        course = self.course_spinner.text
        name = self.name_input.text
        branch = self.branch_spinner.text if course == "B.Tech" else ""

        if not course or not name:
            self.show_error_popup("Error", "Please fill in the Course and Name fields.")
            return

        if course == "B.Tech" and not branch:
            self.show_error_popup("Error", "Please select a branch.")
            return

        self.screen_manager.current = "searching_screen"
        Clock.schedule_once(lambda dt: self.search_for_students(course, branch, name), 1)

    def search_for_students(self, course, branch, name):
        students = [
            student for student in self.students_data
            if to_lowercase(student['Course']) == to_lowercase(course)
            and (course != "B.Tech" or to_lowercase(student['Branch']) == to_lowercase(branch))
            and name.lower() in student['Name'].lower()
        ]
        self.display_students(students)

    def display_students(self, students):
        self.result_label.text = ""

        if not students:
            self.result_label.text = "No matching records found.\n"
        else:
            for idx, student in enumerate(students):
                self.result_label.text += f"[b]--- Record {idx + 1} ---[/b]\n"
                for key, value in student.items():
                    if key != 'Branch' or student['Course'] == "B.Tech":
                        self.result_label.text += f"{key}: {value}\n"
                self.result_label.text += "\n"

        self.update_label_height(self.result_label, None)
        self.screen_manager.current = "results_screen"

    def go_back_to_search_screen(self, instance):
        self.screen_manager.current = "search_screen"

    def show_error_popup(self, title, message):
        popup = kivy.uix.popup.Popup(
            title=title,
            content=kivy.uix.label.Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()


if __name__ == '__main__':
    StudentSearchApp().run()
