NAME=fastapi_docker

run:
	docker-compose build
	docker-compose up -d

stop:
	docker-compose down

status:
	docker-compose ps

run-no:
	docker-compose build --no-cache
	docker-compose up -d

exec:
	docker-compose exec tensorflow bash

log:
	docker logs -f search_jinja_in_the_forest_tensorflow_1
	#docker-compose logs -f tensorflow

#heroku run bash

deploy:
	heroku container:push web
	heroku container:release web

logs:
	heroku logs

