from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
import os


class TestApp(App):
    def build(self):
        layout = BoxLayout()
        path = "/api/weather/condition_icons/sun.png"
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        path2 = os.path.join(BASE_DIR, "api", "weather", "condition_icons", "sunny.png")
        print(path2)
        # <-- Replace with actual path
        print("File exists:", os.path.exists(path2))  # should print True
        img = Image(source=path2, size_hint=(None, None), size=(100, 100))
        layout.add_widget(img)
        return layout


if __name__ == "__main__":
    TestApp().run()
