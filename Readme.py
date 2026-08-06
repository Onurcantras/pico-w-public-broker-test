# 🌐 Pico W - Public MQTT Broker Integration & Security Policy

Integration module for connecting the **Raspberry Pi Pico W** to public MQTT brokers (e.g., `test.mosquitto.org`) with privacy controls and LWT (Last Will and Testament) verification.

## 🚀 Features

- **Public Broker Connectivity:** Tests remote publish/subscribe capabilities via public MQTT test endpoints (`test.mosquitto.org`).
- **Data Privacy Protocols:** Enforces strict payload sanitization (zero personal identifiable data, passwords, or credentials in public payloads).
- **LWT & Availability Lifecycle:** Demonstrates retained `online` and `offline` availability state updates.
- **Collision Avoidance:** Enforces unique namespace topic prefixing (`internship/{studentId}/{deviceId}/...`).

## 📋 Security & Compliance Note

> **Warning:** Public brokers are unencrypted and open to the public internet. Never publish private Wi-Fi credentials, personal names, or authentication keys to public MQTT topic trees.

## 🛠️ Verification Command (CLI)

Listen to the remote public broker telemetry from any host machine:

```bash
mosquitto_sub -h test.mosquitto.org -p 1883 -t "internship/onurcan-tras-unique-id/pico-w-irrigation-01/#" -v