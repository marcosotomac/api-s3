import json
import boto3
from botocore.exceptions import ClientError


def _parse_body(event):
    body = event.get('body')
    if isinstance(body, str):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {}
    return body or {}


def lambda_handler(event, context):
    payload = _parse_body(event)
    bucket_name = payload.get('bucket')
    directory = payload.get('directory')

    if not bucket_name or not directory:
        return {
            'statusCode': 400,
            'message': 'Los campos bucket y directory son obligatorios.'
        }

    key_name = directory.strip('/') + '/'
    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket=bucket_name, Key=key_name)
    except ClientError as error:
        return {
            'statusCode': 500,
            'message': f'Error al crear el directorio: {error.response["Error"]["Message"]}'
        }

    return {
        'statusCode': 200,
        'message': f'Directorio {key_name} creado correctamente en {bucket_name}.'
    }
