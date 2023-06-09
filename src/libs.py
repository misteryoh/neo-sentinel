# Importação das bibliotecas a serem utilizadas
import requests
import logging
import time
import boto3
from botocore.exceptions import ClientError

################################################################
# Reusable functions
################################################################

def make_request(url, method, dados=None, headers=None):
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=dados, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=dados, headers=headers)
        else:
            raise ValueError("Método de requisição inválido. Use GET ou POST.")
        
        response.raise_for_status()  # Lança uma exceção se a resposta não for bem-sucedida
        return response  # Retorna a resposta
    except requests.exceptions.RequestException as e:
        print(f"Erro durante a chamada GET: {e}")
        return None

def upload_s3_object(content, profile, bucket, folder, filename):
    """Upload an object to an S3 bucket

    :param content: Content to upload
    :param profile: AWS profile to be used
    :param bucket: S3 bucket name
    :param folder: Folder name
    :param filename: S3 object name
    :return: True if object was uploaded, else False
    """

    # Create a session using the specified configuration file
    if profile is None:
        session = boto3.Session()
    else:
        session = boto3.Session(profile_name=profile, region_name='sa-east-1')

    s3_client = session.client('s3')

    try:
        # Put object into the S3 bucker
        s3_object = s3_client.put_object(
            Bucket=bucket, Key=f"{folder}/{filename}", Body=content)

        return s3_object
        
    except ClientError as e:
        logging.error(e)
        return False

def save_file(content, file_name, file_type):
    with open(f'{file_name}.{file_type}', 'wb') as file:
        file.write(content.content)
    print(f'File saved at {file_name}.{file_type}')
        
def tempo_de_execucao(funcao):
    def wrapper(event, context):
        inicio = time.time()
        funcao(event, context)
        fim = time.time()
        tempo_execucao = (fim - inicio) / 60.0
        print("Tempo de execução:", tempo_execucao, "minutos")
    return wrapper

