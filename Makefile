.PHONY: docker-build
docker-build:
	docker compose build

.PHONY: docker-up
docker-up:
	docker compose up -d

.PHONY: docker-connect
docker-connect:
	docker compose exec firebase-investigation /bin/bash
