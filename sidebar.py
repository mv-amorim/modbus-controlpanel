from threading import Thread
from time import sleep
from datetime import datetime

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

class Sidebar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._update_clock = True
        self._clock_thread = Thread(target=self.update_clock)
        self._clock_thread.start()
    
    def on_slider_release(self, touch, widget):
        if touch.grab_current == widget:
            freq = self.ids['inv_freq'].value
            App.get_running_app().main_screen._modbus_client.set_freq(round(freq,1))

    def on_switch_release(self, touch, widget, i):
        if touch.grab_current == widget:
            App.get_running_app().main_screen.switch_xv(i)

    def update_clock(self):
        while self._update_clock:
            now = datetime.now()
            self.ids['time'].text = now.strftime('%H:%M:%S')
            sleep(1)
    
    def stop_refresh(self):
        self._update_clock = False