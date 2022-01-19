# Standard library imports
import gzip
from io import BytesIO
import base64

# Third party imports
import ujson

# may need to remove as we will enable compression at GW level
response = {
    'statusCode': 200,
    # 'isBase64Encoded': False,
    'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    },
    'body': None
}


def gzip_b64encode(data):
    """[compress the response]

    Args:
        data ([dict]): [data provided for compression]

    Returns:
        [base54]: [base64 encoded compression]
    """
    compressed = BytesIO()
    with gzip.GzipFile(fileobj=compressed, mode='w') as file:
        json_response = ujson.dumps(data)
        file.write(json_response.encode('utf-8'))
    return base64.b64encode(compressed.getvalue()).decode('ascii')


def built_response(body, status_code=200):
    """[generate response for api gateway proxy]

    Args:
        body ([dict]): [provide dict to send over api]
        status_code (int, optional): [description]. Defaults to 200.

    Returns:
        [dict]: [response template]
    """
    response['statusCode'] = status_code
    response['body'] = ujson.dumps(body)
    return response
