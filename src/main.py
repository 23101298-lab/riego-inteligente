# main.py — bucle principal del riego inteligente
"""
Lee sensores (humedad suelo, DHT11, DS18B20, LDR), muestra planta en LCD
y envía datos a la nube. Si no hay Wi-Fi, sigue mostrando en LCD.
"""

import network, urequests, time, json
from machine import ADC, Pin, I2C
import dht, onewire, ds18x20
from pico_i2c_lcd import I2cLcd

# ---- Configuración (NO PONGAS CLAVES AQUÍ) ----
from config import WIFI_SSID, WIFI_PASSWORD, UBIDOTS_TOKEN, DEVICE_LABEL
I2C_ADDR = 0x27

# ----- LCD / UI -----
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
plantas = ["Muña","Matico","Manzanilla","Hercampuri","Toronjil","Ruda",
           "Hierba Luisa","Eucalipto","Sabila","Tilo"]
indice_planta, boton, estado_anterior = 0, Pin(16, Pin.IN, Pin.PULL_UP), 1

# ----- Sensores -----
ldr = ADC(Pin(27))
hum_suelo = ADC(Pin(28))
dht_sensor = dht.DHT11(Pin(15))
ow, ds_sensor = onewire.OneWire(Pin(14)), None
try:
    ds_sensor = ds18x20.DS18X20(ow); ROMS = ds_sensor.scan()
except: ROMS = []

def conectar_wifi() -> bool:
    """Conecta a Wi-Fi con reintentos y devuelve True/False."""
    wlan = network.WLAN(network.STA_IF); wlan.active(True); wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    print("\nConectando a Wi-Fi...", end=""); t=0
    while not wlan.isconnected() and t < 20: print(".", end=""); time.sleep(0.5); t+=1
    ok = wlan.isconnected()
    print("\nWi-Fi OK. IP:", wlan.ifconfig()[0]) if ok else print("\nERROR Wi-Fi")
    return ok

def enviar_ubidots(temp_aire, hum_aire, temp_suelo, hum_suelo_pct, lux):
    """Postea un JSON a Ubidots. Maneja errores y cierra la conexión."""
    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"
    headers = {"Content-Type":"application/json","X-Auth-Token":UBIDOTS_TOKEN}
    payload = {"temp_aire":temp_aire,"hum_aire":hum_aire,"temp_suelo":temp_suelo,
               "hum_suelo":hum_suelo_pct,"luz":lux}
    try:
        r = urequests.post(url, headers=headers, data=json.dumps(payload))
        print("Ubidots:", r.status_code); r.close()
    except Exception as e:
        print("Error Ubidots:", e)

def leer_sensores():
    """Devuelve tupla (lux%, hum_suelo%, temp_aire, hum_aire, temp_suelo)."""
    try:
        lux = max(0, min(100, (ldr.read_u16()/65535)*100))
    except: lux = None
    try:
        humedad_suelo_pct = 100 - int((hum_suelo.read_u16()/65535)*100)
    except: humedad_suelo_pct = None
    try:
        dht_sensor.measure(); temp_aire=dht_sensor.temperature(); hum_aire=dht_sensor.humidity()
    except: temp_aire=hum_aire=None
    try:
        if ds_sensor and ROMS: ds_sensor.convert_temp(); time.sleep_ms(750); temp_suelo = ds_sensor.read_temp(ROMS[0])
        else: temp_suelo=None
    except: temp_suelo=None
    return lux, humedad_suelo_pct, temp_aire, hum_aire, temp_suelo

def loop():
    """UI + envío cada 5 s."""
    global indice_planta, estado_anterior
    lcd.clear(); lcd.putstr(plantas[indice_planta])
    ultimo = time.time()
    while True:
        estado = boton.value()
        if estado == 0 and estado_anterior == 1:
            indice_planta = (indice_planta + 1) % len(plantas)
            lcd.clear(); lcd.putstr(plantas[indice_planta]); time.sleep(0.15)
        estado_anterior = estado

        if time.time() - ultimo >= 5:
            ultimo = time.time()
            lux, hum_s, t_air, h_air, t_soil = leer_sensores()
            print("\n--- LECTURAS ---")
            print(f"Temp aire: {t_air} °C | HR aire: {h_air} %")
            print(f"Temp suelo: {t_soil} °C | Hum suelo: {hum_s} % | Luz: {lux} %")
            enviar_ubidots(t_air, h_air, t_soil, hum_s, lux)

if __name__ == "__main__":
    if conectar_wifi(): loop()
    else: print("Sin Wi-Fi")
