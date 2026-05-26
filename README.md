
# API Monitoring con Prometheus y Grafana

Proyecto de monitoreo de una API REST usando Prometheus para recolección de métricas y Grafana para visualización.

## Estructura del proyecto

```
tu-proyecto/
├── docker-compose.yml
├── README.md
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── prometheus/
│   └── prometheus.yml
└── scripts/
    └── generate-traffic.py
```

## Tecnologías usadas

- **Flask** — API REST en Python
- **prometheus-client** — Instrumentación de métricas
- **Prometheus** — Recolección y almacenamiento de métricas
- **Grafana** — Visualización y dashboards
- **Docker Compose** — Orquestación de servicios

## Requisitos previos

- Docker Desktop instalado y corriendo
- Python 3.11+
- WSL 2 (si usas Windows)

## Instalación y uso

### 1. Clonar e instalar dependencias locales
```bash
pip install flask prometheus-client requests
```

### 2. Levantar los servicios con Docker
```bash
docker compose up --build
```

### 3. Generar tráfico de prueba
```bash
python scripts/generate-traffic.py
```

## Servicios disponibles

| Servicio | URL | Descripción |
|---|---|---|
| API | http://localhost:5000 | API REST con métricas |
| Métricas | http://localhost:5000/metrics | Endpoint para Prometheus |
| Prometheus | http://localhost:9090 | UI de consultas PromQL |
| Grafana | http://localhost:3001 | Dashboards (admin/admin) |

## Endpoints de la API

| Endpoint | Método | Descripción |
|---|---|---|
| `/api/products` | GET | Lista de productos (latencia 10-300ms) |
| `/api/orders` | GET | Lista de órdenes (20% de errores 500) |
| `/api/users` | GET | Usuarios activos simulados |
| `/health` | GET | Estado de salud de la API |
| `/metrics` | GET | Métricas en formato Prometheus |

## Métricas instrumentadas

| Métrica | Tipo | Descripción |
|---|---|---|
| `http_requests_total` | Counter | Total de requests por endpoint y status |
| `http_request_duration_seconds` | Histogram | Latencia de cada request |
| `active_users` | Gauge | Usuarios activos en tiempo real |

## Queries PromQL útiles

```promql
# Requests por segundo
rate(http_requests_total[1m])

# Requests por status code
sum by (status) (rate(http_requests_total[1m]))

# Latencia promedio
rate(http_request_duration_seconds_sum[1m]) / rate(http_request_duration_seconds_count[1m])

# Usuarios activos
active_users
```

## Configurar Grafana

1. Entrar a http://localhost:3001 con `admin` / `admin`
2. Ir a **Connections → Data sources → Add data source**
3. Seleccionar **Prometheus**
4. URL: `http://prometheus:9090`
5. Click **Save & test**
6. Crear dashboard con las queries PromQL de arriba

## Solución de problemas

**Docker no encontrado en WSL:**
Activar WSL Integration en Docker Desktop → Settings → Resources → WSL Integration

**Diferencia de tiempo en Prometheus:**
```bash
sudo ntpdate -u time.windows.com
docker compose restart
```

**Prometheus no hace scraping (Target DOWN):**
Verificar que la URL en `prometheus.yml` sea `api:5000` y no `localhost:5000`
