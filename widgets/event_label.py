from colors import COLORS
from kivy.uix.label import Label

from kivy.graphics import Color, Rectangle


class EventLabel(Label):
    def __init__(self, event_title, bg_color, **kwargs):

        super().__init__(
            text=event_title,
            font_size="10sp",
            color=COLORS["black"],
            halign="left",
            valign="top",
            padding=(5, 0),
            size_hint_x=1,
            size_hint_y=None,
            **kwargs,
        )

        with self.canvas.before:
            # Define the color for the background rectangle.
            Color(*bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Crucial: Bind the rectangle's position and size to the EventLabel's own position and size.
        self.bind(pos=self._update_rect, size=self._update_rect)

        self.bind(size=self.setter("text_size"))

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
