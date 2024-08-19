migrate-create: ## пример команды: make migrate-create 'MIGRATION="message"'
	alembic revision --autogenerate -m "$(MIGRATION)"

migrate-apply:
	alembic upgrade head