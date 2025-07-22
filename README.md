# Wallet API

Simple Django + DRF project for the B2Broker test task.

---

## Quick start

```bash
# 1. Clone the repo
git clone https://github.com/anushST/b2broker_test.git
cd b2broker_test

# 2. Copy env settings (edit if you need)
cp .env.example .env

# 3. Build and run the containers
docker compose up -d --build

# 4. Go into container
docker compose exec -it wallet bash

# 5. Run linter
flake8 --toml-config=pyproject.toml	

# 6. Run tests
pytest

# 7. Exit from container
Ctrl+D
```
