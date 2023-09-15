# APS 3: Lambda + Docker

### Feito por :sassy_woman:

- Lívia Sayuri Makuta.

### Objetivo da APS 3 :round_pushpin:

A ideia de usar o Docker para fazer o deploy de dependências em AWS Lambda é contornar os limites de tamanho impostos ao empacotar uma função Lambda como um arquivo ZIP. Normalmente, quando uma função Lambda é criada, todas as dependências devem ser empacotadas, bibliotecas e código em um arquivo ZIP, que não pode exceder um determinado tamanho.

No entanto, o uso de contêineres Docker permite que um ambiente personalizado para sua função Lambda seja criado, incluindo todas as dependências e bibliotecas necessárias, sem se preocupar com os limites de tamanho do ZIP. O tamanho máximo permitido para um pacote de imagem de contêiner é significativamente maior, geralmente em torno de 10GB, o que oferece mais flexibilidade para incluir recursos adicionais.

Isso significa que é possível criar uma imagem de contêiner Docker que contém sua função Lambda, suas dependências e qualquer configuração necessária e, em seguida, implantá-la no AWS Lambda. Isso é particularmente útil quando sua função tem muitas dependências ou quando você precisa incluir recursos adicionais que excedem os limites tradicionais de tamanho de pacote.


### Construção da função de predição

Em atividades passadas desenvolvemos um modelo de ML que, com base em dados bancários, previa se um cliente de uma instituição bancária iria ou não se inscrever para um depósito a prazo. Esse conjunto de dados inclui informações sobre o cliente, como idade, emprego, estado civil, educação, status de crédito em atraso, saldo médio anual, empréstimo habitacional, empréstimo pessoal, e informações relacionadas ao último contato da campanha atual, como tipo de comunicação de contato, dia e mês do último contato, duração do último contato, entre outros.

Levando em consideração que já tínhamos os modelos prontos, apenas os utilizamos. Para isso, os arquivos `.pickle` foram copiados para a pasta `models` a qual foi copiada também para o container do Docker, conforme o arquivo de configuração indica:

```dockerfile

FROM public.ecr.aws/lambda/python:3.11

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

COPY models ${LAMBDA_TASK_ROOT}/models

# Install system dependencies
RUN yum install -y libstdc++ cmake gcc-c++ && \
    yum clean all && \
    rm -rf /var/cache/yum

# Install the specified packages
RUN pip install -r requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]

```

Um detalhe importante é que devido ao uso da biblioteca `lightgbm` que possuía outras dependências, foi necessário instalar a biblioteca libstdc++, o utilitário cmake e o compilador C++ gcc-c++.


Feito isso, os seguintes passos foram seguidos:

1) A imagem no Docker foi criada e testada localmente, através dos seguintes comandos:

```
docker build --platform linux/amd64 -t lambda-ex-image:test .
docker run -p 9500:8080 lambda-ex-image:test

curl "http://localhost:9500/2015-03-31/functions/function/invocations" -d '{}'

```
2) Um novo repositório no ECR foi criado:

```
python3 create_repository.py

```

3) Depois a sua imagem do Docker foi taggeada e mandada para o repositório ECR:

```
docker tag lambda-ex-image:test 820926566402.dkr.ecr.us-east-2.amazonaws.com/aps03_liviasm1:latest

docker push 820926566402.dkr.ecr.us-east-2.amazonaws.com/aps03_liviasm1:latest
```

4) Feito isso, a função lambda foi criada e associada com a imagem: 
```
python3 create_function.py
```

5) E por fim, um API gateway foi criado para testar o funcionamento dessa função:
```
python3 create_api_gateway.py

python3 teste.py
```

### Teste da função


O teste da função foi montado da seguinte maneira:

```
import requests

# Change the endpoint
url_endpoing = "https://example.execute-api.us-east-2.amazonaws.com"

url = f"{url_endpoing}/predict"

# Change the phrase
body = {
    "person": {
        "age": 59,
        "job": "admin.",
        "marital": "married",
        "education": "secondary",
        "balance": 2343,
        "housing": "yes",
        "duration": 1042,
        "campaign": 1
    }
}

resp = requests.post(url, json=body) #json=body

print(f"status code: {resp.status_code}")
print(f"text: {resp.text}")
```

Esse teste envia uma solicitação POST para um endpoint (URL) especificado. A solicitação inclui um corpo (body) em formato JSON, que contém informações sobre uma pessoa, como idade, profissão, estado civil, educação, saldo, habitação, duração e campanha.

O teste está simulando uma interação com um serviço da web que  realiza uma previsão ou análise com base nos dados da pessoa fornecidos no corpo da solicitação. Após o envio da solicitação, o teste imprime o código de status da resposta e o texto da resposta, conforme exemplo abaixo:

![Captura de tela de 2023-09-13 21-25-20](https://github.com/insper-classroom/23-2-mlops-aps03-Lihsayuri/assets/62647438/bf1cfd01-0939-435e-bf78-b81153b55773)



### Deletar recursos

Para deletar tudo o que foi feito, basta entrar na pasta `delete_everything`e rodar os seguintes comandos:

```
python3 delete_api.py
python3 delete_function.py
python3 delete_repository.py
```
