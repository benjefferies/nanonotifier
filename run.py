import sys

import requests
import time

host = sys.argv[0]
account = sys.argv[1]
trans = []
while True:
    data = {
        'action': 'account_history',
        'account': account,
        'count': 10,
    }
    data = requests.post(f'{host}:7076', data).json()
    new_trans = set(trans) - set(data.history)
    for tran in new_trans:
        if tran.type == 'receive':
            print(f'New transaction from {tran.account} for {tran.amount}')

    time.sleep(5)
