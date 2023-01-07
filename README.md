# LikeEstampa - Store
[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-orange.svg)](https://sonarcloud.io/summary/new_code?id=leonardocintra_likeestampa)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a91ffbdc0959414b836d5ff2848edf73)](https://app.codacy.com/gh/leonardocintra/likeestampa?utm_source=github.com&utm_medium=referral&utm_content=leonardocintra/likeestampa&utm_campaign=Badge_Grade_Settings)


[![CircleCI](https://circleci.com/gh/leonardocintra/likeestampa/tree/main.svg?style=svg)](https://circleci.com/gh/leonardocintra/likeestampa/tree/main)

Like Estampa - Store T-Shirts - Camisetas

## Como usar

### Dependencias
Seu PC precisa ter instalado
- Python3
- Docker e Docker Compose
- make (unix OS)
- virtualenv

#### MySQL
Caso estiver no Ubuntu
```
$ sudo apt-get install default-libmysqlclient-dev build-essential
$ docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql
```

Outros sitemas operacionais consulte: https://pypi.org/project/mysqlclient/

### Passo a passo primeira vez

- Criar o banco de dados manualmente
- Caso use o DBEaver ativar o allowPublicKeyRetrieval=True

Windows: TODO

Linux:

```
$ virtualenv env -p python3
$ source env/bin/activate
$ pip install -r requirements/requirements.development.txt
$ make migrate
$ make run
```



### Tecnologias
- Python3
- Django
- Docker
- MySQL Database (prod) | Postgres (dev)
- Bootstrap
- Mailgun (sistema de emails)
- Cloudinary (sistema de armazenamento de imagens)
- Mercado Pago (gateway de pagamento)
- Telegram (logs)
- Sentry (logs e eventos)


### Inicio e testes unitarios

```
$ git clone https://github.com/leonardocintra/likeestampa
$ cd likeestampa
$ virtualenv env -p pyhon3
$ souce env/bin/activate
$ make install-dev
$ sudo docker-compose up - d
$ python manage.py collectstatic --no-input
$ make test
```

### Executar local

Tem um arquivo `fixtores/utils/fixture.sql` que possui dados iniciais para voce brincar.

```
$ make migrate
$ python3 manage.py createsuperuser
$ ... (seguir passos superuser)
$ make run
```


## Testes
```
$ make test
```
### Coverage
```
$ make coverage
```

## Dicas
### Erros que podem aparecer
#### DETAIL:  Key (id)=(1) already exists.
Para corrigir execute o comando abaixo
```
python manage.py sqlsequencereset <nome da app> 
```
Ex: `python manage.py sqlsequencereset catalogo`


### Para debugar um teste no Visual Studio Code

Quando vai debugar um projeto django normal, VS Code inclui o comando "runserver".

Para debugar o teste, basta comentar ele e incluir "test" :D

```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "test"
                //"runserver"
            ],
            "django": true
        }
    ]
}
```

### Dump data
Exemplo
```
python3 manage.py dumpdata catalogo.categoria > categoria.json
```

Recuperar em produção
```
$ python3 manage.py dumpdata > db.json --indent 2 --exclude account --exclude pedido --exclude evento --exclude usuario --exclude auth --exclude contenttypes --exclude sessions --exclude pagamento --remote prod
```

## Historia
### Fundado em 20/04/2021

Por **Leonardo Nascimento Cintra** e **Juliana Rosa Rodrigues Cintra**

- Primeira maquina de estampa: **20/04/2021**
