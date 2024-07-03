from kivy.uix.popup import Popup
from kivy_garden.graph import LinePlot
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App


class DataGraphPopup(Popup):
    def __init__(self, xmax, plot_color, **kwargs):
        super().__init__(**kwargs)
        self.plot = LinePlot(line_width=1.5, color = plot_color)
        self.ids.graph.add_plot(self.plot)
        self.ids.graph.xmax = xmax

class LabeledCheckBoxDataGraph(BoxLayout):
    pass

class SettingsPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()
        self.ids.txt_ip.text = str(app.server_ip)
        self.ids.txt_port.text = str(app.server_port)
        self.ids.txt_st.text = str(app.scan_time)

    def submit(self):
        app = App.get_running_app()
        app.server_ip = self.ids.txt_ip.text
        app.server_port = int(self.ids.txt_port.text)
        app.scan_time = int(self.ids.txt_st.text)
        if app.sm.get_screen('main_screen').start_connection():
            self.dismiss()
