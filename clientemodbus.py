from pyModbusTCP.client import ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

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
    def __init__(self, server_ip, porta, scan_time=1):
        """
        Construtor
        """
        self._client = ModbusClient(host=server_ip,port = porta)
        self._scan_time = scan_time

    def get_vel(self):

        return
      
    def get_torque(self):
        data = self._client.read_holding_registers(1420, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        res = decoder.decode_32bit_float()
        return res

    def get_correntes(self):
        res = { 'r': r, 's': s, 't': t, 'n': n, 'med': med }
        return res
    
    def get_pot_atv(self):
        return [r, s, t, tot]
    
    def get_pot_reat(self):
        return [r, s, t, tot]
    
    def get_pot_apar(self):
        return [r, s, t, tot]
    
    def get_freq(self):
        data = self._client.read_holding_registers(884, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        res = decoder.decode_32bit_float()
        return res
       
    def get_tensoes(self):
        return [rs, st, tr, med]
    
    def get_temps(self):
        return [r, s, t, carc]

    def get_pressoes(self):
        return [pit01, fit02, fit03]
    
    #def get_fv01(self):

    def get_xv(self):
        data = self._client.read_holding_registers(712, 1)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        bits = decoder.decode_bits()
        return bits[:5]

    def set_xv(self, xv):
        builder = BinaryPayloadBuilder()
        builder.add_bits(xv)
        regs = builder.to_registers
        self._client.write_multiple_registers(712, regs)
        return xv

    def get_softstart(self):
        data = self._client.read_holding_registers(1316, 1)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        res = decoder.decode_16bit_uint()
        return res

    def set_softstart(self, soft_s):
        if soft_s in [0, 1, 2]:
            builder = BinaryPayloadBuilder()
            builder.add_8bit_uint(soft_s)
            regs = builder.to_registers
            self._client.write_multiple_registers(1316, regs)
            return soft_s
        else:
            return
    
    def get_dirstart(self):
        data = self._client.read_holding_registers(1319, 1)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        res = decoder.decode_16bit_uint()
        return res
    
    def set_dirstart(self, dir_s):
        if dir_s in [0, 1, 2]:
            builder = BinaryPayloadBuilder()
            builder.add_8bit_uint(dir_s)
            regs = builder.to_registers
            self._client.write_multiple_registers(1319, regs)
            return dir_s
        else:
            return
       
    def get_start(self):
        data = self._client.read_holding_registers(1324, 1)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        res = decoder.decode_16bit_uint()
        return res
       
    def set_start(self, start):
        if start in [1, 2, 3]:
            builder = BinaryPayloadBuilder()
            builder.add_8bit_uint(start)
            regs = builder.to_registers
            self._client.write_multiple_registers(1324, regs)
            return start
        else:
            return