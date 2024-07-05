from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy_garden.graph import LinePlot
from threading import Thread
from time import sleep
from datetime import datetime
from modbusclient import CustomModbusClient
from popups import SettingsPopup, DisconnectedPopup

from timeseriesgraph import TimeSeriesGraph
from sidebar import Sidebar

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
        self._disconnected_popup = DisconnectedPopup()
        self._plant_widget = self.ids['plant']
        self.sidebar = self.ids['sidebar']

        self._pit01_graph = self.ids['pit01_graph']
        plot = LinePlot(line_width=1.5, color=get_color_from_hex('#475CA7'))
        self._pit01_graph.add_plot(plot)
        self._pit01_graph.xmax = 20
                
    def start_connection(self):
        app = App.get_running_app()
        self._modbus_client.host = app.server_ip
        self._modbus_client.port = app.server_port
        try:
            Window.set_system_cursor("wait")
            self._modbus_client.open()
            Window.set_system_cursor("arrow")
            if self._modbus_client.is_open:
                self._update_thread = Thread(target=self.updater)
                self._update_thread.start()
                app.connected = True
                return True
            else:
                app.connected = False
        except Exception as e:
            print("Erro: ", e.args)
    
    def updater(self):
        app = App.get_running_app()
        try:
            while self._update_widgets:
                self._modbus_client.open()
                self._data['timestamp'] = datetime.now()
                data = self._modbus_client.fetch_data()
                self._data['values'] = data
                self.update_gui()
                # Banco de dados
                sleep(app.scan_time / 1000)
        except Exception as e:
            print("Erro: ", e.args)
            app.connected = False

    def update_gui(self):
        Clock.schedule_once(lambda dt: self._update_gui())

        eng_info = self.ids['eng_info']
        for tag in eng_info.ids:
            eng_info.ids[tag].text = str(self._data['values'][tag])
        
        #self.ids['co.fv01'].text = self._data['values']['co.fv01']
        fit2 = self._data['values']['co.fit02']
        fit3 = self._data['values']['co.fit03']
        self.ids['co.fit02'].text = f'{fit2:.1f}'
        self.ids['co.fit03'].text = f'{fit3:.1f}'
        
        match self._data['values']['co.sel_driver']:
            case 1:
                self.sidebar.ids['softstart'].state = 'down'
                self.sidebar.ids['invstart'].state = 'normal'
                self.sidebar.ids['dirstart'].state = 'normal'
            case 2:
                self.sidebar.ids['softstart'].state = 'normal'
                self.sidebar.ids['invstart'].state = 'down'
                self.sidebar.ids['dirstart'].state = 'normal'
            case 3:
                self.sidebar.ids['softstart'].state = 'normal'
                self.sidebar.ids['invstart'].state = 'normal'
                self.sidebar.ids['dirstart'].state = 'down'
        
        self._pit01_graph.updateGraph((self._data['timestamp'], self._data['values']['co.pit01']), 0)

    def _update_gui(self):
        app = App.get_running_app()
        if not app.connected:
            self._disconnected_popup.open()
        self.sidebar.ids['connected'].text = 'Status: ' + ('conectado' if app.connected else 'desconectado')
        
        self.sidebar.ids['inv_freq'].value = self._data['values']['co.freq']
        for i in range(1,7,1):
            open = self._data['values'][f'co.xv{i}'] == 1
            self._plant_widget.ids[f'xv{i}'].source = 'imgs/open_valve.png' if open else 'imgs/closed_valve.png'
            self.sidebar.ids[f'xv{i}_switch'].active = open

        match self._data['values']['co.sel_driver']:
            case 1:
                on = self._data['values']['co.soft_start'] == 1
            case 2:
                on = self._data['values']['co.inv_start'] == 1
            case 3:
                on = self._data['values']['co.dir_start'] == 1
        self._plant_widget.ids.engine.source = 'imgs/engine_on.png' if on else 'imgs/engine_off.png'
    
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
        self._plant_widget.set_engine('off')
        match self._data['values']['co.sel_driver']:
            case 1:
                self._modbus_client.set_softstart(0)
            case 2:
                self._modbus_client.set_invstart(0)
            case 3:
                self._modbus_client.set_dirstart(0)
    
    def reset_engine(self):
        self._plant_widget.set_engine('off')
        match self._data['values']['co.sel_driver']:
            case 1:
                self._modbus_client.set_softstart(2)
            case 2:
                self._modbus_client.set_invstart(2)
            case 3:
                self._modbus_client.set_dirstart(2)

    def switch_xv(self, i):
        xv = []
        for j in range(1,7,1):
            xv.append(self._data['values'][f'co.xv{j}'])
        xv[i-1] = 1 if xv[i-1] == 0 else 0
        self._plant_widget.ids[f'xv{i}'].source = 'imgs/closed_valve.png' if xv[i-1] == 0 else 'imgs/open_valve.png'
        self._modbus_client.set_xv(xv)