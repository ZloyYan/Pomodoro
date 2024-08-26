# Было
# run:
# 	poetry run uvicorn main:app --host 127.0.0.1 --port 8000 --reload --env-file $(ENV_FILE)

# Стало после внедрения порядка client-wsgi-asgi-app
run:
	poetry run gunicorn main:app --worker-class uvicorn.workers.UvicornWorker -c gunicorn.conf.py


migrate-create: ## пример команды: make migrate-create 'MIGRATION="message"'
	alembic revision --autogenerate -m "$(MIGRATION)"

migrate-apply:
	alembic upgrade head