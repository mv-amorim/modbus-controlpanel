from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from widgets.numericinput import NumericInput

class DatetimePickerWidget(BoxLayout):
    on_enter = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def submit(self):
        if self.on_enter:
            self.on_enter()
    
    def get_val(self):
        for k in self.ids.keys():
            if self.ids[k].text == "":
                return None

        dd = int(self.ids['D'].text)
        mm = int(self.ids['M'].text)
        yy = int(self.ids['Y'].text)
        h = int(self.ids['h'].text)
        m = int(self.ids['m'].text)

        return datetime(year=yy, month=mm, day=dd, hour=h, minute=m, second=59)

    def set_val(self, dtm):
        self.ids['D'].text = str(dtm.day)
        self.ids['M'].text = str(dtm.month)
        self.ids['Y'].text = str(dtm.year)
        self.ids['h'].text = str(dtm.hour)
        self.ids['m'].text = str(dtm.minute)