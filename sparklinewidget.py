from datetime import datetime

from kivy.uix.boxlayout import BoxLayout
from kivy_garden.graph import LinePlot
from kivy.utils import get_color_from_hex
from kivy.properties import NumericProperty, StringProperty

from timeseriesgraph import TimeSeriesGraph
from indicatorwidget import IndicatorWidget

class SparklineWidget(BoxLayout):
    ymin = NumericProperty(0)
    ymax = NumericProperty(100)
    unity = StringProperty('')
    val = NumericProperty(0)
    title = StringProperty('')

    def __init__(self, **kwargs):
        super(SparklineWidget, self).__init__(**kwargs)
        
    def on_kv_post(self, base_widget):
        self._indicator = self.ids['indicator']
        self._graph = self.ids['graph']
        plot = LinePlot(line_width=1.5, color=get_color_from_hex('#475CA7'))
        self._graph.add_plot(plot)

    def update_val(self, val):
        self.val = val
        self._indicator.update_val(val)
        self._graph.updateGraph((datetime.now(), val), 0)