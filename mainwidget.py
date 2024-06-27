from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup, ScanPopup, DataGraphPopup
from kivy.core.window import Window
from threading import Thread
from time import sleep
from datetime import datetime
import random 
from modbusclient import CustomModbusClient
from timeseriesgraph import TimeSeriesGraph

tags = ['co.temp_carc', 'co.pit01', 'co.vel']

class MainWidget(BoxLayout):
    _updateThread = None
    _updateWidgets = True
    _data = {}
    _max_points = 20
    
    def __init__(self, **kwargs):
        super().__init__()
        self._server_ip = kwargs.get('server_ip')
        self._server_port = kwargs.get('server_port')
        self._scan_time = kwargs.get('scan_time')

        self._data['timestamp'] = None
        self._data['values'] = None

        self._modbusClient = CustomModbusClient(server_ip=self._server_ip, port=self._server_port)

        self._modbusPopup = ModbusPopup(self._server_ip, self._server_port)
        self._scanPopup = ScanPopup(scantime=self._scan_time)
        
        '''
        for key, value in kwargs.get('modbus_addrs').items():
            if key == 'co.pressao':
                plot_color = (1,0,0,1)
            else:
                plot_color = (random.random(),random.random(),random.random(),1)
            self._tags[key] = {'addr': value, 'color':plot_color}
        '''
        self._graph = DataGraphPopup(self._max_points, (1,0,0,1))
        
        
    def start_connection(self, ip, port):
        self._server_ip = ip
        self._server_port = port
        self._modbusClient.host = self._server_ip
        self._modbusClient.port = self._server_port
        try:
            Window.set_system_cursor("wait")
            self._modbusClient.open()
            Window.set_system_cursor("arrow")
            if self._modbusClient.open():
                self._updateThread = Thread(target=self.updater)
                self._updateThread.start()
                self.ids.img_con.source = 'imgs/conectado.png'
                self._modbusPopup.dismiss()
            else:
                self._modbusPopup.setInfo("Falha na conexão com o servidor.")
        except Exception as e:
            print("Erro: ", e.args)
    
    def updater(self):
        try:
            while self._updateWidgets:
                self._data['timestamp'] = datetime.now()
                data = self._modbusClient.fetch_data()
                print(data)
                self._data['values'] = data
                self.updateGUI()
                # Banco de dados
                sleep(self._scan_time / 1000)
        except Exception as e:
            print("Erro: ", e.args)

    def updateGUI(self):
        for t in tags:
            self.ids[t].text = str(self._data['values'][t])
        #Atualização do gráfico
        self._graph.ids.graph.updateGraph((self._data['timestamp'], self._data['values']['co.pit01']), 0)
    
    def stopRefresh(self):
        self._updateWidgets = False