import os
from kivy.app import App
from mainscreen import MainScreen
from connectscreen import ConnectScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from kivy.core.window import Window

global app

class MainApp(App):
    server_ip = '192.168.0.14'
    server_port = 502
    scan_time = 500
    connected = False

    def build(self):
        sm = ScreenManager()
        self.main_screen = MainScreen(name='main_screen')
        sm.add_widget(self.main_screen)
        sm.add_widget(ConnectScreen(name='connect_screen'))
        self.title = 'Supervisório Pneumático'
        sm.current = 'connect_screen'
        app.sm = sm
        return sm
   
    def on_stop(self):
        self.main_screen.stop_refresh()

if __name__ == '__main__':
    Window.fullscreen = 'auto'

    for file in os.listdir("./kv"):
        if file.endswith(".kv"):
            Builder.load_string(open(os.path.join("./kv", file), encoding='utf-8').read(), rulesonly=True)
    app = MainApp()
    app.run()


