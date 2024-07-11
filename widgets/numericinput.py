from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.textinput import TextInput

class NumericInput(TextInput):
    '''
    Widget para inserção de valores númericos (usado para inserir a data e a hora)
    '''

    min_value = NumericProperty()
    max_value = NumericProperty()
    validate = BooleanProperty(True)

    def __init__(self, *args, **kwargs):
        TextInput.__init__(self, *args, **kwargs)
        self.input_filter = 'int'
        self.multiline = False
        self.write_tab = False

    def insert_text(self, string, from_undo=False):
        '''
        Valida os dados assim que inseridos
        '''
        new_text = self.text + string
        if new_text != "":
            if self.validate:
                if self.min_value <= float(new_text) <= self.max_value:
                    TextInput.insert_text(self, string, from_undo=from_undo)
            else:
                TextInput.insert_text(self, string, from_undo=from_undo)