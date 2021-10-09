install-dev:
	@pip install -r requirements/development.txt
	@python3 manage.py collectstatic --noinput

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
	@python3 manage.py test -v 2

coverage:
	@coverage run --source='.' manage.py test -v 2 && coverage report && coverage html