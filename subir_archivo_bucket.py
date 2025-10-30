import base64
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
    file_name = payload.get('file_name')
    file_content = payload.get('file_content')

    if not bucket_name or not file_name or not file_content:
        return {
            'statusCode': 400,
            'message': 'Los campos bucket, file_name y file_content son obligatorios.'
        }

    key_parts = []
    if directory:
        key_parts.append(directory.strip('/'))
    key_parts.append(file_name)
    object_key = '/'.join(part for part in key_parts if part)

    try:
        binary_content = base64.b64decode(file_content)
    except (base64.binascii.Error, TypeError):
        return {
            'statusCode': 400,
            'message': 'file_content debe estar codificado en base64.'
        }

    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=binary_content)
    except ClientError as error:
        return {
            'statusCode': 500,
            'message': f'Error al subir el archivo: {error.response["Error"]["Message"]}'
        }

    return {
        'statusCode': 200,
        'message': f'Archivo {object_key} subido correctamente a {bucket_name}.'
    }
