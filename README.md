# LikeEstampa - Store
Like Estampa - Store T-Shirts

## Como usar

### Dependencias
Seu PC precisa ter instalado
- Python3
- Docker e Docker Compose
- make (unix OS)
- virtualenv

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

Tem um arquivo `fixture.sql` que possui dados iniciais para voce brincar.

```
$ make migrate
$ python3 manage.py createsuperuser
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

## Historia
### Fundado em 20/04/2021

Por **Leonardo Nascimento Cintra** e **Juliana Rosa Rodrigues Cintra**

- Primeira maquina de estampa: **20/04/2021**
