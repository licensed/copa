Sistema de Bolão da Copa do Mundo feito em Flask.
Possui app em Flask, além de api restful com as funcionalidades abaixo:

| Function | HTTP Methods |
| ------ | ----------- |
| /time/ | GET, POST   |
| /time/<id> | GET, PUT, DELETE  |
| /partida/ | GET, POST   |
| /partida/<id> | GET, PUT, DELETE  |
| /aposta/ | GET, POST   |
| /aposta/<id> | GET, PUT, DELETE  |


Examples:

```
$ curl -X GET http://localhost:5000/time/
	{
  "1": {
    "nome": "Brasil", 
    "posicao": 0, 
    "sigla": "BRA"
  }, 
  "2": {
    "nome": "Argentina", 
    "posicao": 0, 
    "sigla": "ARG"
  }
}
```

```
$ curl -X GET http://localhost:5000/time/1
{
  "nome": "Brasil", 
  "posicao": 0, 
  "sigla": "BRA"
}
```

```
$ curl -X GET http://localhost:5000/partida/
{
  "1": {
    "local": "RJ", 
    "placar_time1": "2", 
    "placar_time2": "0", 
    "time1": "BRA", 
    "time2": "ARG"
  }, 
  "2": {
    "local": "SP", 
    "placar_time1": "1", 
    "placar_time2": "1", 
    "time1": "BRA", 
    "time2": "MEX"
  }
}
```

```
$ curl -X GET http://localhost:5000/partida/1/
{
  "1": {
    "local": "RJ", 
    "placar_time1": "2", 
    "placar_time2": "0", 
    "time1": "BRA", 
    "time2": "ARG"
  }
}
```