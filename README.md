# APS 3: Lambda + Docker

Para testar a aplicação basta:

```
docker build --platform linux/amd64 -t lambda-ex-image:test .
docker run -p 9500:8080 lambda-ex-image:test

curl "http://localhost:9500/2015-03-31/functions/function/invocations" -d '{}'

python3 create_repository.py

docker tag lambda-ex-image:test 820926566402.dkr.ecr.us-east-2.amazonaws.com/aps03_liviasm1:latest

docker push 820926566402.dkr.ecr.us-east-2.amazonaws.com/aps03_liviasm1:latest

python3 create_function.py

python3 create_api_gateway.py

python3 teste.py

```

Para deletar tudo o que foi feito, entrat na pasta `delete_everything`:

```
python3 delete_api.py
python3 delete_function.py
python3 delete_repository.py


```