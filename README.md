# Riego inteligente – Pico W

Prototipo de riego automático con Raspberry Pi Pico W: lee sensores (humedad de suelo, DHT11, DS18B20, LDR), muestra planta en LCD I2C y envía datos a Ubidots.

## Hardware
- Raspberry Pi Pico W
- Sensor capacitivo de humedad (ADC GP28)
- DHT11 (GP15)
- DS18B20 (GP14, 1-Wire)
- LDR (ADC GP27)
- LCD 16x2 I2C (0x27, SDA GP2, SCL GP3)
- Botón KY-004 (GP16)
- Relay + bomba/solenoide

## Cómo usar
1. Copia `src/` a la Pico W (Thonny o ampy).
2. Renombra `src/config_example.py` a `config.py` y coloca tus credenciales.
3. Ejecuta `main.py`. El LCD muestra la planta; cada 5 s se envían lecturas a Ubidots.

## Licencia
MIT
