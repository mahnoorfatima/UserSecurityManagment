# Standard library imports
import os
import datetime

# Third party imports
import ujson
import boto3
from loguru import logger

client = boto3.client('cognito-idp')

# Constants
user_pool_id = os.environ['USER_POOL_ID']


class JsonDatetime(datetime.datetime):
    """[Perform serialization]

    Args:
        datetime ([datetime]): [string format]
    """
    def __json__(self):
        return f'{self.isoformat()}'


datetime.datetime = JsonDatetime


def create_user(email, user_attributes):
    """[Perform user creation with with email and password
        and force set password (may need future changes)]

    Args:
        email ([str]): [user email]
        user_attributes ([list<dict>]): [customer user attributes]
    """
    create_user_response = client.admin_create_user(
        UserPoolId=user_pool_id,
        Username=email,
        UserAttributes=user_attributes,
        ForceAliasCreation=False
    )

    logger.debug(f'USER_CREATION {ujson.dumps(create_user_response)}')

    return create_user_response
