from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ColorProperty
from kivy_garden.graph import LinePlot
from kivy.clock import Clock
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

    def add_plot(self, data, label):
        plt = LinePlot(line_width=1.5, color=plot_color[label])
        plt.points = data
        self.ids['graph'].add_plot(plt)
        
        leg = Legend(text=label, color=plot_color[label])
        self.ids['legends'].add_widget(leg)
    
    def update_plots(self, all_data):
        self.clear()
        graph = self.ids['graph']
        
        for key in all_data.keys():
            self.add_plot(all_data[key], key)

        xmin = []
        xmax = []
        ymin = []
        ymax = []
        for i in range(graph.plots.__len__()):
            if graph.plots[i].points:
                xmin.append(min(graph.plots[i].points)[0])
                ymin.append(min(graph.plots[i].points)[1])
                xmax.append(max(graph.plots[i].points)[0])
                ymax.append(max(graph.plots[i].points)[1])

        if xmin: graph.xmin = min(xmin)
        if xmax: graph.xmax = max(xmax)
        if ymin: graph.ymin = min(ymin) - 10
        if ymax: graph.ymax = max(ymax) + 10

        Clock.schedule_once(graph.clear_label)
        graph.update_x_labels()

    def clear(self):
        self.ids['graph'].clear_plots()
        self.ids['legends'].clear_widgets()

class Legend(BoxLayout):
    color = ColorProperty() 
    text = StringProperty()