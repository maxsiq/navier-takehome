SERVICE = navier_takehome
TEST_DB = test_database.sqlite3

shell:
	docker exec -it $(SERVICE) /sh

migration:
	docker exec -it $(SERVICE) alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

upgrade:
	docker exec -it $(SERVICE) alembic upgrade head

downgrade:
	docker exec -it $(SERVICE) alembic downgrade -1

test:
	docker exec -it $(SERVICE) pytest -vv

format:
	docker exec $(SERVICE) black .

help:
	@echo "Available commands:"
	@echo "  shell       - Open a shell in the service container"
	@echo "  make migration \"msg\"   Create a new Alembic migration with a message"
	@echo "  upgrade     - Apply all migrations to the latest version"
	@echo "  downgrade   - Revert the last migration"
	@echo "  test        - Run tests using pytest"
	@echo "  help        - Show this help message"