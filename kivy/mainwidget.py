from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup, ScanPopup, DataGraphPopup
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread
from time import sleep
from datetime import datetime
import random 
from timeseriesgraph import TimeSeriesGraph

class MainWidget(BoxLayout):
   
    _updateThread = None
    _updateWidgets = True
    _tags = {}
    _max_points = 20
    
    def __init__(self, **kwargs):
        super().__init__()
        self._scan_time = kwargs.get('scan_time')
        self._serverIP = kwargs.get('server_ip')
        self._serverPort = kwargs.get('server_port')
        self._modbusPopup = ModbusPopup(self._serverIP, self._serverPort)
        self._scanPopup = ScanPopup(scantime=self._scan_time)
        self._modbusClient = ModbusClient(host=self._serverIP, port=self._serverPort)
        self._meas = {}
        self._meas['timestamp'] = None
        self._meas['values'] = {}
        for key,value in kwargs.get('modbus_addrs').items():
            if key == 'co.pressao':
                plot_color = (1,0,0,1)
            else:
                plot_color = (random.random(),random.random(),random.random(),1)
            self._tags[key] = {'addr': value, 'color':plot_color}
        self._graph = DataGraphPopup(self._max_points, self._tags['co.pressao']['color'])
        
    def startDataRead(self, ip, port):
        self._serverIP = ip
        self._serverPort = port
        self._modbusClient.host = self._serverIP
        self._modbusClient.port = self._serverPort
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
                self.readData()
                self.updateGUI()
                # Banco de dados
                sleep(self._scan_time / 1000)
        except Exception as e:
            print("Erro: ", e.args)
    
    def readData(self):
        self._meas['timestamp'] = datetime.now()
        for key, value in self._tags.items():
            self._meas['values'][key] = self._modbusClient.read_holding_registers(value['addr'],1)[0]

    def updateGUI(self):
       for key,value in self._tags.items():
            self.ids[key].text = str(self._meas['values'][key])
        
        #Atualização do gráfico
            self._graph.ids.graph.updateGraph((self._meas['timestamp'],self._meas['values']['co.pressao']),0)
    
    def stopRefresh(self):
        self._updateWidgets = False