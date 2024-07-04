from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

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

class DisconnectedPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()
        self.ids.txt_ip.text = str(app.server_ip)
        self.ids.txt_port.text = str(app.server_port)

    def submit(self):
        app = App.get_running_app()
        app.server_ip = self.ids.txt_ip.text
        app.server_port = int(self.ids.txt_port.text)
        if app.sm.get_screen('main_screen').start_connection():
            self.dismiss()
    
    def dismiss(self, *_args, **kwargs):
        app = App.get_running_app()
        if app.connected:
            return super().dismiss(*_args, **kwargs)