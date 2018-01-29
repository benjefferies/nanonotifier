import sys

import requests
import time
import json

host = sys.argv[1]
account = sys.argv[2]
data = {
    'action': 'account_history',
    'account': account,
    'count': 10,
}


def get_trans_history():
    return requests.post(f'http://{host}:7076', json.dumps(data)).json().get('history', [])


last_known_trans = get_trans_history()
while True:
    trans_history = get_trans_history()
    new_trans = [x for x in trans_history if x not in last_known_trans]
    total = 0
    message = ''
    for tran in new_trans:
        if tran['type'] == 'receive':
            account = tran['account']
            amount = int(tran['amount'])
            if amount != 0:
                amount = amount/1000000
            total += amount
            message += f'New transaction from {account} for {amount}\n'

    if total > 0:
        print(f'Received {total} XRB')
        print(message)
    last_known_trans = trans_history
    time.sleep(5)

