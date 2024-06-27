from pyModbusTCP.client import ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

class EnhancedModbusClient(ModbusClient):
    """
    Classe Cliente MODBUS
    """
    def __init__(self, server_ip, port):
        super().__init__(host=server_ip, port=port)

    #def get_fv01(self):
      
    def get_torque(self):
        registers = self.read_holding_registers(1420, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        res = decoder.decode_32bit_float()
        return res

    def get_correntes(self):
        registers = self.read_holding_registers(840, 4)
        decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        r = decoder.decode_16bit_int() / 10
        s = decoder.decode_16bit_int() / 10
        t = decoder.decode_16bit_int() / 10
        n = decoder.decode_16bit_int() / 10

        med = self.read_holding_registers(845, 1)[0] / 10

        res = { 'r': r, 's': s, 't': t, 'n': n, 'med': med }
        return res
    
    def get_pot_atv(self):
        registers = self.read_holding_registers(852, 4)
        decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        r = decoder.decode_16bit_int()
        s = decoder.decode_16bit_int()
        t = decoder.decode_16bit_int()
        tot = decoder.decode_16bit_int()
        return { 'r': r, 's': s, 't': t, 'tot': tot }
    
    def get_pot_reat(self):
        registers = self.read_holding_registers(856, 4)
        decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        r = decoder.decode_16bit_int()
        s = decoder.decode_16bit_int()
        t = decoder.decode_16bit_int()
        tot = decoder.decode_16bit_int()
        return { 'r': r, 's': s, 't': t, 'tot': tot }
    
    def get_pot_apar(self):
        registers = self.read_holding_registers(860, 4)
        decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        r = decoder.decode_16bit_int()
        s = decoder.decode_16bit_int()
        t = decoder.decode_16bit_int()
        tot = decoder.decode_16bit_int()
        return { 'r': r, 's': s, 't': t, 'tot': tot }
    
    def get_vel(self):
        registers = self.read_holding_registers(884, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        res = decoder.decode_32bit_float()
        return res
       
    def get_tensoes(self):
        registers = self.read_holding_registers(847, 3, )
        decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        rs = decoder.decode_16bit_int() / 10
        st = decoder.decode_16bit_int() / 10
        tr = decoder.decode_16bit_int() / 10
        return { 'rs': rs, 'st': st, 'tr': tr }
    
    def get_temps(self):
        registers = self.read_holding_registers(700, 8)
        decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        r = decoder.decode_32bit_float() / 10
        s = decoder.decode_32bit_float() / 10
        t = decoder.decode_32bit_float() / 10
        carc = decoder.decode_32bit_float() / 10
        return { 'r': r, 's': s, 't': t, 'carc': carc }

    def get_pressoes(self):
        registers = self.read_holding_registers(714, 6)
        decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        pit01 = decoder.decode_32bit_float()
        fit02 = decoder.decode_32bit_float()
        fit03 = decoder.decode_32bit_float()
        return { 'pit01': pit01, 'fit02': fit02, 'fit03': fit03 }

    def get_xv(self):
        bits = self.read_holding_registers(712, 1)[0]
        bits = [int(x) for x in bin(bits)[2:]]
        return bits[11:16]

    def set_xv(self, xv):
        bits = [0] * 16
        bits[15] = xv[0]
        bits[14] = xv[1]
        bits[13] = xv[2]
        bits[12] = xv[3]
        bits[11] = xv[4]
        bits[10] = xv[5]
        s = ''.join(str(x) for x in bits)
        self.write_single_register(712, int(s, 2))
        return xv

    def get_softstart(self):
        res = self.read_holding_registers(1316, 1)[0]
        return res

    def set_softstart(self, soft_s):
        if soft_s in [0, 1, 2]:
            self.write_single_register(1316, soft_s)
            return soft_s
        else:
            return
    
    def get_dirstart(self):
        res = self.read_holding_registers(1319, 1)[0]
        return res
    
    def set_dirstart(self, dir_s):
        if dir_s in [0, 1, 2]:
            self.write_single_register(1319, dir_s)
            return dir_s
        else:
            return
        
    def get_invstart(self):
        res = self.read_holding_registers(1312, 1)[0]
        return res
       
    def set_invstart(self, inv_s):
        if inv_s in [0, 1, 2]:
            self.write_single_register(1312, inv_s)
            return inv_s
        else:
            return
       
    def get_seldriver(self):
        res = self.read_holding_registers(1324, 1)[0]
        return res
       
    def set_seldriver(self, start):
        if start in [1, 2, 3]:
            self.write_single_register(1324, start)
            return start
        else:
            return
        
    def get_freq(self):
        res = self.read_holding_registers(1313, 1)[0] / 10
        return res
       
    def set_freq(self, vel):
        if vel >= 0 and vel <= 60:
            self.write_single_register(1313, vel*10)
            return vel
        else:
            return
        
    def fetch_data(self):
        res = {}
        res['co.vel'] = self.get_vel()
        res['co.sel_driver'] = self.get_seldriver()
        res['co.inv_start'] = self.get_invstart()
        res['co.dir_start'] = self.get_dirstart()
        res['co.soft_start'] = self.get_softstart()
        res['co.torque'] = self.get_torque()

        res = res | self.get_pressoes()
        res = res | {f'co.xv${i}': xv for i, xv in self.get_xv()}
        res = res | {f'co.temp_${k}': v for k, v in self.get_temps()}
        res = res | {f'co.tensao_${k}': v for k, v in self.get_tensoes()}
        res = res | {f'co.ativa_${k}': v for k, v in self.get_pot_atv()}
        res = res | {f'co.reativa_${k}': v for k, v in self.get_pot_reat()}
        res = res | {f'co.aparente_${k}': v for k, v in self.get_pot_apar()}
        res = res | {f'co.corrente_${k}': v for k, v in self.get_correntes()}

        return res

        