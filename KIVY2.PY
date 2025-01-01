import kivy
import kivy.app
import kivy.uix.boxlayout
import kivy.uix.label
import kivy.uix.button
import kivy.uix.textinput
import kivy.uix.spinner
import kivy.uix.scrollview
import kivy.uix.popup
import kivy.metrics
import kivy.core.window
# import ctypes
import csv

# Set a mobile-friendly window size for testing
kivy.core.window.Window.size = (360, 640)  # Example mobile resolution

# Function to trim leading and trailing whitespace
def trim(s):
    return s.strip()

# Function to convert string to lowercase
def to_lowercase(s):
    return s.lower()

# Function to search the CSV file
def search_csv(course, branch, name):
    students = []
    try:
        with open("C:\\coding\\RKGIT\\Hii\\NOW.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            course = to_lowercase(trim(course))
            branch = to_lowercase(trim(branch))
            name = to_lowercase(trim(name))

            for row in reader:
                if len(row) < 10:
                    continue
                student = {
                    'course': row[0].strip(),
                    'branch': row[1].strip(),
                    'name': row[2].strip(),
                    'fatherName': row[3].strip(),
                    'motherName': row[4].strip(),
                    'dob': row[5].strip(),
                    'category': row[6].strip(),
                    'mobileNumber': row[7].strip(),
                    'religion': row[8].strip(),
                    'emailId': row[9].strip()
                }

                # Case insensitive comparison and partial matching for the name
                if (to_lowercase(student['course']) == course and 
                    to_lowercase(student['branch']) == branch and 
                    name in to_lowercase(student['name'])):  # Partial match for name
                    students.append(student)
        return students
    except FileNotFoundError:
        return []

# Kivy Application
class StudentSearchApp(kivy.app.App):
    def build(self):
        self.layout = kivy.uix.boxlayout.BoxLayout(orientation='vertical', padding=kivy.metrics.dp(10), spacing=kivy.metrics.dp(10))

        # Header Section
        header_label = kivy.uix.label.Label(
            text="Welcome", 
            color=(1, 1, 1, 1), 
            font_size=kivy.metrics.sp(24), 
            bold=True,
            size_hint=(1, None),
            height=kivy.metrics.dp(50)
        )
        self.layout.add_widget(header_label)

        # ScrollView wrapping the form
        scroll = kivy.uix.scrollview.ScrollView(size_hint=(1, None), size=(kivy.core.window.Window.width, kivy.metrics.dp(400)))
        form_card = kivy.uix.boxlayout.BoxLayout(
            orientation='vertical', 
            padding=kivy.metrics.dp(10), 
            spacing=kivy.metrics.dp(10),
            size_hint=(1, None)
        )
        form_card.bind(minimum_height=form_card.setter('height'))

        # form_card.add_widget(kivy.uix.label.Label(text="Select Course:", font_size=kivy.metrics.sp(16)))
        self.course_spinner = kivy.uix.spinner.Spinner(
            text='Select Course', 
            values=('B.Tech', 'B.Pharm', 'MBA'),
            size_hint=(1, None),
            height=kivy.metrics.dp(40)
        )
        form_card.add_widget(self.course_spinner)

        # form_card.add_widget(kivy.uix.label.Label(text="Select Branch:", font_size=kivy.metrics.sp(16)))
        self.branch_spinner = kivy.uix.spinner.Spinner(
            text='Select Branch', 
            values=[], 
            size_hint=(1, None),
            height=kivy.metrics.dp(40)
        )
        form_card.add_widget(self.branch_spinner)

        form_card.add_widget(kivy.uix.label.Label(text="Enter Name:", font_size=kivy.metrics.sp(16)))
        self.name_input = kivy.uix.textinput.TextInput(
            hint_text="Enter Name", 
            multiline=False, 
            size_hint=(1, None),
            height=kivy.metrics.dp(40)
        )
        form_card.add_widget(self.name_input)

        # Search Button
        self.search_button = kivy.uix.button.Button(
            text="Search",
            size_hint=(1, None),
            height=kivy.metrics.dp(50),
            background_normal='', 
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.search_button.bind(on_press=self.on_search_click)
        form_card.add_widget(self.search_button)

        scroll.add_widget(form_card)
        self.layout.add_widget(scroll)

        # Results Section
        self.result_text = kivy.uix.textinput.TextInput(
            hint_text="Results will be shown here.", 
            multiline=True, 
            readonly=True,
            size_hint=(1, None),
            height=kivy.metrics.dp(300)
        )
        result_scroll = kivy.uix.scrollview.ScrollView(size_hint=(1, 1))
        result_scroll.add_widget(self.result_text)
        self.layout.add_widget(result_scroll)

        # Bind course spinner selection to update branch options
        self.course_spinner.bind(text=self.on_course_select)

        return self.layout

    def on_course_select(self, spinner, text):
        if text == "B.Tech":
            branches = ["CSE", "CSE-DS", "CSE-AIML", "CS", "IT", "CSE-IOT", "ECE", "ME"]
            self.branch_spinner.values = branches
        else:
            self.branch_spinner.values = []

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

        # Perform the search
        students = search_csv(course, branch, name)
        self.display_students(students)

    def display_students(self, students):
        self.result_text.text = ""  # Clear previous results

        if not students:
            self.result_text.text = "No matching records found.\n"
        else:
            for idx, student in enumerate(students):
                self.result_text.text += f"--- Record {idx + 1} ---\n"
                for key, value in student.items():
                    self.result_text.text += f"{key}: {value}\n"
                self.result_text.text += "\n"

    def show_error_popup(self, title, message):
        popup = kivy.uix.popup.Popup(title=title, content=kivy.uix.label.Label(text=message), size_hint=(None, None), size=(kivy.metrics.dp(300), kivy.metrics.dp(200)))
        popup.open()


if __name__ == "__main__":
    StudentSearchApp().run()
