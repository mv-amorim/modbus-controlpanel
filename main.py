from kivy.app import App
from mainscreen import MainScreen
from connectscreen import ConnectScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from kivy.core.window import Window  # consigo definir o tamnho da janela5
from kivy.config import Config

class MainApp(App):
    server_ip = '192.168.0.14'
    server_port = 502
    scan_time = 500

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main_screen'))
        self.sm.add_widget(ConnectScreen(name='connect_screen'))
        self.title = 'Supervisório Pneumático'
        self.sm.current = 'connect_screen'
        return self.sm
   
    def on_stop(self):
        self.sm.get_screen('main_screen').stop_refresh()
        
if __name__ == '__main__':
    Window.fullscreen = 'auto'  # o aplicativo roda em tela inteira se for auto
    #Window.size = (1920,1080)  # mudo o tamanho da janela aqui
    #Window.minimum_width = 1250
    #Window.minimum_height = 700
    #Config.set('graphics', 'resizable', 0)

    Builder.load_string(open('mainscreen.kv', encoding='utf-8').read(), rulesonly=True)
    Builder.load_string(open('connectscreen.kv', encoding='utf-8').read(), rulesonly=True)
    Builder.load_string(open('popups.kv', encoding='utf-8').read(), rulesonly=True)
    app = MainApp()
    app.run()


