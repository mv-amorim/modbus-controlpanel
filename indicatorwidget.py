from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Triangle
from kivy.properties import NumericProperty

class IndicatorWidget(Widget):
    ymin = NumericProperty(0)
    ymax = NumericProperty(100)
    increment = NumericProperty(0)

    def __init__(self, **kwargs):
        super(IndicatorWidget, self).__init__(**kwargs)

    def update_val(self, val):
        self._range = self.ymax - self.ymin
        self.increment = self.height * (val/self._range)
        self.canvas.clear()
        with self.canvas:
            Color(rgb=get_color_from_hex("#475CA7"))
            Triangle(points=(self.x-5, self.y-6 + self.increment, self.x-5, self.y+6 + self.increment, self.x+5, self.y + self.increment))

    