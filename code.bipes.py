import network
import time
from machine import I2C, Pin
import umqtt.robust

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)

def sht20_temperature():
    i2c.writeto(0x40, b'\xf3')
    time.sleep_ms(70)
    t = i2c.readfrom(0x40, 2)
    return -46.86 + 175.72 * (t[0] * 256 + t[1]) / 65535

def sht20_humidity():
    i2c.writeto(0x40, b'\xf5')
    time.sleep_ms(70)
    t = i2c.readfrom(0x40, 2)
    return -6 + 125 * (t[0] * 256 + t[1]) / 65535

def save_to_csv(data, filename="/temperatures.csv"):
    with open(filename, 'w') as f:
        for temp in data:
            f.write(f"{temp}\n")

print(sta_if.scan())
sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.scan()
sta_if.connect('motog52_3718', '12345678')
print("Waiting for Wifi connection")
while not sta_if.isconnected():
    time.sleep(1)
print("Connected")

i2c = I2C(scl=Pin(22), sda=Pin(21))
easymqtt_session = "vefeoh"
easymqtt_client = umqtt.robust.MQTTClient("umqtt_client", server="bipes.net.br", port=1883, user="bipes", password="m8YLUr5uW3T")
easymqtt_client.connect()
print("EasyMQTT connected")

temperatures = []  # Lista para armazenar as temperaturas
max_readings = 10  # Nmero mximo de leituras antes de salvar em CSV

while True:
    temperature = sht20_temperature()
    easymqtt_client.publish(easymqtt_session + "/" + 'temperatura', str(temperature))
    print("EasyMQTT Publish - Session:", easymqtt_session, "Topic:", 'temperatura', "Value:", str(temperature))

    temperatures.append(temperature)  # Armazena a temperatura na lista

    if len(temperatures) >= max_readings:
        save_to_csv(temperatures)
        print(f"Saved {len(temperatures)} readings to CSV.")
        temperatures = []  # Limpa a lista para novas leituras

    time.sleep(3)