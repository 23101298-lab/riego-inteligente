# Riego Inteligente con Raspberry Pi Pico W

Sistema IoT de monitoreo y riego automático usando sensores, Raspberry Pi Pico W, LCD I2C y envío de datos a la nube (Ubidots / ThingSpeak / Blynk).  
Repo estructurado, con credenciales fuera del código (`config.py` ignorado por Git).

---

##  Características
- Sensores:
  - Humedad de suelo (capacitivo/FC-28, ADC GP28)
  - Temp/HR del aire (DHT11/DHT22, GP15)
  - Temp del suelo (DS18B20, 1-Wire GP14)
  - Luz (LDR, ADC GP27)
- LCD 16x2 I2C (0x27) en SDA GP2 / SCL GP3
- Botón KY-004 en GP16 para cambiar planta en pantalla
- Envío de lecturas cada 5 s por Wi-Fi integrado
- Código sin credenciales públicas (usa `config.py` local)

---

## 🔧Requisitos
- Raspberry Pi Pico W con **MicroPython**
- Thonny (o similar) para subir archivos
- Cuenta en Ubidots/ThingSpeak/Blynk (si usarás nube)

---

##  Pines sugeridos (Pico W)

- **LDR** → `GP27 / ADC1`
- **Humedad de suelo (capacitivo/FC-28)** → `GP28 / ADC2`
- **DHT11 / DHT22 (Temp/HR aire)** → `GP15`
- **DS18B20 (Temp suelo, 1-Wire)** → `GP14`
- **LCD I2C 16x2 (0x27)** → `SDA GP2` / `SCL GP3`
- **Botón KY-004** → `GP16`
- **Relay bomba/válvula** → `GPIO` (el que definas en tu código)

> Ajusta los pines en `src/main.py` si usas otros.

---

##  Cómo funciona (resumen)

1. Lee sensores:  
   - humedad del suelo  
   - temperatura/humedad del aire  
   - temperatura del suelo  
   - nivel de luz  

2. Muestra en el **LCD** la planta seleccionada (cambia con el botón).

3. Cada **5 segundos** empaqueta lecturas y **envía datos a la nube** vía HTTP.

4. (Opcional) Activa el **relay** si aplicas lógica de riego por umbral.



