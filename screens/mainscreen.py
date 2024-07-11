from threading import Thread, Lock
from time import sleep
from datetime import datetime

from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock

from database.models import DadoCLP
from modbusclient import CustomModbusClient

from popups import SettingsPopup, DisconnectedPopup
from widgets.sparkline import SparklineWidget
from widgets.sidebar import SidebarWidget

class MainScreen(Screen):
    '''
    Tela principal do supervisório
    '''

    _update_thread = None
    _do_refresh = True
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
        self._sidebar = self.ids['sidebar']

    def start_connection(self):
        '''
        Método para iniciar a conexão com o servidor MODBUS
        '''
        app = App.get_running_app()
        self._modbus_client.host = app.server_ip
        self._modbus_client.port = app.server_port
        try:
            Window.set_system_cursor("wait")
            self._modbus_client.open()
            Window.set_system_cursor("arrow")
            if self._modbus_client.is_open:
                self._lock = Lock()
                self._update_thread = Thread(target=self.updater)
                self._update_thread.start()
                app.connected = True
                return True
            else:
                app.connected = False
        except Exception as e:
            print("Erro: ", e.args)
    
    def updater(self):
        '''
        Método para obter dados a ser executado em segundo plano
        '''
        app = App.get_running_app()
        try:
            while self._do_refresh:
                self._modbus_client.open()
                self._data['timestamp'] = datetime.now()
                data = self._modbus_client.fetch_data()
                self._data['values'] = data
                self.update_gui()
                self.store_data(session=app.session)
                # Banco de dados
                sleep(app.scan_time / 1000)
        except Exception as e:
            print("Erro: ", e.args)
            app.connected = False

    def update_gui(self):
        '''
        Método para atualizar a interface em segundo plano
        '''
        Clock.schedule_once(lambda dt: self._update_gui())

        eng_info = self.ids['eng_info']
        for tag in eng_info.ids:
            eng_info.ids[tag].text = str(self._data['values'][tag])

        table_pot = self.ids['table_pot']
        for tag in table_pot.ids:
            table_pot.ids[tag].text = str(self._data['values'][tag])
        
        #self.ids['co.fv01'].text = self._data['values']['co.fv01']
        fit2 = self._data['values']['co.fit02']
        fit3 = self._data['values']['co.fit03']
        self.ids['co.fit02'].text = f'{fit2:.1f}'
        self.ids['co.fit03'].text = f'{fit3:.1f}'
        
        match self._data['values']['co.sel_driver']:
            case 1:
                self._sidebar.ids['softstart'].state = 'down'
                self._sidebar.ids['invstart'].state = 'normal'
                self._sidebar.ids['dirstart'].state = 'normal'
            case 2:
                self._sidebar.ids['softstart'].state = 'normal'
                self._sidebar.ids['invstart'].state = 'down'
                self._sidebar.ids['dirstart'].state = 'normal'
            case 3:
                self._sidebar.ids['softstart'].state = 'normal'
                self._sidebar.ids['invstart'].state = 'normal'
                self._sidebar.ids['dirstart'].state = 'down'
        
    def _update_gui(self):
        '''
        Método para atualizar a interface na Thread principal
        '''
        app = App.get_running_app()
        if not app.connected:
            self._disconnected_popup.open()
        self._sidebar.ids['connected'].text = 'Status: ' + ('conectado' if app.connected else 'desconectado')
        
        self._sidebar.ids['inv_freq'].value = self._data['values']['co.freq']

        for i in range(1,7,1):
            open = self._data['values'][f'co.xv{i}'] == 1
            self._plant_widget.ids[f'xv{i}'].source = 'imgs/open_valve.png' if open else 'imgs/closed_valve.png'
            self._sidebar.ids[f'xv{i}_switch'].active = open

        match self._data['values']['co.sel_driver']:
            case 1:
                on = self._data['values']['co.soft_start'] == 1
            case 2:
                on = self._data['values']['co.inv_start'] == 1
            case 3:
                on = self._data['values']['co.dir_start'] == 1
        self._plant_widget.ids.engine.source = 'imgs/engine_on.png' if on else 'imgs/engine_off.png'
        
        self.ids['co.pit01'].update_val(self._data['values']['co.pit01'])

    def store_data(self, session):
        '''
        Método para armazenar os dados no banco
        '''
        try:
            data = {
                'timestamp': self._data['timestamp']
            }

            keys = DadoCLP.__table__.columns.keys()
            for key in keys[2:]:
                data[key] = self._data['values'][f'co.{key}']

            dadoCLP = DadoCLP(**data)
            with self._lock:
                session.add(dadoCLP)
                session.commit()
        except Exception as e:
            print("Erro: ", e.args)
            
    def stop_refresh(self):
        self._do_refresh = False
        self._sidebar.stop_refresh()
        self._modbus_client.close()


    def start_engine(self):
        '''
        Método para ligar o motor de acordo com o driver selecionado
        '''
        self._plant_widget.ids['engine'].source = 'imgs/engine_on.png'
        match self._data['values']['co.sel_driver']:
            case 1:
                self._modbus_client.set_softstart(1)
            case 2:
                self._modbus_client.set_invstart(1)
            case 3:
                self._modbus_client.set_dirstart(1)
    
    def stop_engine(self):
        '''
        Método para desligar o motor de acordo com o driver selecionado
        '''
        self._plant_widget.ids['engine'].source = 'imgs/engine_off.png'
        match self._data['values']['co.sel_driver']:
            case 1:
                self._modbus_client.set_softstart(0)
            case 2:
                self._modbus_client.set_invstart(0)
            case 3:
                self._modbus_client.set_dirstart(0)
    
    def reset_engine(self):
        '''
        Método para resetar o motor de acordo com o driver selecionado
        '''
        self._plant_widget.ids['engine'].source = 'imgs/engine_off.png'
        match self._data['values']['co.sel_driver']:
            case 1:
                self._modbus_client.set_softstart(2)
            case 2:
                self._modbus_client.set_invstart(2)
            case 3:
                self._modbus_client.set_dirstart(2)

    def switch_xv(self, i):
        '''
        Método para comutar uma válvula
        '''
        xv = []
        for j in range(1,7,1):
            xv.append(self._data['values'][f'co.xv{j}'])
        xv[i-1] = 1 if xv[i-1] == 0 else 0
        self._plant_widget.ids[f'xv{i}'].source = 'imgs/closed_valve.png' if xv[i-1] == 0 else 'imgs/open_valve.png'
        self._modbus_client.set_xv(xv)