import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from kivy.core.window import Window

from database.db import Base, Session, engine

from screens.mainscreen import MainScreen
from screens.connectscreen import ConnectScreen
from screens.dbscreen import DBScreen

class MainApp(App):
    server_ip = '192.168.0.14'
    server_port = 502
    scan_time = 500
    connected = False

    def build(self):
        # Define o título da janela
        self.title = 'Supervisório Pneumático'

        # Inicializa o banco de dados
        Base.metadata.create_all(engine)
        self.session = Session()

        # Cria e adiciona as telas no ScreenManager
        self.main_screen = MainScreen(name='main_screen')
        self.db_screen = DBScreen(name='db_screen')
        sm = ScreenManager()
        sm.add_widget(self.main_screen)
        sm.add_widget(ConnectScreen(name='connect_screen'))
        sm.add_widget(self.db_screen)

        # Define ConnectScreen como a tela inicial
        sm.current = 'connect_screen'

        self.sm = sm
        return sm
   
    def on_stop(self):
        # Para as tarefas recursivas
        self.db_screen._update_clock = False
        self.main_screen.stop_refresh()

if __name__ == '__main__':
    # Abre a janela em tela cheia
    Window.fullscreen = 'auto'
    
    # Carrega todos os arquivos .kv
    for file in os.listdir("./kv"):
        if file.endswith(".kv"):
            Builder.load_string(open(os.path.join("./kv", file), encoding='utf-8').read(), rulesonly=True)
    
    app = MainApp()
    app.run()


