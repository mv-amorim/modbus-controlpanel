from datetime import datetime, timedelta
from time import sleep
from threading import Thread

from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from database.models import DadoCLP

from widgets.datetimepicker import DatetimePickerWidget
from widgets.datagraph import DataGraphWidget

class DBScreen(Screen):
    '''
    Tela de consulta de dados
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._time_i = self.ids['time_i']
        self._time_f = self.ids['time_f']
        self._time_i.submit = self.update_gui
        self._time_f.submit = self.update_gui

        self._update_clock = True
        self._clock_thread = Thread(target=self.update_clock)
        self._clock_thread.start()

        self._checkboxes = {}
        self._keys = DadoCLP.__table__.columns.keys()[2:]
        for tag in self._keys:
            checkitem = CheckItem(text=tag)
            checkbox = checkitem.ids['checkbox']
            checkbox.bind(active=lambda a,b: self.update_gui())
            self._checkboxes[tag] = checkbox
            self.ids['tags'].add_widget(checkitem)
        
        self._graph = self.ids['graph']
        self.set_time('24h')
 
    def get_data(self, time_i, time_f, cols):
        '''
        Método para obter dados do banco
        '''
        columns = [getattr(DadoCLP, col) for col in cols]
        columns.append(DadoCLP.timestamp)
        app = App.get_running_app()
        return app.session.query(*columns).filter(DadoCLP.timestamp.between(time_i, time_f)).all()

    def update_gui(self):
        '''
        Método para atualizar a interface (gráfico e legendas)
        '''
        time_i = self._time_i.get_val()
        time_f = self._time_f.get_val()
        
        cols = []
        for tag in self._keys:
            if self._checkboxes[tag].active:
                cols.append(tag)
    
        if time_i and time_f and cols.__len__() > 0:
            res = self.get_data(time_i, time_f, cols)
            
            data = {}
            for tag in cols: data[tag] = []

            for reg in res:
                for tag in cols: data[tag].append((getattr(reg,'timestamp').timestamp(), getattr(reg, tag)))
            
            self._graph.update_plots(data)
        else:
            self._graph.clear()
            

    def set_time(self, setting):
        '''
        Método para atualizar o intervalo de tempo conforme os botões indicam
        '''
        now = datetime.now()
        self._time_f.set_val(now)
        match setting:
            case '1w':
                self._time_i.set_val(now - timedelta(days=7))
            case '24h':
                self._time_i.set_val(now - timedelta(days=1))
            case '1h':
                self._time_i.set_val(now - timedelta(hours=1))
            case '10min':
                self._time_i.set_val(now - timedelta(minutes=10))
        self.update_gui()
    
    def back(self):
        '''
        Método para voltar à tela anterior
        '''
        app = App.get_running_app()
        app.sm.transition.direction = 'right'
        if app.connected:
            app.sm.current = 'main_screen'
        else:
            app.sm.current = 'connect_screen'

    def update_clock(self):
        '''
        Método para atualizar o relógio
        '''
        app = App.get_running_app()
        while self._update_clock:
            now = datetime.now()
            self.ids['time'].text = now.strftime('%H:%M:%S')
            self.ids['connected'].text = 'Status: ' + ('conectado' if app.connected else 'desconectado')
            sleep(1)

class CheckItem(BoxLayout):
    '''
    Widget de CheckBox + Label
    '''
    text = StringProperty()