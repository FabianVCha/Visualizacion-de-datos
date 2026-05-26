import requests
import time
import random

BASE_URL = "http://localhost:5000"

ENDPOINTS = [
    "/api/products",
    "/api/orders",
    "/api/users",
    "/health",
]

def generate_traffic():
    print("🚀 Generando tráfico... Ctrl+C para detener\n")
    request_count = 0
    
    while True:
        endpoint = random.choice(ENDPOINTS)
        
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            request_count += 1
            
            status_icon = "✅" if response.status_code == 200 else "❌"
            print(f"{status_icon} [{request_count:04d}] GET {endpoint} → {response.status_code}")
            
        except requests.exceptions.ConnectionError:
            print("⚠️  No se puede conectar a la API. ¿Está corriendo en :5000?")
            time.sleep(3)
        
        # Pausa aleatoria entre requests (simula usuarios reales)
        time.sleep(random.uniform(0.1, 0.8))

if __name__ == "__main__":
    generate_traffic()
