from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ColorProperty
from kivy.graphics import Rectangle, Color
from kivy_garden.graph import LinePlot
from kivy.utils import get_color_from_hex

from widgets.timeseriesgraph import TimeSeriesGraph

plot_color = {
    'ativa_r': get_color_from_hex("#898952"),
    'ativa_s': get_color_from_hex("#B2945B"),
    'ativa_t': get_color_from_hex("#D0E562"),
    'ativa_tot': get_color_from_hex("#B6D7B1"),
    'reativa_r': get_color_from_hex("#EA8C55"),
    'reativa_s': get_color_from_hex("#C75146"),
    'reativa_t': get_color_from_hex("#AD2E24"),
    'reativa_tot': get_color_from_hex("#81171B"),
    'aparente_r': get_color_from_hex("#A6EBC9"),
    'aparente_s': get_color_from_hex("#61FF7E"),
    'aparente_t': get_color_from_hex("#5EEB5B"),
    'aparente_tot': get_color_from_hex("#62AB37"),
    'vel': get_color_from_hex("#B9314F"),
    'pit01': get_color_from_hex("#EFBC9B"),
    'fit02': get_color_from_hex("#EE92C2"),
    'fit03': get_color_from_hex("#9D6A89"),
    'tensao_rs': get_color_from_hex("#065143"),
    'tensao_st': get_color_from_hex("#129490"),
    'tensao_tr': get_color_from_hex("#70B77E"),
    'corrente_r': get_color_from_hex("#0A2239"),
    'corrente_s': get_color_from_hex("#53A2BE"),
    'corrente_t': get_color_from_hex("#1D84B5"),
    'corrente_n': get_color_from_hex("#132E32"),
    'corrente_med': get_color_from_hex("#176087"),
    'temp_r': get_color_from_hex("#C4BBAF"),
    'temp_s': get_color_from_hex("#A5978B"),
    'temp_t': get_color_from_hex("#5C4742"),
    'temp_carc': get_color_from_hex("#8D5B4C"),
}

class DataGraphWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._indexes = {}

    def add_plot(self, data, label):
        plt = LinePlot(line_width=1.5, color=plot_color[label])
        self.ids['graph'].add_plot(self.plot)
        plt.points = data
        index = self.ids['graph'].plots.index(plt)
        

        self._indexes[label] = index

        leg = Legend(text=label, color=plot_color[label])
        self._legends[label] = leg
        self.ids['legend'].add_widget(leg)

    def remove_plot(self, label):
        index = self._indexes[label]
        self.ids['graph'].remove_plot(self.ids['graph'].plots[index])
        if label in self._indexes: del self._indexes[label]

        self.ids['legend'].remove_widget(self._legends[label])
        if label in self._legends: del self._legends[label]
    
    def update_plots(self, all_data):
        for label in all_data:
            index = self._indexes[label]
            self.ids['graph'].update_graph(all_data[label], index)

class Legend(BoxLayout):
    color = ColorProperty() 
    text = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        
        txt = Label(text=self.text, pos=(self.x + 30, self.y))
        with self.canvas:
            Color(rgb=self.color)
            Rectangle(size=(30,30), pos=(self.x, self.y))

