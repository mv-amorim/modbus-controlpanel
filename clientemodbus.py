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
        data = self._client.read_holding_registers(1420, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        res = decoder.decode_32bit_float()
        return res

    def get_correntes(self):
        data = self._client.read_holding_registers(840, 7)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        r = decoder.decode_16bit_float() * 10
        s = decoder.decode_16bit_float() * 10
        t = decoder.decode_16bit_float() * 10
        n = decoder.decode_32bit_float() * 10
        med = decoder.decode_32bit_float() * 10
        res = { r, s, t, n, med }
        return res
    
    def get_pot_atv(self):
        data = self._client.read_holding_registers(852, 4)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        r = decoder.decode_16bit_float()
        s = decoder.decode_16bit_float()
        t = decoder.decode_16bit_float()
        tot = decoder.decode_16bit_float()
        return { r, s, t, tot }
    
    def get_pot_reat(self):
        data = self._client.read_holding_registers(856, 4)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        r = decoder.decode_16bit_float()
        s = decoder.decode_16bit_float()
        t = decoder.decode_16bit_float()
        tot = decoder.decode_16bit_float()
        return { r, s, t, tot }
    
    def get_pot_apar(self):
        data = self._client.read_holding_registers(860, 4)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        r = decoder.decode_16bit_float()
        s = decoder.decode_16bit_float()
        t = decoder.decode_16bit_float()
        tot = decoder.decode_16bit_float()
        return { r, s, t, tot }
    
    def get_freq(self):
        data = self._client.read_holding_registers(884, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        res = decoder.decode_32bit_float()
        return res
       
    def get_tensoes(self):
        data = self._client.read_holding_registers(847, 3)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        rs = decoder.decode_16bit_float() * 10
        st = decoder.decode_16bit_float() * 10
        tr = decoder.decode_16bit_float() * 10
        return { rs, st, tr }
    
    def get_temps(self):
        data = self._client.read_holding_registers(700, 8)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        r = decoder.decode_32bit_float() * 10
        s = decoder.decode_32bit_float() * 10
        t = decoder.decode_32bit_float() * 10
        carc = decoder.decode_32bit_float() * 10
        return { r, s, t, carc }

    def get_pressoes(self):
        data = self._client.read_holding_registers(714, 6)
        decoder = BinaryPayloadDecoder.fromRegisters(data.registers)
        pit01 = decoder.decode_32bit_float()
        fit02 = decoder.decode_32bit_float()
        fit03 = decoder.decode_32bit_float()
        return { pit01, fit02, fit03 }

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