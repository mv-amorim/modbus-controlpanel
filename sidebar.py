from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

class Sidebar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_slider_release(self, touch, widget):
        if touch.grab_current == widget:
            freq = self.ids['inv_freq'].value
            App.get_running_app().main_screen._modbus_client.set_freq(round(freq,1))

    def on_switch_release(self, touch, widget, i):
        if touch.grab_current == widget:
            App.get_running_app().main_screen.switch_xv(i)