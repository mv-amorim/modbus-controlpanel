from kivy_garden.graph import Graph
from kivy.clock import Clock

class TimeSeriesGraph(Graph):
    '''
    Classe derivada que implementa a possibilidade de se plotar 
    gráficos temporais 
    '''
    def __init__(self,**kwargs):
        '''
        Construtor
        '''
        super().__init__(**kwargs)
        self._trigger_time_label = Clock.create_trigger(self._add_time_labels)
        self._timestamps = []
        self._max_points = kwargs.get('max_points')
        self._max_points = 20
        self._numMeds = -1

    def update_x_labels(self,timestamps=None):
        '''
        Método para atualização do eixo das abscissas com os valores
        dos timestamps das amostras
        :param timestamps: vetor com os timestamps, caso não seja passado
        como argumento, será utilizado o vetor interno, que é atualizado por
        meio do método updateGraph
        '''
        if timestamps is not None:
            self._timestamps = timestamps
            if len(timestamps)>= 100:
                self.x_ticks_major = int(len(timestamps)/10)
            else:
                self.x_ticks_major = 5
        self._trigger_time_label()

    
    def clear_label(self,*args):
        '''
        Método que apaga os rótulos do eixo das abscissas
        '''
        for lb in self._x_grid_label:
                lb.text = ''
    
    def clear_plots(self):
        '''
        Método que apaga os plots do gráfico
        '''
        try:
            while len(self.plots) != 0:
                self.remove_plot(self.plots[0])
        except Exception as e:
            print(e.args)

    def _add_time_labels(self, *args):
        '''
        Método privado utilizado para atualizar os rótulos do
        eixo das abscissas de acordo com o vetor de timestamps.
        Este método é invocado por meio do trigger _trigger_time_label
        '''
        try:  
            labels = self._timestamps[0:len(self._timestamps):self.x_ticks_major] 
            for i in range(0,min(len(self._x_grid_label),len(labels))):
                self._x_grid_label[i].text = str(labels[i].strftime("%H:%M:%S"))
        except Exception as e:
            print('Error: ',e.args)
    
    def set_max_points(self, mp, plot_number):
        '''
        Método utilizado para definir o número máximo de pontos de um 
        determinado plot.
        :param mp: número máximo de pontos desejado
        :param plot_number: número do plot em que se deseja alterar o número 
        de pontos
        '''
        try:
            self._max_points = mp
            if mp == 100:
                self.x_ticks_major = 10
            else:
                self.x_ticks_major = 5
            if len(self.plots[plot_number].points) < self._max_points:
                self.xmax = min(self.plots[plot_number].points)[0] + self._max_points - 1
            self.plots[plot_number].points = self.plots[plot_number].points[-self._max_points:]
            self._timestamps = self._timestamps[-self._max_points:]
        except Exception as e:
            print(e.args)
    
    def update_graph(self, meas, plot_number):
        '''
        Método que atualiza os dados de um determinado gráfico
        :param meas: tupla com a medição no formato (datetime,valor)
        :param plot_number: número do plot que será atualizado
        '''
        try:
           
            if len(self._timestamps)==0 or meas[0] != self._timestamps[-1]:
                self._timestamps.append(meas[0])
                self._timestamps = self._timestamps[-self._max_points:]
                self._numMeds += 1
                # Verifica se o número de pontos é maior que zero para atribuir corretamente o índice da medição
                self.plots[plot_number].points.append((self._numMeds,meas[1]))    
                    
                # Verifica se o número de pontos é maior que o número máximo e remove os pontos mais antigos
                self.plots[plot_number].points = self.plots[plot_number].points[-self._max_points:] 
                # Atualiza o label da medição mais antiga
                self.xmin = min(self.plots[plot_number].points)[0]

                # Atualiza o label da medição mais recente  
                if len(self.plots[plot_number].points) >= self._max_points:
                    self.xmax = max(self.plots[plot_number].points)[0]
                else:
                    Clock.schedule_once(self.clear_label)
                self.update_x_labels()
            else:
                # Verifica se o número de pontos é maior que zero para atribuir corretamente o índice da medição
                self.plots[plot_number].points.append((self._numMeds,meas[1]))    
                    
                # Verifica se o número de pontos é maior que o número máximo e remove os pontos mais antigos
                self.plots[plot_number].points = self.plots[plot_number].points[-self._max_points:]                
        except Exception as e:
            print(e.args)