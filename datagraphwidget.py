from kivy.uix.widget import Widget
from kivy_garden.graph import LinePlot
from timeseriesgraph import TimeSeriesGraph

class DataGraphWidget(Widget):
    def __init__(self, xmax, plot_color, **kwargs):
        super().__init__(**kwargs)
        self.plot = LinePlot(line_width=1.5, color=plot_color)
        self.ids.graph.add_plot(self.plot)
        self.ids.graph.xmax = xmax