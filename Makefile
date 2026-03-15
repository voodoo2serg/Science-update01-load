up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

test:
	docker compose run --rm backend pytest -q

install:
	bash scripts/install.sh
