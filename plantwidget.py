from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.graphics.svg import Svg
from threading import Thread
from time import sleep
import xml.etree.ElementTree as ET

class PlantWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(PlantWidget, self).__init__(**kwargs)
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = False

        self._tree = ET.parse('imgs/plant.svg')
        self.add_widget(SvgWidget(tree=self._tree))

    def set_engine(self, state):
        #disable btn
        motor = self._tree.findall('''.//*[@id='motor']''')[0]
        match state:
            case 'on':
                motor.set('fill', '#F0F0F0')
            case 'off':
                motor.set('fill', '#808080')
        #enable btn
        self.reload()

    def set_xv(self, state, xv):
        valve = self._tree.findall(f'''.//*[@id='xv{xv}']''')[0]
        match state:
            case 'open':
                valve.set('fill', '#F0F0F0')
            case 'closed':
                valve.set('fill', '#808080')
        self.reload()

    def reload(self):
        #self.clear_widgets()
        print(self.children)
        #self.add_widget(SvgWidget(tree=self._tree))


class SvgWidget(Scatter):
    def __init__(self, tree, **kwargs):
        super().__init__(**kwargs)
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = False

        with self.canvas:
            svg = Svg()
            svg.set_tree(tree)

        self.scale = .75
        self.size = svg.width, svg.height