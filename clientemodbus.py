from pyModbusTCP.client import ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

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

    #def get_fv01(self):

    # def get_vel(self):
      
    def get_torque(self):
        registers = self._client.read_holding_registers(1420, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(registers)
        res = decoder.decode_32bit_float()
        return res

    def get_correntes(self):
        registers = self._client.read_holding_registers(840, 7)
        decoder = BinaryPayloadDecoder.fromRegisters(registers)
        r = decoder.decode_16bit_float() * 10
        s = decoder.decode_16bit_float() * 10
        t = decoder.decode_16bit_float() * 10
        n = decoder.decode_32bit_float() * 10
        med = decoder.decode_32bit_float() * 10
        res = { r, s, t, n, med }
        return res
    
    def get_pot_atv(self):
        registers = self._client.read_holding_registers(852, 4)
        decoder = BinaryPayloadDecoder.fromRegisters(registers)
        r = decoder.decode_16bit_float()
        s = decoder.decode_16bit_float()
        t = decoder.decode_16bit_float()
        tot = decoder.decode_16bit_float()
        return { r, s, t, tot }
    
    def get_pot_reat(self):
        registers = self._client.read_holding_registers(856, 4)
        decoder = BinaryPayloadDecoder.fromRegisters(registers)
        r = decoder.decode_16bit_float()
        s = decoder.decode_16bit_float()
        t = decoder.decode_16bit_float()
        tot = decoder.decode_16bit_float()
        return { r, s, t, tot }
    
    def get_pot_apar(self):
        registers = self._client.read_holding_registers(860, 4)
        decoder = BinaryPayloadDecoder.fromRegisters(registers)
        r = decoder.decode_16bit_float()
        s = decoder.decode_16bit_float()
        t = decoder.decode_16bit_float()
        tot = decoder.decode_16bit_float()
        return { r, s, t, tot }
    
    def get_freq(self):
        registers = self._client.read_holding_registers(884, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(registers)
        res = decoder.decode_32bit_float()
        return res
       
    def get_tensoes(self):
        registers = self._client.read_holding_registers(847, 3)
        decoder = BinaryPayloadDecoder.fromRegisters(registers)
        rs = decoder.decode_16bit_float() * 10
        st = decoder.decode_16bit_float() * 10
        tr = decoder.decode_16bit_float() * 10
        return { rs, st, tr }
    
    def get_temps(self):
        registers = self._client.read_holding_registers(700, 8)
        decoder = BinaryPayloadDecoder.fromRegisters(registers)
        r = decoder.decode_32bit_float() * 10
        s = decoder.decode_32bit_float() * 10
        t = decoder.decode_32bit_float() * 10
        carc = decoder.decode_32bit_float() * 10
        return { r, s, t, carc }

    def get_pressoes(self):
        registers = self._client.read_holding_registers(714, 6)
        decoder = BinaryPayloadDecoder.fromRegisters(registers)
        pit01 = decoder.decode_32bit_float()
        fit02 = decoder.decode_32bit_float()
        fit03 = decoder.decode_32bit_float()
        return { pit01, fit02, fit03 }

    def get_xv(self):
        registers = self._client.read_holding_registers(712, 1)
        decoder = BinaryPayloadDecoder.fromRegisters(registers)
        bits = decoder.decode_bits()
        return bits[:5]

    def set_xv(self, xv):
        builder = BinaryPayloadBuilder()
        builder.add_bits(xv)
        regs = builder.to_registers()
        self._client.write_multiple_registers(712, regs)
        return xv

    def get_softstart(self):
        res = self._client.read_holding_registers(1316, 1)[0]
        return res

    def set_softstart(self, soft_s):
        if soft_s in [0, 1, 2]:
            self._client.write_single_register(1316, soft_s)
            return soft_s
        else:
            return
    
    def get_dirstart(self):
        res = self._client.read_holding_registers(1319, 1)[0]
        return res
    
    def set_dirstart(self, dir_s):
        if dir_s in [0, 1, 2]:
            self._client.write_single_register(1319, dir_s)
            return dir_s
        else:
            return
        
    def get_invstart(self):
        res = self._client.read_holding_registers(1312, 1)[0]
        return res
       
    def set_invstart(self, inv_s):
        if inv_s in [0, 1, 2]:
            self._client.write_single_register(1312, inv_s)
            return inv_s
        else:
            return
       
    def get_seldriver(self):
        res = self._client.read_holding_registers(1324, 1)[0]
        return res
       
    def set_seldriver(self, start):
        if start in [1, 2, 3]:
            self._client.write_single_register(1324, start)
            return start
        else:
            return