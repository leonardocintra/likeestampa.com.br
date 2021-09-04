# LikeEstampa - Store
Like Estampa - Store T-Shirts

[![Build Status](https://travis-ci.com/leonardocintra/likeestampa.svg?branch=main)](https://travis-ci.com/leonardocintra/likeestampa)

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

## Historia
### Fundado em 20/04/2021

Por **Leonardo Nascimento Cintra** e **Juliana Rosa Rodrigues Cintra**

- Primeira maquina de estampa: **20/04/2021**
