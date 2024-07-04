from kivy.uix.screenmanager import Screen
from popups import SettingsPopup, DataGraphPopup
from kivy.core.window import Window
from plantwidget import PlantWidget
from threading import Thread
from time import sleep
from datetime import datetime
import random 
from modbusclient import CustomModbusClient
from timeseriesgraph import TimeSeriesGraph
from kivy.app import App

tags = ['co.torque', 'co.vel', 'co.temp_r', 'co.temp_s', 'co.temp_t', 'co.temp_carc']

class MainScreen(Screen):
    _update_thread = None
    _update_widgets = True
    _data = {}
    _max_points = 20
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._data['timestamp'] = None
        self._data['values'] = None

        app = App.get_running_app()
        self._modbus_client = CustomModbusClient(server_ip=app.server_ip, port=app.server_port)
        self._settings_popup = SettingsPopup()
        self._plant_widget = PlantWidget()

        for i in range(1,7,1):
            self.ids[f'xv{i}_switch'].bind(active=lambda: self.set_xv(i))
        
        '''
        for key, value in kwargs.get('modbus_addrs').items():
            if key == 'co.pressao':
                plot_color = (1,0,0,1)
            else:
                plot_color = (random.random(),random.random(),random.random(),1)
            self._tags[key] = {'addr': value, 'color':plot_color}
        '''
        self._graph = DataGraphPopup(self._max_points, (1,0,0,1))
        
    def start_connection(self):
        app = App.get_running_app()
        self._modbus_client.host = app.server_ip
        self._modbus_client.port = app.server_port
        try:
            Window.set_system_cursor("wait")
            self._modbus_client.open()
            Window.set_system_cursor("arrow")
            if self._modbus_client.open():
                self._update_thread = Thread(target=self.updater)
                self._update_thread.start()
                self.ids.img_con.source = 'imgs/conectado.png'
                return True
            else:
                pass
                #alert("Falha na conexão com o servidor.")
        except Exception as e:
            print("Erro: ", e.args)
    
    def updater(self):
        app = App.get_running_app()
        try:
            while self._update_widgets:
                self._data['timestamp'] = datetime.now()
                data = self._modbus_client.fetch_data()
                self._data['values'] = data
                self.update_gui()
                # Banco de dados
                sleep(app.scan_time / 1000)
        except Exception as e:
            print("Erro: ", e.args)

    def update_gui(self):
        for t in tags:
            self.ids[t].text = str(self._data['values'][t])
        
        match self._data['values']['co.sel_driver']:
            case 1:
                self.ids['softstart'].state = 'down'
            case 2:
                self.ids['invstart'].state = 'down'
            case 3:
                self.ids['dirstart'].state = 'down'

        self.ids['inv_freq'].value = self._data['values']['co.freq']
        
        for i in range(1,7,1):
            open = self._data['values'][f'co.xv{i}'] == 1
            self._plant_widget.set_xv('open' if open else 'closed', i)
            self.ids[f'xv{i}_switch'].active = open
        
        #Atualização do gráfico
        self._graph.ids.graph.updateGraph((self._data['timestamp'], self._data['values']['co.pit01']), 0)
    
    def stop_refresh(self):
        self._modbus_client.close()
        self._update_widgets = False
    
    def start_engine(self):
        self._plant_widget.set_engine('on')
        match self._data['values']['co.sel_driver']:
            case 1:
                self._modbus_client.set_softstart(1)
            case 2:
                self._modbus_client.set_invstart(1)
            case 3:
                self._modbus_client.set_dirstart(1)
    
    def stop_engine(self):
        #self._plant_widget.set_engine('off')
        match self._data['values']['co.sel_driver']:
            case 1:
                self._modbus_client.set_softstart(0)
            case 2:
                self._modbus_client.set_invstart(0)
            case 3:
                self._modbus_client.set_dirstart(0)
    
    def reset_engine(self):
        #self._plant_widget.set_engine('off')
        match self._data['values']['co.sel_driver']:
            case 1:
                self._modbus_client.set_softstart(2)
            case 2:
                self._modbus_client.set_invstart(2)
            case 3:
                self._modbus_client.set_dirstart(2)

    def switch_xv(self, i):
        xv = self._modbus_client.get_xv()
        xv[i-1] = 0 if xv[i-1] == 1 else 1
        self._modbus_client.set_xv(xv)