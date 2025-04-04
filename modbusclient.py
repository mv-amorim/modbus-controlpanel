import random
from pyModbusTCP.client import ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

class CustomModbusClient(ModbusClient):
    '''
    Classe Cliente MODBUS
    '''

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
        num = self.read_holding_registers(712, 1)[0]
        bits = [int(x) for x in bin(num)[2:].zfill(16)]
        bits = bits[::-1]
        xv = bits[:6]
        return xv

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
            self.write_single_register(1313, int(vel*10))
            return vel
        else:
            return
    
    def fetch_data(self):
        '''
        Retorna um dicionário contendo todos os dados
        '''

        res = {}
        res['co.vel'] = self.get_vel()
        res['co.freq'] = self.get_freq()
        res['co.sel_driver'] = self.get_seldriver()
        res['co.inv_start'] = self.get_invstart()
        res['co.dir_start'] = self.get_dirstart()
        res['co.soft_start'] = self.get_softstart()
        res['co.torque'] = self.get_torque()
        #res['co.fv01'] = self.get_fv01()

        tmp = self.get_pressoes()
        res = res | {f'co.{k}': tmp[k] for k in tmp.keys()}

        tmp = self.get_xv()
        res = res | {f'co.xv{i}': tmp[i-1] for i in range(1,7,1)}

        tmp = self.get_temps()
        res = res | {f'co.temp_{k}': tmp[k] for k in tmp.keys()}

        tmp = self.get_tensoes()
        res = res | {f'co.tensao_{k}': tmp[k] for k in tmp.keys()}

        tmp = self.get_pot_atv()
        res = res | {f'co.ativa_{k}': tmp[k] for k in tmp.keys()}

        tmp = self.get_pot_reat()
        res = res | {f'co.reativa_{k}': tmp[k] for k in tmp.keys()}

        tmp = self.get_pot_apar()
        res = res | {f'co.aparente_{k}': tmp[k] for k in tmp.keys()}

        tmp = self.get_correntes()
        res = res | {f'co.corrente_{k}': tmp[k] for k in tmp.keys()}

        return res
    
    ''' 
    Pra testar com dados falsos
    
    xv = [0,0,0,1,0,0]

    def fetch_data(self):
        res = {}
        res['co.vel'] = 11.5 #self.get_vel()
        res['co.freq'] = 24.5 #self.get_freq()
        res['co.sel_driver'] = 3 #self.get_seldriver()
        res['co.inv_start'] = 1 #self.get_invstart()
        res['co.dir_start'] = 1 #self.get_dirstart()
        res['co.soft_start'] = 1 #self.get_softstart()
        res['co.torque'] = 12.3 #self.get_torque()

        tmp = {'pit01': random.randint(0,600), 'fv01': 31.5, 'fit02': 32.4, 'fit03': 14.3} #self.get_pressoes()
        res = res | {f'co.{k}': tmp[k] for k in tmp.keys()}

        tmp = self.xv #self.get_xv()
        res = res | {f'co.xv{i}': tmp[i-1] for i in range(1,7,1)}

        tmp = { 'r': 74, 's': 84, 't': 94, 'carc': 500 } #self.get_temps()
        res = res | {f'co.temp_{k}': tmp[k] for k in tmp.keys()}

        tmp = { 'rs': 274, 'st': 284, 'tr': 294 } #self.get_tensoes()
        res = res | {f'co.tensao_{k}': tmp[k] for k in tmp.keys()}

        tmp = { 'r': 5, 's': 9, 't': 4, 'tot': 18 } #self.get_pot_atv()
        res = res | {f'co.ativa_{k}': tmp[k] for k in tmp.keys()}

        tmp = { 'r': 3, 's': 7, 't': 2, 'tot': 12 } #self.get_pot_reat()
        res = res | {f'co.reativa_{k}': tmp[k] for k in tmp.keys()}

        tmp = { 'r': 4, 's': 1, 't': 5, 'tot': 10 } #self.get_pot_apar()
        res = res | {f'co.aparente_{k}': tmp[k] for k in tmp.keys()}

        tmp = { 'r': 43, 's': 12, 't': 75, 'n': 31, 'med': 20 } #self.get_correntes()
        res = res | {f'co.corrente_{k}': tmp[k] for k in tmp.keys()}

        return res

    def open(self):
        return True
    
    @property
    def is_open(self):
        return True
    '''
    