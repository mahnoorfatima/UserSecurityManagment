# Third party imports
import boto3

# User based imports
from constants import constants

iot_client = boto3.client('iot')


def attach_iot_policy(policy_name, identity_id):
    """[Perform attachment of policy for iot on user]

    Args:
        policy_name ([str]): [name of IoR policy]
        identity_id ([str]): [identity id from congnito identity provider]

    Returns:
        [dict]: [response of attach policy]
    """
    response = iot_client.attach_policy(
        policyName=policy_name,
        target=identity_id
    )
    return response


def get_user_attributes(client_id, customer_id, is_client_admin, is_customer_admin, 
                        user_name, name, email):
    """[get user attributes]

    Args:
        client_id ([str]): [client id]
        is_client_admin (bool): [is client admin]
        is_customer_admin (bool): [is customer admin]
        user_name ([str]): [name of user]
        name ([str]): [full name of user]
        email ([str]): [email of user]

    Returns:
        [list]: [return the list of dict with user attributes]
    """
    user_attributes = [
        {
            'Name': 'custom:clientId',
            'Value': client_id
        },
        {
            'Name': 'custom:isClientAdmin',
            'Value': is_client_admin
        },
        {
            'Name': 'custom:isCustomerAdmin',
            'Value': is_customer_admin
        },
        {
            'Name': 'custom:userName',
            'Value': user_name
        },
        {
            "Name": 'name',
            "Value": name
        },
        {
            "Name": 'email',
            "Value": email
        },
        {
            'Name': 'email_verified',
            'Value': 'true'
        }
    ]

    if customer_id is not None:
        user_attributes.append({
            'Name': 'custom:customerId',
            'Value': customer_id
        })
    return user_attributes


def check_client_user_limit(client):
    """[check if client has reached maximum
        users]

    Args:
        client ([dict]): [JSON document of client table]

    Returns:
        [bool]: [boolean if max users of client reached]
    """
    if client[constants.TOTAL_USER] < client['maxUsers']:
        return True
    return False
