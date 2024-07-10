from datetime import datetime, timedelta
from time import sleep
from threading import Thread

from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label

from database.models import DadoCLP

from widgets.datetimepicker import DatetimePickerWidget
from widgets.datagraph import DataGraphWidget

class DBScreen(Screen):
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
            item = BoxLayout(orientation='horizontal', size_hint=(1,None), height=30)
            
            checkbox = CheckBox()
            checkbox.bind(active=lambda a,b: self.update_gui())
            self._checkboxes[tag] = checkbox

            label = Label(text=tag, halign="left")

            item.add_widget(self._checkboxes[tag])
            item.add_widget(label)
            self.ids['tags'].add_widget(item)
        
        self._graph = self.ids['graph']
 
    def get_data(self, time_i, time_f, cols):
        cols.append('timestamp')
        columns = [getattr(DadoCLP, col) for col in cols]
        app = App.get_running_app()
        return app.session.query(*columns).filter(DadoCLP.timestamp.between(time_i, time_f)).all()

    def update_gui(self):
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
                d = reg.__dict__
                for tag in cols: data[tag].append((d['timestamp'], d[tag]))

            print(data)
                
            

    def set_time(self, setting):
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
        app = App.get_running_app()
        app.sm.transition.direction = 'right'
        if app.connected:
            app.sm.current = 'main_screen'
        else:
            app.sm.current = 'connect_screen'

    def update_clock(self):
        app = App.get_running_app()
        while self._update_clock:
            now = datetime.now()
            self.ids['time'].text = now.strftime('%H:%M:%S')
            self.ids['connected'].text = 'Status: ' + ('conectado' if app.connected else 'desconectado')
            sleep(1)