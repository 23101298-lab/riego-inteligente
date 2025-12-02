flowchart LR
  subgraph CAMPO["Parcela / Campo"]
    HUM[Humedad suelo]
    LDR[LDR]
    DHT[DHT11/DHT22]
    DS[DS18B20]
  end

  subgraph PICO["Raspberry Pi Pico W"]
    CPU[CPU]
    ADC[ADC]
    GPIO[GPIO]
    WIFI[WiFi]
    RAM[RAM]
    FLASH[Flash]
  end

  subgraph RIEGO["Riego"]
    RELAY[Relay]
    PUMP[Valvula/Bomba]
  end

  subgraph NUBE["Nube"]
    API[API]
    DASH[Dashboard]
  end

  HUM --> ADC
  LDR --> ADC
  DHT --> GPIO
  DS  --> GPIO
  ADC --> CPU
  GPIO --> CPU
  CPU --> RELAY --> PUMP
  CPU --> WIFI --> API --> DASH

