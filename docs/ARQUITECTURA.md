flowchart LR
  HUM[Humedad suelo]
  LDR[LDR]
  DHT[DHT11/DHT22]
  DS[DS18B20]
  CPU[Raspberry Pi Pico W - CPU]
  ADC[ADC]
  GPIO[GPIO]
  WIFI[WiFi]
  RELAY[Relay]
  PUMP[Valvula/Bomba]
  API[API Nube]
  DASH[Dashboard]

  HUM --> ADC
  LDR --> ADC
  DHT --> GPIO
  DS  --> GPIO
  ADC --> CPU
  GPIO --> CPU
  CPU --> RELAY --> PUMP
  CPU --> WIFI --> API --> DASH
