install-dev:
	@pip install -r requirements/development.txt

run:
	@python manage.py runserver

shell:
	@python manage.py shell

deploy:
	@git push heroku main
	@git push origin main
	@heroku run python manage.py migrate

migrate:
	@python manage.py makemigrations
	@python manage.py migrate

test:
	@python3 manage.py test