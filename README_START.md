# Monitoring & Observability — Інструкція запуску

## Архітектура системи

```
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Compose                           │
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌────────────┐                  │
│  │  web1     │   │  web2     │   │ mosquitto  │                  │
│  │ Flask     │   │ Flask     │   │ MQTT broker│                  │
│  │ :5001     │   │ :5002     │   │ :1883/:9001│                  │
│  │ /metrics  │   │ /metrics  │   └────────────┘                  │
│  └─────┬─────┘   └─────┬─────┘                                  │
│        │               │                                         │
│        └───────┬───────┘                                         │
│                ▼                                                 │
│  ┌──────────────────┐    ┌─────────────┐    ┌────────────────┐  │
│  │   Prometheus      │───▶│ Alertmanager │───▶│   Telegram     │  │
│  │   :9090           │    │ :9093        │    │   Bot API      │  │
│  └────────┬──────────┘    └─────────────┘    └────────────────┘  │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                            │
│  │    Grafana        │    ┌──────────────┐  ┌──────────────┐    │
│  │    :3000          │    │  cAdvisor     │  │ node-exporter│    │
│  │  (dashboards)     │    │  :8080        │  │ :9100        │    │
│  └──────────────────┘    └──────────────┘  └──────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Компоненти

| Сервіс | Порт | Призначення |
|---|---|---|
| **mosquitto** | 1883, 9001 | MQTT брокер (TCP + WebSocket) |
| **web-service-1** | 5001 | Flask веб-сервіс з MQTT health-check |
| **web-service-2** | 5002 | Flask API сервіс |
| **Prometheus** | 9090 | Збір та зберігання метрик |
| **Grafana** | 3000 | Візуалізація метрик (дашборди) |
| **Alertmanager** | 9093 | Маршрутизація алертів (Telegram) |
| **cAdvisor** | 8080 | Метрики контейнерів (CPU, RAM, Network) |
| **node-exporter** | 9100 | Метрики хостової системи |

---

## Передумови

- **Docker Desktop** встановлений та запущений
- **Git** (опціонально)

---

## Крок 1: Створення Telegram-бота для алертів

### 1.1 Створити бота

1. Відкрийте Telegram і знайдіть **@BotFather**
2. Надішліть команду `/newbot`
3. Введіть ім'я бота (наприклад: `MQTT Monitor Bot`)
4. Введіть username бота (наприклад: `mqtt_monitor_horovyak_bot`) — повинен закінчуватись на `bot`
5. BotFather поверне **Bot Token** — скопіюйте його. Виглядає як:
   ```
   8615976197:AAE5F-50OhqrDSd-me43aTVA-T0ni8BKOTM
   ```

### 1.2 Отримати Chat ID

1. Напишіть будь-яке повідомлення вашому новому боту в Telegram
2. Відкрийте в браузері:
   ```
   https://api.telegram.org/bot8615976197:AAE5F-50OhqrDSd-me43aTVA-T0ni8BKOTM/getUpdates
   ```
   (замініть `<YOUR_BOT_TOKEN>` на ваш токен)
3. У відповіді знайдіть поле `"chat":{"id": 976981028}` — це ваш **Chat ID**

### 1.3 Вписати дані в конфігурацію

Відкрийте файл `stt-pz-3/monitoring/alertmanager/alertmanager.yml` та замініть:

- `YOUR_BOT_TOKEN` — на токен з кроку 1.1
- `0` (chat_id) — на ваш Chat ID з кроку 1.2

Приклад:
```yaml
receivers:
  - name: "telegram"
    telegram_configs:
      - bot_token: "7123456789:AAHfiqksKZ8WmR2zMfLSt3m-example"
        chat_id: 123456789
