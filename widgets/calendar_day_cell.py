from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle


class DayCell(GridLayout):
    def __init__(self, day_num, bg_color, date_text_color, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.padding = 2
        self.spacing = 5
        self.day_num = day_num

        with self.canvas.before:
            Color(*bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # anchor layout to position the date number at the top-left
        date_anchor = AnchorLayout(
            anchor_x="left",
            anchor_y="top",
            size_hint=(1, None),
            height=70,
        )
        date_anchor.add_widget(
            Label(
                text=str(day_num),
                size_hint=(None, None),
                font_size="20sp",
                color=date_text_color,
                padding=(0, 0),
            )
        )
        self.add_widget(date_anchor)

        # events to be appended here
        self.event_box = BoxLayout(
            orientation="vertical", spacing=1, size_hint=(1, 1), padding=(0, 0, 0, 0)
        )
        self.add_widget(self.event_box)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
