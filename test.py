from time import sleep
from modbusclient import CustomModbusClient

client = CustomModbusClient(server_ip='192.168.0.14', port=502)

sleep(1)
client.set_freq(60)

sleep(1)
client.set_seldriver(2)

sleep(1)
client.set_invstart(1)
print('ligou')

sleep(3)
print(client.fetch_data())

sleep(15)
client.set_freq(30)

sleep(15)
client.set_invstart(0)
print('desligou')

sleep(1)
client.set_xv([0,1,0,0,0,0])
sleep(1)
client.set_xv([0,1,0,0,0,0])
sleep(1)
client.set_xv([0,0,1,0,0,0])
sleep(1)
client.set_xv([0,0,0,1,0,0])
sleep(1)
client.set_xv([0,0,0,0,1,0])
sleep(1)
client.set_xv([0,0,0,0,0,1])
sleep(1)
client.set_xv([0,0,0,0,0,0])