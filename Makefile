create-migrations:
	@echo "Enter migration message: "; \
	read MESSAGE; \
	docker compose run --rm web_service uv run --no-dev alembic revision --autogenerate -m "$$MESSAGE"

migrate:
	docker compose run --rm web_service uv run --no-dev alembic upgrade head

clean-macos-trash-stuff:
	find . -name ".DS_Store" -type f -delete
