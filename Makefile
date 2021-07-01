install-dev:
	@pip install -r requirements/development.txt

run:
	@python manage.py runserver

shell:
	@python manage.py shell

deploy:
	@git push origin develop

check:
	@python3 manage.py check

migrate:
	@python manage.py makemigrations
	@python manage.py migrate

test:
	@python3 manage.py test