from kivy.uix.screenmanager import Screen
from kivy.app import App

class ConnectScreen(Screen):
    '''
    Tela inicial do app
    '''

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
        if app.main_screen.start_connection():
            app.sm.current = 'main_screen'