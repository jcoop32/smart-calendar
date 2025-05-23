from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.properties import ObjectProperty

from colors import COLORS  # Import your COLORS dictionary


class CustomizationPopup(Popup):
    # This property will hold a reference to the function in the main app
    # that will apply the selected colors.
    apply_callback = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Customize Calendar Colors"
        self.size_hint = (0.7, 0.7)  # Adjust popup size as needed

        # Main layout for the popup content
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Dictionary to store references to the Spinner widgets
        self.color_spinners = {}

        # Define which elements are customizable and their initial color keys
        # These keys should match the 'COLORS' dictionary keys.
        # You can add more elements here if you want to customize other parts.
        customizable_elements = {
            "Current Day Background": "purple",
            "Default Day Background": "white",
            "Date Text Color": "black",
            "Event Background Color": "lightgray",
            "Event Text Color": "black",
        }

        # Create a row for each customizable element (Label + Spinner)
        for element_name, default_color_key in customizable_elements.items():
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
            row.add_widget(Label(text=element_name, size_hint_x=0.6))

            # Spinner for color selection, listing all colors from COLORS
            color_spinner = Spinner(
                text=default_color_key,  # Set initial text to the default color
                values=list(COLORS.keys()),  # Populate with all color names
                size_hint_x=0.4,
            )
            self.color_spinners[element_name] = (
                color_spinner  # Store spinner for later retrieval
            )
            row.add_widget(color_spinner)
            content.add_widget(row)

        # Buttons for Apply and Cancel
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        apply_button = Button(text="Apply", on_release=self.apply_changes)
        cancel_button = Button(text="Cancel", on_release=self.dismiss)
        button_layout.add_widget(apply_button)
        button_layout.add_widget(cancel_button)
        content.add_widget(button_layout)

        self.content = content  # Set the content of the popup

    def apply_changes(self, instance):
        # Collect the currently selected color for each element
        selected_colors = {}
        for element_name, spinner in self.color_spinners.items():
            selected_colors[element_name] = (
                spinner.text
            )  # Get the selected color name (string key)

        # Call the callback function provided by the main app, passing the selected colors
        if self.apply_callback:
            self.apply_callback(selected_colors)
        self.dismiss()  # Close the popup
