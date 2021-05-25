install-dev:
	@pip install -r requirements/development.txt

run:
	@python manage.py runserver

shell:
	@python manage.py shell

deploy:
	@git push origin develop

migrate-stage:
	@heroku run python manage.py migrate --remote stage

migrate-prod:
	@heroku run python manage.py migrate --remote prod

migrate:
	@python manage.py makemigrations
	@python manage.py migrate

test:
	@python3 manage.py test