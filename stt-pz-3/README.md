# Практична робота: pz-MQTT (стаття 3)

Опис: розгортається локальний MQTT-брокер (Eclipse Mosquitto) та два прості веб-сервіси у Docker для демонстрації працездатності. Також описані кроки для тестування Publish/Subscribe через Postman.

Файли в цьому каталозі:
- `broker/mosquitto.conf` — мінімальна конфігурація Mosquitto (включено websockets)
- `docker-compose.yml` — піднімає Mosquitto та два прості веб-сервіси (`web1`, `web2`)
- `web1/`, `web2/` — мінімальні Flask-сервіси для перевірки
- `screenshots/` — місце для збереження доказів (скріншотів чи логів)

Запуск
1) Відкрийте термінал у папці `stt-pz-3`.
2) Запустіть команду:

```
docker compose up --build
```

Сервіси:
- Mosquitto MQTT: брокер доступний на порту 1883 (TCP) та 9001 (WebSockets).
- Web1: http://localhost:5001/ повертає JSON {"service":"web1","status":"ok"}
- Web2: http://localhost:5002/ повертає JSON {"service":"web2","status":"ok"}

Тестування через Postman (MQTT)
1) Відкрийте Postman.
2) Створіть нове MQTT-з'єднання (New -> MQTT Request):
   mqtt://localhost:1883
3) Підписка (Subscribe): вкажіть topic `pz/test` та натисніть Subscribe.
4) Публікація (Publish): вкажіть topic `pz/test` та payload, наприклад `{ "msg": "hello from Postman" }`, натисніть Publish.
5) У вікні Subscribe має з'явитись повідомлення.

Перевірка веб-сервісів
- Відкрийте браузер або Postman і перейдіть до `http://localhost:5001/` та `http://localhost:5002/`.


