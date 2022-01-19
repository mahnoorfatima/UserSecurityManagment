"""[Constants]
"""
CLIENT_TABLE = 'client'
CUSTOMER_TABLE = 'customer'
CLIENT_USER_TABLE = 'client-user'
USER_TABLE = 'user'
TOTAL_USER = 'usersTotal'
UPDATE_EXPRESSION = f'SET {TOTAL_USER}=if_not_exists({TOTAL_USER},:start)+:inc'
