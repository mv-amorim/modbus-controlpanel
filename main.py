from clientemodbus import ClienteMODBUS

c = ClienteMODBUS('192.168.0.14', 502)

c.set_seldriver(1)
c.set_softstart(0)
print()