import boto3

def lambda_handler(event, context):
    # Entrada

    # Proceso
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    lista = []
    for bucket in response['Buckets']:
        lista.append(bucket["Name"])

    # Salida
    return {
        'statusCode': 200,
        'lista_buckets': lista
    }