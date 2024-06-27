from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder
from kivy.core.window import Window  # consigo definir o tamnho da janela
from time import sleep
from modbusclient import EnhancedModbusClient

class MainApp(App):    
    def build(self):
        self._widget = MainWidget(scan_time=500, server_ip='192.168.0.14', server_port=502)
        self.title = 'Supervisório Pneumático'
        return self._widget
   
    def on_stop(self):
        self._widget.stopRefresh()
        
if __name__ == '__main__':
    Window.size=(650,500)  # mudo o tamanho da janela aqui
    Window.fullscreen = False  # o aplicativo roda em tela inteira se for True

    Builder.load_string(open('mainwidget.kv', encoding='utf-8').read(), rulesonly=True)
    Builder.load_string(open('popups.kv', encoding='utf-8').read(), rulesonly=True)
    app = MainApp()
    app.run()

    sleep(5)
    client = EnhancedModbusClient(server_ip='192.168.0.14', port=502)
    client.set_seldriver(2)
    client.set_freq(60)
    client.set_invstart(1)
    print(client.fetch_data())

    sleep(10)
    client.set_freq(30)

    sleep(15)
    client.set_invstart(0)
    
    sleep(3)
    client.set_xv([0,1,0,0,0,0])
    sleep(1.5)
    client.set_xv([0,0,1,0,0,0])
    sleep(1.5)
    client.set_xv([0,0,0,1,0,0])
    sleep(1.5)
    client.set_xv([0,0,0,0,1,0])
    sleep(1.5)
    client.set_xv([0,0,0,0,0,1])
    sleep(1.5)
    client.set_xv([0,0,0,0,0,0])
