# Практична робота pz‑MQTT (stt‑pz‑3)
Мета: розгорнути MQTT‑брокер (Eclipse Mosquitto), налаштувати базову конфігурацію та продемонструвати обмін повідомленнями (Publish/Subscribe).

---

## Що в репозиторії

- `broker/docker-compose.yml` — Docker Compose для запуску Mosquitto
- `broker/mosquitto.conf` — мінімальна конфігурація (persistence, websockets)
- `examples/` — прості скрипти для демонстрації (Node.js): `publisher.js`, `subscriber.js`
- `screenshots/` — покладіть сюди скриншоти або логи як докази

---

## Коротка інструкція (Quick start)

Підготуйтеся:
- Встановіть Docker (якщо ще не встановлений).
- Встановіть Node.js (для прикладів у `examples`).

Запустіть брокер (в PowerShell):

```powershell
Set-Location .\stt-pz-3\broker
docker compose up -d
```

Подивитись логи:

```powershell
docker compose logs -f
```

Після запуску брокер слухатиме:
- MQTT TCP: `localhost:1883`
- WebSocket (опційно): `localhost:9001`

---

## Демонстрація Publish/Subscribe

Node.js приклади (у `stt-pz-3/examples`)

Інсталяція і запуск:

```powershell
Set-Location .\stt-pz-3\examples
npm install
# В одному терміналі
node .\subscriber.js
# В іншому терміналі
node .\publisher.js
```

Очікування у subscriber:

```
Subscriber connected
Subscribed to test/topic
Message received on test/topic: {"time":"...","msg":"hello from publisher"}
```

---

## Як зафіксувати роботу (докази)

- Зробіть скриншот або збережіть текст логів з запуску контейнера (`docker compose logs`), з виводу `subscriber` і `publisher`, або з Postman.
- Помістіть файли у `stt-pz-3/screenshots/` з короткими підписами, наприклад:
	- `01-docker-ps.png` — вивід `docker ps`
	- `02-subscriber.png` — вивід підписувача
	- `03-publisher.png` — вивід публікатора

---

## Чек‑лист для приймання роботи

- [ ] Docker‑контейнер брокера запущено (порти 1883/9001)
- [ ] `mosquitto.conf` є в `broker/` і містить persistence/websockets
- [ ] Демонстрація Publish/Subscribe (CLI або Postman або Node.js)
- [ ] Пояснення основних понять MQTT (Topic, Publish, Subscribe, QoS) в README
- [ ] Скриншоти/логи додані до `stt-pz-3/screenshots/`

---

## Пояснення основних понять (коротко)

- Topic — адреса/канал повідомлень (наприклад `test/topic`).
- Publish — відправка повідомлення в topic.
- Subscribe — підписка на topic для отримання повідомлень.
- QoS — level доставки: 0 (всього найменше раз), 1 (принаймні один раз), 2 (точно один раз).

