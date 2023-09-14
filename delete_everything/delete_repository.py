import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Nome do repositório que você deseja excluir
repository_name = "aps03_liviasm1"

# Crie um cliente Boto3 para o Amazon ECR
ecr_client = boto3.client(
    "ecr",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

# Exclua o repositório ECR
response = ecr_client.delete_repository(
    repositoryName=repository_name,
    force=True  # Isso é necessário se houver imagens no repositório
)

print(f"Resposta da exclusão: {response}")
print(f"Repositório {repository_name} excluído com sucesso")
