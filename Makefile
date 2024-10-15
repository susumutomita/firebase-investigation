.PHONY: build
build:
	docker compose build

.PHONY: up
up:
	docker compose up

.PHONY: down
down:
	docker compose down -v

.PHONY: connect
connect:
	docker compose exec firebase-investigation /bin/bash
