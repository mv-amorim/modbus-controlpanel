import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from kivy.core.window import Window

from database.db import Base, Session, engine

from screens.mainscreen import MainScreen
from screens.connectscreen import ConnectScreen
from screens.dbscreen import DBScreen

global app

class MainApp(App):
    server_ip = '192.168.0.14'
    server_port = 502
    scan_time = 500
    connected = False

    def build(self):
        self.title = 'Supervisório Pneumático'

        Base.metadata.create_all(engine)
        self.session = Session()

        self.main_screen = MainScreen(name='main_screen')
        self.db_screen = DBScreen(name='db_screen')
        
        sm = ScreenManager()
        sm.add_widget(self.main_screen)
        sm.add_widget(ConnectScreen(name='connect_screen'))
        sm.add_widget(self.db_screen)
        sm.current = 'connect_screen'
        self.sm = sm

        return sm
   
    def on_stop(self):
        self.db_screen._update_clock = False
        self.main_screen.stop_refresh()

if __name__ == '__main__':
    Window.fullscreen = 'auto'

    for file in os.listdir("./kv"):
        if file.endswith(".kv"):
            Builder.load_string(open(os.path.join("./kv", file), encoding='utf-8').read(), rulesonly=True)
    app = MainApp()
    app.run()


