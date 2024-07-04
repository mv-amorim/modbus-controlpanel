from kivy.uix.scatter import Scatter
from kivy.graphics.svg import Svg
from xml.etree.cElementTree import parse

class PlantWidget(Scatter):
    def __init__(self, **kwargs):
        super(PlantWidget, self).__init__(**kwargs)
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = False

        self._tree = parse('imgs/plant.svg')

        with self.canvas:
            svg = Svg()
            svg.set_tree(self._tree)

        self.svg = svg
        self.scale = .75
        self.size = svg.width, svg.height

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
        self.svg.set_tree(self._tree)
