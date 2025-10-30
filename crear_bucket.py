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
    region = payload.get('region')

    if not bucket_name:
        return {
            'statusCode': 400,
            'message': 'El campo bucket es obligatorio.'
        }

    s3 = boto3.client('s3')
    params = {'Bucket': bucket_name}

    if region and region != 'us-east-1':
        params['CreateBucketConfiguration'] = {
            'LocationConstraint': region
        }

    try:
        s3.create_bucket(**params)
    except ClientError as error:
        return {
            'statusCode': 500,
            'message': f'Error al crear el bucket: {error.response["Error"]["Message"]}'
        }

    return {
        'statusCode': 200,
        'message': f'Bucket {bucket_name} creado correctamente.'
    }
