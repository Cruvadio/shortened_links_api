# API for shortening URLs
## Deploying using docker-compose
~~~bash
docker-compose up -d --build
~~~
## Making migrations in data base: ##
~~~bash
docker-compose exec web alembic revision --autogenerate -m "Initial revision"
~~~~
~~~bash
docker-compose exec web alembic upgrade head
~~~
