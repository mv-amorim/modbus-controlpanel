from pyModbusTCP.client import ModbusClient

float_tags_addrs = {
  'co.corrente_r': 840,
  'co.corrente_s': 841,
  'co.corrente_t': 842,
  'co.corrente_n': 843,
  'co.corrente_media': 845,
  'co.tensao_rs': 847,
  'co.tensao_st': 848,
  'co.tensao_tr': 849,
  'co.ativa_r': 852,
  'co.ativa_s': 853,
  'co.ativa_t': 854,
  'co.ativa_total': 855,
  'co.reativa_r': 856,
  'co.reativa_s': 857,
  'co.reativa_t': 858,
  'co.reativa_total': 859,
  'co.aparente_r': 860,
  'co.aparente_s': 861,
  'co.aparente_t': 862,
  'co.aparente_total': 863,
  'co.temp_r': 700,
  'co.temp_s': 702,
  'co.temp_t': 704,
  'co.temp_carc': 706,
  'co.pressao': 714,
  'co.fit02': 716,
  'co.fit03': 718,
  'co.torque': 1420,
}

int_tags_addrs = {
  'co.encoder': 884,
}

class ClienteMODBUS():
  """
  Classe Cliente MODBUS
  """
  def __init__(self, server_ip,porta,scan_time=1):
    """
    Construtor
    """
    self._cliente = ModbusClient(host=server_ip,port = porta)
    self._scan_time = scan_time

    def get_vel(self):
      
    
    def get_torque(self):
        

    def get_correntes(self):
      res = {
        'r': r,
        's': s,
        't': t,
        'n': n,
        'med': med
      }
      return res
    
    def get_pot_atv(self):
       return [r, s, t, tot]
    
    def get_pot_reat(self):
       return [r, s, t, tot]
    
    def get_pot_apar(self):
       return [r, s, t, tot]
    
    def get_freq(self):
       
       
    def get_tensoes(self):
       return [rs, st, tr, med]
    
    def get_temps(self):
       return [r, s, t, carc]

    def get_pressoes(self):
       return [pit01, fit02, fit03]
    
    #def get_fv01(self):

    def get_xv(self):
       return [xv1, xv2, xv3, xv4, xv5, xv6]

    def set_xv(self, xv):


    def get_softstart(self):


    def set_softstart(self, soft_s):
       
    
    def get_dirstart(self):
      
    
    def set_dirstart(self, dir_s):
       
    def get_invstart(self):
       
    def set_invstart(self, inv_s):

    def lerDado(self, tipo, addr):
        """
        Método para leitura de um dado da Tabela MODBUS
        """
        if tipo == 1:
            return self._cliente.read_holding_registers(addr,1)[0]

        if tipo == 2:
            return self._cliente.read_coils(addr,1)[0]

        if tipo == 3:
            return self._cliente.read_input_registers(addr,1)[0]

        if tipo == 4:
            return self._cliente.read_discrete_inputs(addr,1)[0]

    def escreveDado(self, tipo, addr, valor):
        """
        Método para a escrita de dados na Tabela MODBUS
        """
        if tipo == 1:
            return self._cliente.write_single_register(addr,valor)

        if tipo == 2:
            return self._cliente.write_single_coil(addr,valor)