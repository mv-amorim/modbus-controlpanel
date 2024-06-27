from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder
from kivy.core.window import Window  # consigo definir o tamnho da janela

class MainApp(App):
    #'192.168.0.14'
    
    def build(self):
        self._widget = MainWidget(scan_time=500, server_ip='192.168.0.14', server_port=502)
        return self._widget
   
    def on_stop(self):
        self._widget.stopRefresh()
        
if __name__ == '__main__':
    Window.size=(650,500)  # mudo o tamanho da janela aqui
    Window.fullscreen = False  # o aplicativo roda em tela inteira se for True
    Builder.load_string(open("mainwidget.kv", encoding="utf-8").read(), rulesonly=True)
    Builder.load_string(open("popups.kv", encoding="utf-8").read(), rulesonly=True)
    MainApp().run()