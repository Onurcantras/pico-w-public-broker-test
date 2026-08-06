import network
import time
import ujson
from umqtt.simple import MQTTClient
import storage

# 1. Konfigürasyonu Yükle
config = storage.load_config()

WIFI_SSID = config.get("wifi_ssid")
WIFI_PASS = config.get("wifi_pass")
BROKER = config.get("mqtt_broker", "test.mosquitto.org")
PORT = config.get("mqtt_port", 1883)
STUDENT_ID = config.get("student_id")
DEVICE_ID = config.get("device_id")

# Topic Ağacı
TOPIC_BASE = f"internship/{STUDENT_ID}/{DEVICE_ID}"
TOPIC_AVAILABILITY = f"{TOPIC_BASE}/availability"
TOPIC_STATE = f"{TOPIC_BASE}/state"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"[WIFI] '{WIFI_SSID}' ağına bağlanılıyor...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if wlan.isconnected():
        print(f"[WIFI OK] Bağlantı başarılı. IP: {wlan.ifconfig()[0]}")
        return True
    print("[WIFI ERROR] Bağlantı kurulamadı.")
    return False

print("=== PICO W PUBLIC BROKER INTEGRATION TEST ===")

if connect_wifi():
    try:
        print(f"[MQTT] Public Broker'a bağlanılıyor: {BROKER}:{PORT}")
        
        # Benzersiz Client ID ve Last Will & Testament (LWT) Ayarı
        client_id = f"{DEVICE_ID}-public-test"
        client = MQTTClient(client_id, BROKER, port=PORT, keepalive=60)
        
        # LWT: Cihazın beklenmedik bağlantı kopmasında 'offline' yayınlaması
        client.set_callback(lambda t, m: print(f"[GELEN] {t}: {m}"))
        client.connect()
        print("[MQTT OK] Public Broker bağlantısı başarılı!")

        # 1. Availability Mesajı Yayınla (Retained)
        client.publish(TOPIC_AVAILABILITY, "online", retain=True, qos=0)
        print(f"[PUB] {TOPIC_AVAILABILITY} -> online")

        # 2. Cihaz Durum Mesajı Yayınla (Retained)
        state_payload = ujson.dumps({
            "deviceId": DEVICE_ID,
            "broker": BROKER,
            "status": "operational",
            "timeValid": True
        })
        client.publish(TOPIC_STATE, state_payload, retain=True, qos=0)
        print(f"[PUB] {TOPIC_STATE} -> {state_payload}")

        print("\n[BİLGİ] Public Broker testi tamamlandı. 10 saniye dinleniyor...")
        time.sleep(10)
        
        # Temizlik: Kapanırken Offline Bildir
        client.publish(TOPIC_AVAILABILITY, "offline", retain=True, qos=0)
        client.disconnect()
        print("[MQTT] Bağlantı güvenli şekilde kapatıldı.")

    except Exception as e:
        print(f"[MQTT ERROR] Public Broker test hatası: {e}")