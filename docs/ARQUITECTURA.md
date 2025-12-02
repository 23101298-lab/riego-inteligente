# Arquitectura del sistema

```mermaid
flowchart LR

  subgraph CAMPO["Parcela / Campo"]
    HUM[Humedad de suelo]
    LDR[LDR]
    DHT[DHT11 / DHT22]
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
    PUMP[Valvula / Bomba]
  end

  subgraph NUBE["Nube"]
    API[A]()


