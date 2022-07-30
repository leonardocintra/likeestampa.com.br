install-dev:
	@pip install -r requirements/development.txt
	@python3 manage.py collectstatic --noinput

run:
	@python manage.py runserver

shell:
	@python manage.py shell

check:
	@python3 manage.py check

migrate:
	@python3 manage.py makemigrations
	@python3 manage.py migrate

deploy-stage:
	@git push stage main
	@heroku run python3 manage.py migrate --remote stage

deploy-prod:
	@git push prod main
	@heroku run python3 manage.py migrate --remote prod

test:
	@python3 manage.py test -v 2 --parallel 1

coverage:
	@coverage run --source='.' manage.py test -v 2 && coverage report && coverage html