from kivy.uix.widget import Widget
from kivy_garden.graph import LinePlot
from timeseriesgraph import TimeSeriesGraph
from kivy.utils import get_color_from_hex

class DataGraphWidget(Widget):
    def __init__(self, xmax=20, plot_color=get_color_from_hex("#475CA7"), **kwargs):
        super().__init__(**kwargs)
        self.plot = LinePlot(line_width=1.5, color=plot_color)
        self.ids['graph'].add_plot(self.plot)
        self.ids.graph.xmax = xmax