```

---

## Крок 2: Запуск

Перейдіть у папку проєкту та запустіть все однією командою:

```bash
cd stt-pz-3
docker compose up --build -d
```

Зачекайте 1-2 хвилини, поки всі сервіси стартують.

### Перевірка що все працює

```bash
docker compose ps
```

Всі контейнери повинні мати статус `Up`.

---

## Крок 3: Доступ до сервісів

| Сервіс | URL |
|---|---|
| Web1 (MQTT Console) | http://localhost:5001 |
| Web2 (API) | http://localhost:5002 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| Alertmanager | http://localhost:9093 |
| cAdvisor | http://localhost:8080 |

### Grafana

- **Логін:** `admin`
- **Пароль:** `admin`
- Дашборд **"MQTT Infrastructure Monitor"** вже підключений автоматично
- Знайдіть його: Dashboards → Browse → MQTT Infrastructure Monitor

---

## Крок 4: Перевірка роботи моніторингу

### 4.1 Перевірка метрик

1. Відкрийте http://localhost:9090/targets — всі targets повинні бути `UP`
2. Відкрийте http://localhost:3000 — дашборд показує графіки CPU, RAM, статус контейнерів

### 4.2 Перевірка алертів (зупинка контейнера)

Зупиніть один з контейнерів:

```bash
docker stop web-service-1
```

Через ~30-60 секунд:
1. Prometheus зафіксує, що target `web1` — `DOWN`
2. Alert `ServiceDown` перейде в стан `FIRING`
3. Alertmanager надішле повідомлення в Telegram
4. На дашборді Grafana панель "Services Status" покаже `DOWN`

Перевірити алерти:
- Prometheus: http://localhost:9090/alerts
- Alertmanager: http://localhost:9093/#/alerts

### 4.3 Відновлення

```bash
docker start web-service-1
```

Через ~1 хвилину alert автоматично перейде в стан `RESOLVED`, і в Telegram прийде повідомлення про відновлення.

---

## Крок 5: Тестування MQTT

Для публікації повідомлень в MQTT можна використати:

### Через Postman (MQTT client)
- Host: `localhost`
- Port: `1883`
- Topic: `pz/test`

### Через командний рядок (якщо встановлено mosquitto-clients)
```bash
# Підписка
docker exec mosquitto mosquitto_sub -t "pz/test" &

# Публікація
docker exec mosquitto mosquitto_pub -t "pz/test" -m "Hello MQTT!"
```

---

## Зупинка всіх сервісів

```bash
cd stt-pz-3
docker compose down
```

Для повного видалення даних (volumes):
```bash
docker compose down -v
```

---

## Опис реалізованого алертингу

### Alert Rules (Prometheus)

| Alert | Умова | Severity |
|---|---|---|
| `ContainerDown` | Контейнер не відповідає > 60с | critical |
| `ServiceDown` | Prometheus target недоступний > 30с | critical |
| `MqttBrokerDown` | MQTT брокер недоступний > 30с | critical |
| `HighCpuUsage` | CPU > 80% протягом 1хв | warning |
| `HighMemoryUsage` | RAM > 80% протягом 1хв | warning |

### Маршрут сповіщень

```
Prometheus → Alertmanager → Telegram Bot → Ваш чат
```

Alertmanager групує алерти за назвою, чекає 10с перед відправкою (для групування), та повторює кожні 3 години якщо alert не вирішено.

---

## Структура проєкту

```
stt-pz-3/
├── docker-compose.yml              # Всі сервіси
├── broker/
│   └── mosquitto.conf              # Конфіг MQTT брокера
├── web1/
│   ├── Dockerfile
│   ├── app.py                      # Flask + Prometheus metrics + MQTT check
│   ├── requirements.txt
│   └── templates/
│       └── index.html              # MQTT WebSocket клієнт
├── web2/
│   ├── Dockerfile
│   ├── app.py                      # Flask + Prometheus metrics
│   └── requirements.txt
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml          # Scrape конфігурація
│   │   └── alert_rules.yml         # Правила алертів
│   ├── alertmanager/
│   │   └── alertmanager.yml        # Telegram notifications
│   └── grafana/
│       └── provisioning/
│           ├── datasources/
│           │   └── datasource.yml  # Prometheus як Data Source
│           └── dashboards/
│               ├── dashboard.yml   # Provider config
│               └── monitoring.json # Dashboard JSON
└── screenshots/
```

## Панелі дашборду Grafana

1. **Services Status** — статус всіх сервісів (UP/DOWN)
2. **Container CPU Usage (%)** — використання CPU контейнерами
3. **Container RAM Usage (MB)** — використання оперативної пам'яті
4. **Container Status (Up/Down)** — timeline стану контейнерів
5. **HTTP Request Rate (req/s)** — частота HTTP запитів до web1/web2
6. **MQTT Broker Availability** — доступність MQTT брокера
7. **HTTP Request Duration** — час відповіді web сервісів
8. **Container Network I/O** — мережевий трафік контейнерів
