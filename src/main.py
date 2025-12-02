# main.py — bucle principal del riego inteligente
"""
Lee sensores (humedad suelo, DHT11, DS18B20, LDR), muestra planta en LCD
y envía datos a la nube. Si no hay Wi-Fi, sigue mostrando en LCD.
"""

import network
import urequests
import time
import json
from machine import ADC, Pin, I2C
import dht
import onewire, ds18x20
from pico_i2c_lcd import I2cLcd

# --------------------------
# CONFIGURACIÓN DEL USUARIO
# --------------------------
WIFI_SSID = "iPhone"
WIFI_PASSWORD = "310108**"
UBIDOTS_TOKEN = "BBUS-Srviab4b2udKgJTWd1HMcN4p0FBmVy"
DEVICE_LABEL = "Raspi"

# ----- Configuración de LCD -----
I2C_ADDR = 0x27
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# ----- Lista de plantas -----
plantas = [
    "Muña", "Matico", "Manzanilla", "Hercampuri",
    "Toronjil", "Ruda", "Hierba Luisa", "Hierba Luisa",
    "Eucalipto", "Sabila", "Tilo"
]
indice_planta = 0

# ----- BOTÓN KY-004 -----
boton = Pin(16, Pin.IN, Pin.PULL_UP)  # GP16
estado_anterior = 1

# --------------------------
# CONFIG SENSORES
# --------------------------
ldr = ADC(Pin(27))             # LDR
hum_suelo = ADC(Pin(28))       # FC-28 Humedad suelo
dht_sensor = dht.DHT11(Pin(15)) # DHT11 Aire
ds_pin = Pin(14)               # DS18B20 Suelo
ow = onewire.OneWire(ds_pin)
ds_sensor = ds18x20.DS18X20(ow)
roms = ds_sensor.scan()

# --------------------------
# FUNCIONES
# --------------------------
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    print("\nConectando a WiFi...", end="")
    intentos = 0
    while not wlan.isconnected() and intentos < 20:
        print(".", end="")
        time.sleep(0.5)
        intentos += 1

    if wlan.isconnected():
        print("\nWiFi conectado con éxito. IP:", wlan.ifconfig()[0])
        return True
    else:
        print("\nERROR: No se pudo conectar al WiFi")
        return False

def enviar_ubidots(temp_aire, hum_aire, temp_suelo, hum_suelo, lux):
    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"
    headers = {"Content-Type": "application/json", "X-Auth-Token": UBIDOTS_TOKEN}
    payload = {
        "temp_aire": temp_aire,
        "hum_aire": hum_aire,
        "temp_suelo": temp_suelo,
        "hum_suelo": hum_suelo,
        "luz": lux
    }

    try:
        response = urequests.post(url, headers=headers, data=json.dumps(payload))
        print("Ubidots:", response.status_code)
        response.close()
    except Exception as e:
        print("Error enviando a Ubidots:", e)

# --------------------------
# BUCLE PRINCIPAL
# --------------------------
if conectar_wifi():

    lcd.clear()
    lcd.putstr(plantas[indice_planta])

    ultimo_envio = time.time()

    while True:

        # ---- CAMBIO DE PLANTA INSTANTÁNEO ----
        estado = boton.value()
        if estado == 0 and estado_anterior == 1:  # pulsación real
            indice_planta = (indice_planta + 1) % len(plantas)
            lcd.clear()
            lcd.putstr(plantas[indice_planta])
            time.sleep(0.15)  # anti rebote
        estado_anterior = estado

        # ---- ENVÍO DE SENSORES CADA 5 SEG ----
        if time.time() - ultimo_envio >= 5:
            ultimo_envio = time.time()

            # LDR
            try:
                adc_lux = ldr.read_u16()
                lux = max(0, min(100, (adc_lux / 65535) * 100))
            except:
                lux = None

            # Humedad suelo
            try:
                adc_suelo = hum_suelo.read_u16()
                humedad_suelo_pct = 100 - int((adc_suelo / 65535) * 100)
            except:
                humedad_suelo_pct = None

            # DHT11 Aire
            try:
                dht_sensor.measure()
                temp_aire = dht_sensor.temperature()
                hum_aire = dht_sensor.humidity()
            except:
                temp_aire = hum_aire = None

            # DS18B20 Suelo
            try:
                ds_sensor.convert_temp()
                time.sleep_ms(750)
                temp_suelo = ds_sensor.read_temp(roms[0]) if roms else None
            except:
                temp_suelo = None

            # Consola
            print("\n--- LECTURAS REALES ---")
            print(f"Temp aire: {temp_aire} °C")
            print(f"Hum aire: {hum_aire} %")
            print(f"Temp suelo: {temp_suelo} °C")
            print(f"Hum suelo: {humedad_suelo_pct} %")
            print(f"Luz: {lux} %")

            enviar_ubidots(temp_aire, hum_aire, temp_suelo, humedad_suelo_pct, lux)

else:
    print("Sin WiFi")
