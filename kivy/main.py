from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder
from kivy.core.window import Window  # consigo definir o tamnho da janela

class MainApp(App):
    
    def build(self):
        self._widget = MainWidget(scan_time=1000, server_ip='localhost', server_port=502,
            modbus_addrs = {         
                'co.temp_carc': 706,
                'co.pressao': 714,
                'co.encoder': 884,
                'co.corrente_r': 840,
                'co.corrente_s': 841,
                'co.corrente_t': 842,
                'co.corrente_n': 843,
                'co.corrente_media': 845,
                'co.tensao_rs': 847,
                'co.tensao_st': 848,
                'co.tensao_tr': 849,
                'co.ativa_r': 852,
                'co.ativa_s': 853,
                'co.ativa_t': 854,
                'co.ativa_total': 855,
                'co.reativa_r': 856,
                'co.reativa_s': 857,
                'co.reativa_t': 858,
                'co.reativa_total': 859,
                'co.aparente_r': 860,
                'co.aparente_s': 861,
                'co.aparente_t': 862,
                'co.aparente_total': 863,
                'co.temp_r': 700,
                'co.temp_s': 702,
                'co.temp_t': 704,
                'co.fit02': 716,
                'co.fit03': 718,
                'co.torque': 1420,
            }
        )
        return self._widget
   
    def on_stop(self):
        self._widget.stopRefresh()
        
if __name__ == '__main__':
    Window.size=(650,500)  # mudo o tamanho da janela aqui
    Window.fullscreen = False  # o aplicativo roda em tela inteira se for True
    Builder.load_string(open("mainwidget.kv", encoding="utf-8").read(),rulesonly=True)
    Builder.load_string(open("popups.kv", encoding="utf-8").read(),rulesonly=True)
    MainApp().run()

'''
    modbus_addrs = {
        'co.corrente_r': 840,
        'co.corrente_s': 841,
        'co.corrente_t': 842,
        'co.corrente_n': 843,
        'co.corrente_media': 845,
        'co.tensao_rs': 847,
        'co.tensao_st': 848,
        'co.tensao_tr': 849,
        'co.ativa_r': 852,
        'co.ativa_s': 853,
        'co.ativa_t': 854,
        'co.ativa_total': 855,
        'co.reativa_r': 856,
        'co.reativa_s': 857,
        'co.reativa_t': 858,
        'co.reativa_total': 859,
        'co.aparente_r': 860,
        'co.aparente_s': 861,
        'co.aparente_t': 862,
        'co.aparente_total': 863,
        'co.temp_r': 700,
        'co.temp_s': 702,
        'co.temp_t': 704,
        'co.temp_carc': 706,
        'co.pressao': 714,
        'co.fit02': 716,
        'co.fit03': 718,
        'co.torque': 1420,
        'co.encoder': 884,
    }  
'''