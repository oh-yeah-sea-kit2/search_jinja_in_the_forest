#NAME=tensorflow
NAME=web

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
	docker-compose exec $(NAME) bash

log:
	docker logs -f search_jinja_in_the_forest_$(NAME)_1
	#docker-compose logs -f $(NAME)

#heroku run bash

deploy:
	heroku container:login
	heroku container:push $(NAME)
	heroku container:release $(NAME)

logs:
	heroku logs --tail

