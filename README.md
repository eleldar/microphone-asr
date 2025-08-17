# Mictophone ASR

## Record

```bash
uv run src/recorder/handler.py

```

## Transcript
```bash
docker compose -f backend-compose.yml up --build -d
```

## WebUI

```bash
docker compose -f frontend-compose.yml up --build -d
```

## Test
```bash
uv run pytest
```
