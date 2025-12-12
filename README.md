# ML Deployment: FastAPI + Docker + Blue/Green + Nginx + GitHub Actions

Мини-пример ML-сервиса (FastAPI), который:
- обучает простую модель (`train_model.py`) и сохраняет артефакт `model.pkl`;
- поднимает API с эндпоинтами `/health` и `/predict`;
- деплоится по стратегии **Blue/Green** через **nginx**;
- собирает и пушит Docker-образ в **GHCR** через **GitHub Actions** и делает smoke-test.

---

## 1) Blue/Green

Идея:
- **Blue** — текущая «боевaя» версия сервиса (`v1.0.0`)
- **Green** — новая версия (например, `v1.1.0`), развёрнута параллельно

Обе версии работают одновременно в Docker сети:
- `blue:8080`
- `green:8080`

Снаружи доступен только nginx на порту `8080`:
- nginx проксирует запросы либо на `blue`, либо на `green`
- переключение делается без остановки обеих версий, через reload nginx-конфига

Это даёт:
- безопасный rollout (можно проверить green отдельно)
- быстрый rollback обратно на blue

---
<img width="974" height="582" alt="image" src="https://github.com/user-attachments/assets/6fc360cd-0cc2-4c16-87eb-528189367b1f" />


## 2) Структура проекта

- `app/` — blue-версия приложения  
- `app_green/` — green-версия приложения (например отличается `/health` → добавляет `"color":"green"`)
- `nginx/default.conf` — конфиг роутинга (куда проксировать)
- `Dockerfile` — образ blue
- `Dockerfile.green` — образ green
- `docker-compose.*.yml` — сборка окружения blue/green/nginx
- `.github/workflows/deploy.yml` — CI: build/push в GHCR + smoke-test

---

## 3) Локальный запуск (Docker + nginx router)

### Запуск всех сервисов (blue + green + nginx)

```bash
docker compose -f docker-compose.bg.yml up --build -d
---

### Проверка состояния

```bash
curl -s http://127.0.0.1:8080/health && echo

---

### Проверка предсказаний

```bash
curl -s -X POST http://127.0.0.1:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"x":[1,2,3]}' && echo
---

## 4) Переключение Blue ↔ Green (без даунтайма)

Вариант A: правим proxy_pass

В nginx/default.conf меняем upstream:

на blue:

```bash
proxy_pass http://blue:8080;

---
на green:
```bash
proxy_pass http://green:8080;

---

После изменения делаем reload nginx:

```bash
docker compose -f docker-compose.bg.yml exec nginx nginx -s reload
---

## Версии

Blue: MODEL_VERSION=v1.0.0

Green: MODEL_VERSION=v1.1.0

Green-версия дополнительно возвращает "color":"green" в /health для наглядного подтверждения переключения.

## Logs
Логи пишутся в stdout контейнера (Docker собирает их автоматически).
Посмотреть:
- docker compose -f docker-compose.bg.yml logs -f blue
- docker compose -f docker-compose.bg.yml logs -f green
- docker compose -f docker-compose.bg.yml logs -f nginx






